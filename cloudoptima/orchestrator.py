"""Orchestrator — runs the five-agent pipeline (Phase 6).

What happens, in order:

1. The four specialists run sequentially (Architect → Cost Analyst → Security
   → Compliance). Each turn lands on ``session.agent_turns`` as it completes,
   so downstream agents read upstream output and the judge sees all four plus
   the detected conflicts.
2. Disagreements are detected across all **six** specialist pairs. Detection
   is deterministic and keyed per pair — the budget check can only fire for
   (Architect, Cost Analyst). (v1 lesson: it used to fire for every pair and
   tripled the duplicates.) Schemas are read directly, so a key mismatch
   between agents (compliance's ``rules`` vs security's ``findings``) can
   never invent a conflict.
3. The Judge arbitrates with all outputs + the conflicts; its resolutions are
   folded back into the session, and conflicts it noticed but the detector
   missed are adopted.
4. Four artifacts are generated: Bicep template, cost forecast, compliance
   report, arbitration summary. The IaC is malware-scanned before it's stored.

Failure isolation: an agent that fails becomes an error turn and the pipeline
keeps going. If anything unexpected still raises, ``run`` marks the session
``failed`` and returns it — it never crashes the caller.

Example:
    >>> from cloudoptima.orchestrator import Orchestrator
    >>> orch = Orchestrator.from_settings(Settings())
    >>> session = orch.run(session)
"""

from __future__ import annotations

import json
import logging
import re
import threading
import time
from datetime import UTC, datetime
from typing import Any, Final

from cloudoptima.agent_base import BaseAgent
from cloudoptima.agents import ALL_AGENTS
from cloudoptima.config import Settings
from cloudoptima.llm_client import create_llm_client
from cloudoptima.llm_routing import create_routed_client
from cloudoptima.mcp_bridge import get_tool_executor
from cloudoptima.models import AgentTurn, AgentType, Artifact, Conflict, Session
from cloudoptima.observability import TraceEvent, get_audit_logger
from cloudoptima.sanitize import clean_output, rate_limit, scan_for_malware_in_iac

_logger = logging.getLogger(__name__)

# ── Constants ───────────────────────────────────────────────────────────

# Pipeline execution order — matches ALL_AGENTS in cloudoptima.agents.
_PIPELINE_TYPES: Final[tuple[AgentType, ...]] = (
    AgentType.ARCHITECT,
    AgentType.COST_ANALYST,
    AgentType.SECURITY,
    AgentType.COMPLIANCE,
    AgentType.JUDGE,
)

# Bicep resource types keyed by architect output section.
_RESOURCE_TYPES: Final[dict[str, str]] = {
    "compute": "Microsoft.ContainerService/managedClusters@2024-02-01",
    "storage": "Microsoft.Storage/storageAccounts@2023-01-01",
    "networking": "Microsoft.Network/virtualNetworks@2023-01-01",
    "data": "Microsoft.Sql/servers@2023-01-01",
}

# Bicep resource bodies keyed by architect output section.
# Braces that are literal Bicep syntax MUST be doubled ({{ / }}) because Python
# str.format() interprets single braces as placeholders. Only {slug} is a real
# placeholder.
_RESOURCE_BODIES: Final[dict[str, str]] = {
    "compute": (
        "  name: 'aks-{slug}'\n"
        "  location: location\n"
        "  identity: {{ type: 'SystemAssigned' }}\n"
        "  properties: {{\n"
        "    dnsPrefix: 'aks{slug}'\n"
        "    agentPoolProfiles: [\n"
        "      {{ name: 'system', count: 3, vmSize: 'Standard_D4s_v3' }}\n"
        "    ]\n"
        "  }}"
    ),
    "storage": (
        "  name: 'st{slug}'\n"
        "  location: location\n"
        "  kind: 'StorageV2'\n"
        "  sku: {{ name: 'Standard_LRS' }}\n"
        "  properties: {{\n"
        "    minimumTlsVersion: 'TLS1_2'\n"
        "    allowBlobPublicAccess: false\n"
        "  }}"
    ),
    "networking": (
        "  name: 'vnet-{slug}'\n"
        "  location: location\n"
        "  properties: {{\n"
        "    addressSpace: {{ addressPrefixes: ['10.0.0.0/16'] }}\n"
        "  }}"
    ),
    "data": (
        "  name: 'sql-{slug}'\n"
        "  location: location\n"
        "  properties: {{\n"
        "    administratorLogin: 'cloudoptima_admin'\n"
        "    minimalTlsVersion: '1.2'\n"
        "  }}"
    ),
}

