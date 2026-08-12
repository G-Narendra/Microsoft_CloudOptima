"""Tests for the Orchestrator pipeline and app entry point (Phase 6).

Covers the checklist 6.3 scenarios — full pipeline, ≥1 conflict with mock
data, 4 artifacts, broken-agent resilience, and re-run determinism — plus the
budget-pair conflict, judge resolution folding, IaC malware scanning, and the
stdin→stdout CLI.
"""

from __future__ import annotations

import asyncio
import io
import json
from typing import Any

import pytest

from cloudoptima import app
from cloudoptima.agent_base import BaseAgent
from cloudoptima.agents import ALL_AGENTS
from cloudoptima.agents.architect import ArchitectAgent
from cloudoptima.agents.compliance import ComplianceOfficerAgent
from cloudoptima.agents.cost_analyst import CostAnalystAgent
from cloudoptima.agents.judge import JudgeAgent
from cloudoptima.agents.security import SecurityEngineerAgent
from cloudoptima.config import Settings
from cloudoptima.llm_client import MockClient
from cloudoptima.models import AgentTurn, AgentType, Session
from cloudoptima.orchestrator import Orchestrator
from cloudoptima.sanitize import reset_rate_limits


@pytest.fixture(autouse=True)
def _reset_global_rate_limits() -> None:
    """The orchestrator's global hourly limiter is process-wide; isolate tests."""
    reset_rate_limits()


# ── Test doubles ───────────────────────────────────────────────────────


class _StubAgent(BaseAgent):
    """Returns a fixed AgentTurn without calling any LLM."""

    system_prompt = "stub agent"

    def __init__(self, agent_type: AgentType, turn: AgentTurn) -> None:
        super().__init__(agent_type, MockClient(), Settings())
        self._turn = turn

    def _build_prompt(self, session: Session) -> str:  # pragma: no cover - stub
        return "stub"

    def _validate_output(self, data: dict[str, Any]) -> tuple[bool, str]:  # pragma: no cover - stub
        return True, ""

    async def analyze(self, session: Session) -> AgentTurn:  # noqa: ARG002 - stub
        return self._turn


def _error_turn(agent_type: AgentType) -> AgentTurn:
    return AgentTurn(agent_type=agent_type, output={"error": "simulated failure"})


def _malicious_architect_turn() -> AgentTurn:
    """Architect output whose recommendation smuggles executable code."""
    return AgentTurn(
        agent_type=AgentType.ARCHITECT,
        output={
            "compute": {
                "recommendation": "Run exec('rm -rf /') on the cluster",
                "justification": "x",
                "alternatives": [],
            },
            "storage": {"recommendation": "Blob", "justification": "x", "alternatives": []},
            "networking": {"recommendation": "VNet", "justification": "x", "alternatives": []},
            "data": {"recommendation": "SQL", "justification": "x", "alternatives": []},
        },
    )


# ── Fixtures / helpers ─────────────────────────────────────────────────


def _make_session(**overrides: Any) -> Session:
    defaults: dict[str, Any] = {
        "project_name": "Demo Project",
        "user_prompt": "Build a scalable web app on Azure",
    }
    defaults.update(overrides)
    return Session(**defaults)


def _real_orchestrator() -> Orchestrator:
    """Orchestrator with all five real agents over MockClient (demo mode)."""
    return Orchestrator.from_settings(Settings())


def _orchestrator_with(
    overrides: dict[AgentType, BaseAgent] | None = None,
) -> Orchestrator:
    """Orchestrator with real agents except any listed in ``overrides``."""
    settings = Settings()
    llm = MockClient()
    agents: dict[AgentType, BaseAgent] = {
        AgentType.ARCHITECT: ArchitectAgent(AgentType.ARCHITECT, llm, settings),
        AgentType.COST_ANALYST: CostAnalystAgent(AgentType.COST_ANALYST, llm, settings),
        AgentType.SECURITY: SecurityEngineerAgent(AgentType.SECURITY, llm, settings),
        AgentType.COMPLIANCE: ComplianceOfficerAgent(AgentType.COMPLIANCE, llm, settings),
        AgentType.JUDGE: JudgeAgent(AgentType.JUDGE, llm, settings),
    }
    if overrides:
        agents.update(overrides)
    return Orchestrator(agents=agents, config=settings)