_ARTIFACT_DESCRIPTIONS: Final[dict[str, str]] = {
    "iac_bicep": "Bicep template derived from the architect's design",
    "cost_forecast": "Monthly cost estimate and breakdown from the cost analyst",
    "compliance_report": "Compliance rule-by-rule report from the compliance officer",
    "arbitration_summary": "Judge arbitration: final recommendation and resolutions",
}

# Rate limiting (Phase 10.4). The global key and window are shared by every
# orchestrator instance in this process, matching the checklist's "60 analyses
# per hour" rule. Per-session concurrency is enforced by _SessionGate.
_GLOBAL_RATE_KEY: Final[str] = "global"
_GLOBAL_RATE_WINDOW_SEC: Final[float] = 3600.0


class _SessionGate:
    """Tracks in-flight pipeline runs per session (Phase 10.4).

    ``rate_limit_per_session`` (default 1) bounds how many pipeline runs may be
    in flight for the same session id at once. The dashboard disables its
    Analyze button while a run is active, but the gate is the real enforcement
    for the CLI and any concurrent callers — without it, two threads could
    race the same session and interleave agent turns.
    """

    def __init__(self) -> None:
        self._counts: dict[str, int] = {}
        self._lock = threading.Lock()

    def acquire(self, session_id: str, limit: int) -> bool:
        """Try to start a run for ``session_id``; False when at capacity."""
        with self._lock:
            current = self._counts.get(session_id, 0)
            if current >= limit:
                return False
            self._counts[session_id] = current + 1
            return True

    def release(self, session_id: str) -> None:
        """End a run for ``session_id`` (idempotent)."""
        with self._lock:
            current = self._counts.get(session_id, 0)
            if current <= 1:
                self._counts.pop(session_id, None)
            else:
                self._counts[session_id] = current - 1


class Orchestrator:
    """Runs the five-agent pipeline over a session and returns the updated session.

    Attributes:
        agents:  All five agents keyed by :class:`AgentType`.
        config:  Application settings shared by every agent.
    """

    def __init__(
        self,
        agents: dict[AgentType, BaseAgent],
        config: Settings,
    ) -> None:
        """Wire the orchestrator with its agents and shared settings.

        Args:
            agents: A complete mapping of all five :class:`AgentType` roles to
                their agent instances.
            config: The application :class:`Settings` used for shared behavior.

        Raises:
            ValueError: If any of the five agent roles is missing.
        """
        missing = set(_PIPELINE_TYPES) - set(agents.keys())
        if missing:
            raise ValueError(f"Orchestrator is missing agents: {sorted(m.value for m in missing)}")
        self.agents = agents
        self.config = config
        self._session_gate = _SessionGate()
        # Issue #7: tool executor (MCP when enabled, else the in-process
        # registry) — lets callers run tools with the session's settings.
        self.tools = get_tool_executor(config)

    @classmethod
    def from_settings(cls, settings: Settings) -> Orchestrator:
        """Build a fully-wired orchestrator from application settings.

        Creates one LLM client (Mock/Nvidia/Azure per ``settings.llm_provider``)
        and instantiates every agent from :data:`ALL_AGENTS` in pipeline order.

        Args:
            settings: The application :class:`Settings`.

        Returns:
            A ready-to-run :class:`Orchestrator`.
        """
        llm_client = (
            create_routed_client(settings)
            if settings.routing_enabled
            else create_llm_client(settings)
        )
        agents: dict[AgentType, BaseAgent] = {
            agent_type: agent_cls(agent_type, llm_client, settings)
            for agent_type, agent_cls in zip(_PIPELINE_TYPES, ALL_AGENTS, strict=True)
        }
        return cls(agents=agents, config=settings)

    # ── Pipeline ────────────────────────────────────────────────────────

    def run(self, session: Session) -> Session:
        """Execute the full pipeline over a session. Never raises.

        Pipeline outputs are reset first so re-running the same session is
        deterministic; then the four specialists run, conflicts are detected,
        the judge arbitrates, and the four artifacts are generated. Any
        unexpected exception marks the session ``failed`` and returns it with
        whatever turns completed — the caller never sees a crash.

        Args:
            session: The session to analyze. User inputs are preserved; the
                pipeline outputs are replaced.

        Returns:
            The updated session with ``status`` set to ``completed`` or
            ``failed``.
        """
        started = time.monotonic()

        # Phase 10.4: block BEFORE any LLM call so a throttled analysis costs
        # no API credits. The global hourly quota is shared process-wide.
        if not rate_limit(
            _GLOBAL_RATE_KEY,
            self.config.rate_limit_global_per_hour,
            _GLOBAL_RATE_WINDOW_SEC,
        ):
            session.status = "failed"
            session.updated_at = datetime.now(UTC)
            session.error_message = (
                "Rate limit exceeded: the global hourly quota "
                f"({self.config.rate_limit_global_per_hour} analyses/hour) is exhausted. "
                "Try again in about an hour."
            )
            self._log_run_event(
                session, started, "rate_limited",
                extra={"reason": "global hourly quota exhausted"},
            )
            return session

        # Phase 10.4: at most `rate_limit_per_session` runs in flight per
        # session (default 1) — prevents two threads interleaving one session.
        if not self._session_gate.acquire(
            session.session_id, self.config.rate_limit_per_session
        ):
            session.status = "failed"
            session.updated_at = datetime.now(UTC)
            session.error_message = (
                "Rate limit exceeded: another analysis for this session is "
                "already running. Wait for it to finish."
            )
            self._log_run_event(
                session, started, "rate_limited",
                extra={"reason": "session already in flight"},
            )
            return session

        try:
            return self._run_locked(session, started)
        finally:
            self._session_gate.release(session.session_id)

    def _run_locked(self, session: Session, started: float) -> Session:
        """Execute the pipeline after the rate-limit gates have passed."""
        session.status = "running"
        session.updated_at = datetime.now(UTC)
        session.error_message = ""

        # Deterministic re-runs: pipeline outputs are owned by run().
        session.agent_turns = []
        session.conflicts = []
        session.artifacts = []

        turns: dict[AgentType, AgentTurn] = {}
        try:
            for agent_type in _PIPELINE_TYPES:
                if agent_type == AgentType.JUDGE:
                    continue
                turn = self.agents[agent_type].analyze(session)
                session.agent_turns.append(turn)
                turns[agent_type] = turn

            session.conflicts = self._detect_conflicts(session, turns)

            judge_turn = self.agents[AgentType.JUDGE].analyze(session)
            session.agent_turns.append(judge_turn)
            turns[AgentType.JUDGE] = judge_turn

            self._apply_judge_resolutions(session, judge_turn)
            session.artifacts = self._generate_artifacts(session, turns, judge_turn)
            session.status = "completed"
        except Exception as exc:
            _logger.exception("Orchestrator run failed for session %s", session.session_id)
            session.status = "failed"
            session.error_message = clean_output(str(exc))[:500]
            self._log_run_event(session, started, "error", extra={"error": str(exc)})
            return session

        self._log_run_event(session, started, "success")
        return session

    # ── Conflict detection ──────────────────────────────────────────────

    def _detect_conflicts(
        self,
        session: Session,
        turns: dict[AgentType, AgentTurn],
    ) -> list[Conflict]:
        """Compare the four specialist outputs across all six pairs.

        Each pair has its own focused question (does the design fit the budget?
        is it secure? does it comply? can we afford the security controls? can
        we afford compliance? do security and compliance agree?). A pair that
        does not apply (e.g. no budget provided, or an agent failed) yields no
        conflict. Results are deterministic and ordered by ``_SPECIALIST_PAIRS``.

        Args:
            session: The session carrying the user's budget and settings.
            turns:   The four specialist turns keyed by agent type.

        Returns:
            A list of unresolved :class:`Conflict` objects (``resolution`` is
            empty until the judge arbitrates).
        """
        arch = self._output_of(turns, AgentType.ARCHITECT)
        cost = self._output_of(turns, AgentType.COST_ANALYST)
        security = self._output_of(turns, AgentType.SECURITY)
        compliance = self._output_of(turns, AgentType.COMPLIANCE)
        budget = session.budget

        conflicts: list[Conflict] = []

        # Architect vs Cost — does the design fit the budget?
        if arch is not None and cost is not None:
            estimate = cost.get("estimate")
            over_budget = (
                budget is not None
                and isinstance(estimate, (int, float))
                and estimate > budget
            )
            if over_budget or cost.get("budget_status") == "OVER":
                if budget is not None and isinstance(estimate, (int, float)):
                    issue = (
                        f"Estimated monthly cost ${estimate:,.2f} exceeds the "
                        f"${budget:,.2f} budget"
                    )
                else:
                    issue = "Cost analyst reports the design is over budget"
                conflicts.append(
                    Conflict(
                        dimension="architect_vs_cost",
                        agents=[AgentType.ARCHITECT, AgentType.COST_ANALYST],
                        issue=issue,
                        resolution="",
                    )
                )

        # Architect vs Security — is the design secure?
        if arch is not None and security is not None:
            risk = security.get("overall_risk_rating")
            fail_findings = [
                f
                for f in security.get("findings", [])
                if isinstance(f, dict) and f.get("status") == "FAIL"
            ]
            if risk in ("HIGH", "CRITICAL") or fail_findings:
                conflicts.append(
                    Conflict(
                        dimension="architect_vs_security",
                        agents=[AgentType.ARCHITECT, AgentType.SECURITY],
                        issue=(
                            f"Architecture carries a {risk or 'FAIL'} security "
                            "finding that must be addressed"
                        ),
                        resolution="",
                    )
                )

        # Architect vs Compliance — does the design follow regulations?
        if arch is not None and compliance is not None:
            if compliance.get("overall_status") == "NEEDS_WORK":
                remediation = compliance.get("remediation_steps", [])
                first_step = (
                    remediation[0] if remediation else "see the compliance report"
                )
                conflicts.append(
                    Conflict(
                        dimension="architect_vs_compliance",
                        agents=[AgentType.ARCHITECT, AgentType.COMPLIANCE],
                        issue=(
                            "Architecture does not yet satisfy compliance "
                            f"requirements: {first_step}"
                        ),
                        resolution="",
                    )
                )

        # Cost vs Security — can we afford the security controls?
        if cost is not None and security is not None:
            estimate = cost.get("estimate")
            open_gaps = [
                f
                for f in security.get("findings", [])
                if isinstance(f, dict) and f.get("status") != "PASS"
            ]
            if (
                budget is not None
                and isinstance(estimate, (int, float))
                and estimate >= budget
                and open_gaps
            ):
                conflicts.append(
                    Conflict(
                        dimension="cost_vs_security",
                        agents=[AgentType.COST_ANALYST, AgentType.SECURITY],
                        issue=(
                            "Remediating open security gaps may push the "
                            "solution over budget"
                        ),
                        resolution="",
                    )
                )

        # Cost vs Compliance — can we afford compliance?
        if cost is not None and compliance is not None:
            estimate = cost.get("estimate")
            if (
                budget is not None
                and isinstance(estimate, (int, float))
                and estimate > budget
                and compliance.get("overall_status") == "NEEDS_WORK"
            ):
                conflicts.append(
                    Conflict(
                        dimension="cost_vs_compliance",
                        agents=[AgentType.COST_ANALYST, AgentType.COMPLIANCE],
                        issue=(
                            "Compliance remediation and the estimated cost both "
                            "pressure the budget"
                        ),
                        resolution="",
                    )
                )

        # Security vs Compliance — do security and compliance agree?
        if security is not None and compliance is not None:
            risk = security.get("overall_risk_rating")
            if risk in ("HIGH", "CRITICAL") and compliance.get("overall_status") == "PASS":
                conflicts.append(
                    Conflict(
                        dimension="security_vs_compliance",
                        agents=[AgentType.SECURITY, AgentType.COMPLIANCE],
                        issue=(
                            "Security reports critical risk while compliance "
                            "reports a full pass"
                        ),
                        resolution="",
                    )
                )

        return conflicts

    # ── Judge arbitration ───────────────────────────────────────────────

    def _apply_judge_resolutions(
        self,
        session: Session,
        judge_turn: AgentTurn,
    ) -> None:
        """Fold the judge's arbitration back into the session's conflicts.

        For each judge conflict summary, match it to a detected conflict by the
        set of involved agents and fill in the resolution. Summaries that the
        deterministic detector missed (the judge saw something we did not) are
        adopted as new resolved conflicts so the final list always reflects the
        judge's view. Malformed summaries are skipped — never crashes.

        Args:
            session:   The session whose ``conflicts`` list is updated.
            judge_turn: The judge's turn (may carry an error).
        """
        output = judge_turn.output
        if "error" in output:
            return
        arbitration = output.get("arbitration")
        summaries = arbitration.get("conflict_summaries") if isinstance(arbitration, dict) else None
        if not isinstance(summaries, list):
            return

        for summary in summaries:
            if not isinstance(summary, dict):
                continue
            involved = summary.get("agents_involved")
            if not isinstance(involved, list):
                continue
            key = {str(getattr(agent, "value", agent)) for agent in involved}
            if not key:
                continue

            matched = next(
                (
                    c
                    for c in session.conflicts
                    if self._agent_value_set(c.agents) == key
                ),
                None,
            )
            if matched is not None:
                resolution = summary.get("resolution")
                if isinstance(resolution, str) and resolution:
                    matched.resolution = resolution
                continue

            # Judge-reported conflict with no deterministic match — adopt it.
            agents = self._parse_agents(involved)
            if len(agents) < 2:
                continue
            session.conflicts.append(
                Conflict(
                    dimension=str(summary.get("dimension", "")),
                    agents=agents,
                    issue=str(summary.get("issue", "")),
                    resolution=str(summary.get("resolution", "") or ""),
                )
            )

    @staticmethod
    def _agent_value_set(agents: list[AgentType]) -> set[str]:
        """Normalize a conflict's agents to a set of value strings.

        Pydantic's ``use_enum_values`` stores list-of-enum items as plain
        strings (e.g. ``"architect"``) rather than :class:`AgentType` members,
        so reads must tolerate both forms.
        """
        return {str(getattr(agent, "value", agent)) for agent in agents}

    @staticmethod
    def _parse_agents(values: list[object]) -> list[AgentType]:
        """Parse agent value strings into :class:`AgentType` members.

        Unknown values are skipped so a hallucinated agent name can never
        crash the pipeline.

        Args:
            values: Candidate agent identifiers (usually strings).

        Returns:
            The valid :class:`AgentType` members, in input order.
        """
        parsed: list[AgentType] = []
        for value in values:
            try:
                parsed.append(AgentType(str(value)))
            except ValueError:
                continue
        return parsed

    # ── Artifact generation ─────────────────────────────────────────────

    def _generate_artifacts(
        self,
        session: Session,
        turns: dict[AgentType, AgentTurn],
        judge_turn: AgentTurn,
    ) -> list[Artifact]:
        """Build the four output artifacts.

        Always returns four artifacts; a failed source agent yields an
        artifact that says so, so the dashboard always renders a full result
        set. The IaC template is scanned for executable patterns before it is
        stored.

        Args:
            session:    The completed session (for user inputs and conflicts).
            turns:      The four specialist turns.
            judge_turn: The judge's turn.

        Returns:
            Four :class:`Artifact` objects.
        """
        return [
            self._build_iac_artifact(session, turns),
            self._build_cost_artifact(session, turns),
            self._build_compliance_artifact(session, turns),
            self._build_arbitration_artifact(session, judge_turn),
        ]

    def _build_iac_artifact(self, session: Session, turns: dict[AgentType, AgentTurn]) -> Artifact:
        """Render a Bicep template from the architect's design, malware-scanned."""
        arch = self._output_of(turns, AgentType.ARCHITECT)
        if arch is None:
            content = "# Architect output unavailable — IaC template not generated.\n"
        else:
            lines = [
                "// CloudOptima generated architecture — "
                +        self._safe_comment(session.project_name),
                "targetScope = 'resourceGroup'",
                "param location string = resourceGroup().location",
                "",
            ]
            slug = self._slugify(session.project_name) or "app"
            for section in ("compute", "storage", "networking", "data"):
                block = arch.get(section)
                recommendation = (
                    block.get("recommendation", "") if isinstance(block, dict) else ""
                )
                lines.append(f"// ── {section.title()} ──")
                comment = self._safe_comment(recommendation)
                if comment:
                    lines.append(f"// {comment}")
                lines.append(
                    f"resource {section} '{_RESOURCE_TYPES[section]}' = {{"
                )
                lines.append(_RESOURCE_BODIES[section].format(slug=slug))
                lines.append("}")
                lines.append("")
            content = "\n".join(lines)

        matches = scan_for_malware_in_iac(content)
        if matches:
            _logger.warning(
                "IaC artifact withheld — malware patterns detected: %s", matches
            )
            content = (
                "# [BLOCKED] The generated template contained executable patterns "
                "(e.g. exec/eval/os.system) and was withheld.\n"
            )
            description = "IaC template withheld — malware patterns detected"
        else:
            description = _ARTIFACT_DESCRIPTIONS["iac_bicep"]

        return Artifact(
            name="architecture.bicep",
            type="iac_bicep",
            format="bicep",
            content=content,
            description=description,
        )

    def _build_cost_artifact(
        self, session: Session, turns: dict[AgentType, AgentTurn]
    ) -> Artifact:
        """Serialize the cost analyst's estimate as pretty JSON."""
        cost = self._output_of(turns, AgentType.COST_ANALYST)
        if cost is None:
            payload: dict[str, Any] = {"error": "cost analyst output unavailable"}
        else:
            payload = {
                "project": session.project_name,
                "currency": cost.get("currency", "USD"),
                "estimate": cost.get("estimate"),
                "budget": session.budget,
                "budget_status": cost.get("budget_status"),
                "breakdown": cost.get("breakdown", []),
                "savings": cost.get("savings", []),
            }
        content = json.dumps(payload, indent=2, ensure_ascii=False, default=str) + "\n"
        return Artifact(
            name="cost_forecast.json",
            type="cost_forecast",
            format="json",
            content=content,
            description=_ARTIFACT_DESCRIPTIONS["cost_forecast"],
        )

    def _build_compliance_artifact(
        self, session: Session, turns: dict[AgentType, AgentTurn]
    ) -> Artifact:
        """Render the compliance officer's rule-by-rule report as Markdown."""
        compliance = self._output_of(turns, AgentType.COMPLIANCE)
        if compliance is None:
            content = "Compliance report unavailable — compliance turn failed.\n"
        else:
            frameworks = ", ".join(
                str(getattr(framework, "value", framework))
                for framework in session.compliance_frameworks
            ) or "not specified"
            lines = [
                f"# Compliance Report — {self._safe_comment(session.project_name)}",
                "",
                f"Frameworks: {frameworks}",
                f"Overall status: **{self._safe_comment(compliance.get('overall_status', ''))}**",
                "",
                "## Rules",
            ]
            for rule in compliance.get("rules", []):
                if isinstance(rule, dict):
                    status = self._safe_comment(rule.get("status", ""))
                    rid = rule.get("rule_id", "")
                    rname = self._safe_comment(rule.get("rule_name", ""))
                    det = self._safe_comment(rule.get("details", ""))
                    lines.append(f"- [{status}] {rid} {rname}: {det}")
            remediation = compliance.get("remediation_steps", [])
            if remediation:
                lines.append("")
                lines.append("## Remediation steps")
                for index, step in enumerate(remediation, start=1):
                    lines.append(f"{index}. {self._safe_comment(step)}")
            content = "\n".join(lines) + "\n"

        return Artifact(
            name="compliance_report.md",
            type="compliance_report",
            format="markdown",
            content=content,
            description=_ARTIFACT_DESCRIPTIONS["compliance_report"],
        )

    def _build_arbitration_artifact(
        self, session: Session, judge_turn: AgentTurn
    ) -> Artifact:
        """Render the judge's final arbitration as Markdown."""
        output = judge_turn.output
        if "error" in output:
            content = "Arbitration unavailable — judge turn failed.\n"
        else:
            overridden = output.get("overridden_agents", [])
            overridden_text = (
                ", ".join(str(a) for a in overridden) if overridden else "none"
            )
            lines = [
                f"# Arbitration Summary — {self._safe_comment(session.project_name)}",
                "",
                f"Final recommendation: "
                f"{self._safe_comment(output.get('final_recommendation', ''))}",
                f"Overridden agents: "
                f"{self._safe_comment(overridden_text)}",
                "",
                "## Conflicts",
            ]
            if session.conflicts:
                for conflict in session.conflicts:
                    agents = ", ".join(
                        str(getattr(agent, "value", agent))
                        for agent in conflict.agents
                    )
                    resolution = conflict.resolution or "pending arbitration"
                    lines.append(
                        f"- **{conflict.dimension}** ({agents}): "
                        f"{self._safe_comment(conflict.issue)} → {self._safe_comment(resolution)}"
                    )
            else:
                lines.append("- No conflicts detected.")
            content = "\n".join(lines) + "\n"

        return Artifact(
            name="arbitration_summary.md",
            type="arbitration_summary",
            format="markdown",
            content=content,
            description=_ARTIFACT_DESCRIPTIONS["arbitration_summary"],
        )

    # ── Observability ───────────────────────────────────────────────────

    def _log_run_event(
        self,
        session: Session,
        started: float,
        status: str,
        extra: dict[str, Any] | None = None,
    ) -> None:
        """Write an orchestrator run summary to the append-only audit log.

        Observability is best-effort: a logging failure must never break the
        pipeline, so any exception is caught and logged at debug level.
        """
        try:
            event = TraceEvent(
                event_type="orchestrator_run",
                agent_name="Orchestrator",
                latency_ms=round((time.monotonic() - started) * 1000, 2),
                status=status,
                session_id=session.session_id,
                extra={
                    "conflicts": len(session.conflicts),
                    "artifacts": len(session.artifacts),
                    "agent_turns": len(session.agent_turns),
                    **(extra or {}),
                },
            )
            get_audit_logger().log(event)
        except Exception:
            _logger.debug("Failed to log orchestrator run event", exc_info=True)

    # ── Shared helpers ──────────────────────────────────────────────────

    @staticmethod
    def _output_of(
        turns: dict[AgentType, AgentTurn], agent_type: AgentType
    ) -> dict[str, Any] | None:
        """Return a specialist's validated output dict, or ``None`` on failure.

        Turns that carry an ``error`` key (failed agents) return ``None`` so
        detection and artifact logic can skip them gracefully.
        """
        turn = turns.get(agent_type)
        if turn is None or "error" in turn.output:
            return None
        return turn.output

    @staticmethod
    def _safe_comment(text: object) -> str:
        """Flatten arbitrary text into a one-line, HTML-free comment fragment."""
        cleaned = clean_output(text)
        return re.sub(r"\s+", " ", cleaned).strip()[:120]

    @staticmethod
    def _slugify(text: object) -> str:
        """Lowercase alphanumeric slug for use inside Bicep resource names."""
        return re.sub(r"[^a-z0-9]+", "", str(text).lower())[:20]