# ── Checklist 6.3 — core scenarios ─────────────────────────────────────


def test_full_pipeline_completes_without_errors() -> None:
    """The whole pipeline runs and returns a completed session."""
    session = asyncio.run(_real_orchestrator().run(_make_session()))

    assert session.status == "completed"
    assert len(session.agent_turns) == 5  # 4 specialists + judge
    assert all("error" not in turn.output for turn in session.agent_turns)
    # Pipeline order preserved: judge always last.
    assert session.agent_turns[-1].agent_type == AgentType.JUDGE


def test_at_least_one_conflict_found_with_mock_data() -> None:
    """Mock data (compliance NEEDS_WORK + judge summaries) yields conflicts."""
    session = asyncio.run(_real_orchestrator().run(_make_session()))

    assert len(session.conflicts) >= 1
    dimensions = [c.dimension for c in session.conflicts]
    assert "architect_vs_compliance" in dimensions


def test_four_artifacts_generated() -> None:
    """Exactly the four expected artifacts are produced."""
    session = asyncio.run(_real_orchestrator().run(_make_session()))

    assert len(session.artifacts) == 4
    assert {a.type for a in session.artifacts} == {
        "iac_bicep",
        "cost_forecast",
        "compliance_report",
        "arbitration_summary",
    }
    assert all(a.name and a.content for a in session.artifacts)


def test_broken_agent_does_not_crash_pipeline() -> None:
    """A failed specialist is recorded as an error turn; the run continues."""
    broken = _StubAgent(AgentType.ARCHITECT, _error_turn(AgentType.ARCHITECT))
    session = asyncio.run(
        _orchestrator_with({AgentType.ARCHITECT: broken}).run(_make_session())
    )

    assert session.status == "completed"
    architect_turn = next(
        t for t in session.agent_turns if t.agent_type == AgentType.ARCHITECT
    )
    assert "error" in architect_turn.output
    # The other agents still ran and the full artifact set is present.
    assert len(session.agent_turns) == 5
    assert len(session.artifacts) == 4


def test_same_session_twice_has_same_conflict_count() -> None:
    """Re-running a session is deterministic — identical conflict results."""
    orch = _real_orchestrator()
    session = _make_session()

    first = asyncio.run(orch.run(session))
    first_count = len(first.conflicts)
    first_dimensions = [c.dimension for c in first.conflicts]

    second = asyncio.run(orch.run(session))  # same object — outputs are reset each run
    assert len(second.conflicts) == first_count
    assert [c.dimension for c in second.conflicts] == first_dimensions
    assert len(second.agent_turns) == len(first.agent_turns)


# ── Conflict detection specifics ───────────────────────────────────────


def test_budget_overrun_detected_as_architect_vs_cost() -> None:
    """An estimate above the budget fires the budget pair conflict."""
    session = asyncio.run(_real_orchestrator().run(_make_session(budget=1000.0)))

    dimensions = [c.dimension for c in session.conflicts]
    assert "architect_vs_cost" in dimensions
    budget_conflict = next(c for c in session.conflicts if c.dimension == "architect_vs_cost")
    assert "1,000" in budget_conflict.issue


def test_no_budget_no_budget_conflict() -> None:
    """Without a budget the deterministic budget detector cannot fire."""
    session = asyncio.run(_real_orchestrator().run(_make_session(budget=None)))

    dimensions = [c.dimension for c in session.conflicts]
    assert "architect_vs_cost" not in dimensions
    # NOTE: cost_vs_security may still appear because the mock judge's
    # arbitration always includes this summary (adopted into conflicts).


def test_judge_resolutions_applied_to_detected_conflicts() -> None:
    """Detected conflicts get resolutions folded in from the judge's summaries."""
    session = asyncio.run(_real_orchestrator().run(_make_session()))

    compliance_conflict = next(
        c for c in session.conflicts if c.dimension == "architect_vs_compliance"
    )
    assert compliance_conflict.resolution  # filled by the judge


def test_judge_reported_conflicts_are_adopted() -> None:
    """Conflicts the deterministic detector missed are adopted from the judge."""
    session = asyncio.run(_real_orchestrator().run(_make_session()))

    dimensions = [c.dimension for c in session.conflicts]
    # Mock judge reports cost_vs_security; the deterministic detector does not
    # fire it without a budget — the judge's summary should still appear.
    assert "cost_vs_security" in dimensions


# ── Artifact safety ────────────────────────────────────────────────────


def test_iac_artifact_scanned_for_malware() -> None:
    """Executable patterns in the design block the IaC artifact."""
    malicious = _StubAgent(AgentType.ARCHITECT, _malicious_architect_turn())
    session = asyncio.run(
        _orchestrator_with({AgentType.ARCHITECT: malicious}).run(_make_session())
    )

    iac = next(a for a in session.artifacts if a.type == "iac_bicep")
    assert "exec(" not in iac.content
    assert "BLOCKED" in iac.content
    assert "malware" in iac.description


def test_iac_artifact_rendered_from_clean_design() -> None:
    """A clean design produces a real Bicep template with all four sections."""
    session = asyncio.run(_real_orchestrator().run(_make_session(project_name="E-Shop")))

    iac = next(a for a in session.artifacts if a.type == "iac_bicep")
    assert "targetScope = 'resourceGroup'" in iac.content
    for section in ("compute", "storage", "networking", "data"):
        assert f"// ── {section.title()} ──" in iac.content
    assert "Microsoft.ContainerService" in iac.content


# ── Resilience ─────────────────────────────────────────────────────────


def test_unexpected_agent_exception_marks_session_failed() -> None:
    """An exception escaping an agent marks the session failed, not a crash."""

    class _RaisingAgent(_StubAgent):
        async def analyze(self, session: Session) -> AgentTurn:  # noqa: ARG002
            raise RuntimeError("boom")

    session = asyncio.run(
        _orchestrator_with(
            {AgentType.JUDGE: _RaisingAgent(AgentType.JUDGE, _error_turn(AgentType.JUDGE))}
        ).run(_make_session())
    )

    assert session.status == "failed"


def test_missing_agent_role_rejected() -> None:
    """An orchestrator missing an agent role is rejected at construction."""
    agents: dict[AgentType, BaseAgent] = {
        AgentType.ARCHITECT: ArchitectAgent(AgentType.ARCHITECT, MockClient(), Settings())
    }
    try:
        Orchestrator(agents=agents, config=Settings())
    except ValueError as exc:
        assert "missing" in str(exc)
    else:  # pragma: no cover - the guard must raise
        raise AssertionError("expected ValueError for missing agents")


# ── Factory + app entry point ──────────────────────────────────────────


def test_from_settings_builds_all_five_agents() -> None:
    """from_settings wires every pipeline role in order."""
    orch = Orchestrator.from_settings(Settings())

    assert set(orch.agents.keys()) == set(AgentType)
    # Pipeline order matches AgentType definition order (judge last).
    assert list(orch.agents.keys()) == list(AgentType)
    for agent, expected_cls in zip(orch.agents.values(), ALL_AGENTS, strict=True):
        assert isinstance(agent, expected_cls)


def test_create_orchestrator_returns_ready_orchestrator() -> None:
    """app.create_orchestrator wires a runnable pipeline."""
    orch = app.create_orchestrator(Settings())
    session = asyncio.run(orch.run(_make_session()))

    assert session.status == "completed"
    assert len(session.artifacts) == 4


def test_cli_main_runs_pipeline_from_stdin(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """A valid session JSON on stdin produces the completed session on stdout."""
    payload = json.dumps(
        {"project_name": "CLI App", "user_prompt": "Design a batch pipeline"}
    )
    monkeypatch.setattr("sys.stdin", io.StringIO(payload))

    exit_code = app.main()

    captured = capsys.readouterr()
    assert exit_code == 0
    result = json.loads(captured.out)
    assert result["status"] == "completed"
    assert len(result["artifacts"]) == 4
    assert captured.err == ""


def test_cli_main_rejects_invalid_json(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Malformed JSON on stdin exits with code 2 and a message."""
    monkeypatch.setattr("sys.stdin", io.StringIO("{not json"))

    exit_code = app.main()

    captured = capsys.readouterr()
    assert exit_code == 2
    assert "not valid JSON" in captured.err


def test_cli_main_rejects_missing_required_field(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """A session without project_name fails validation with exit code 2."""
    monkeypatch.setattr("sys.stdin", io.StringIO('{"user_prompt": "hi"}'))

    exit_code = app.main()

    captured = capsys.readouterr()
    assert exit_code == 2
    assert "invalid session" in captured.err
