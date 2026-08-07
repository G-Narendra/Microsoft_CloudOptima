"""Streamlit dashboard (Phase 7).

The user fills in a form, the orchestrator runs the five-agent pipeline, and
the results land across four tabs (Overview, Agents, Conflicts, Artifacts)
with downloadable artifacts.

Design notes:
- **Progress is real, never faked.** The orchestrator runs on a background
  thread; the main thread polls ``session.agent_turns`` and only moves the
  bar when a turn actually completes.
- **Security first.** Every user value passes through :func:`clean_input` in
  :func:`build_session`; every LLM-produced string through
  :func:`clean_output` before display. ``unsafe_allow_html`` is never used.
- **Testable core.** Pure logic (session building, severity mapping, text
  formatting) lives in module-level functions that never touch Streamlit, so
  they're unit-testable without a Streamlit runtime.

Run with:
    streamlit run cloudoptima/dashboard.py
"""

from __future__ import annotations

import json
import threading
import time
from typing import Any, Final

import pandas as pd
import streamlit as st

from cloudoptima import __version__
from cloudoptima.agents import DISPLAY_NAMES
from cloudoptima.app import create_orchestrator
from cloudoptima.config import Settings
from cloudoptima.health import check_all, overall_status
from cloudoptima.models import (
    AgentTurn,
    AgentType,
    Artifact,
    AzureRegion,
    ComplianceFramework,
    Conflict,
    DeploymentScale,
    Session,
    WorkloadType,
)
from cloudoptima.pricing import extract_services, live_prices
from cloudoptima.sanitize import clean_input, clean_output

# ── Constants ───────────────────────────────────────────────────────────

_START_TIME: Final[float] = time.time()
_PAGE_TITLE: Final[str] = "Microsoft CloudOptima"

# Pipeline order (matches cloudoptima.agents.ALL_AGENTS).
_PIPELINE_TYPES: Final[tuple[AgentType, ...]] = (
    AgentType.ARCHITECT,
    AgentType.COST_ANALYST,
    AgentType.SECURITY,
    AgentType.COMPLIANCE,
    AgentType.JUDGE,
)
_TOTAL_STEPS: Final[int] = len(_PIPELINE_TYPES)

_SEVERITY_LABELS: Final[dict[str, str]] = {
    "high": "🔴 HIGH",
    "medium": "🟡 MEDIUM",
    "resolved": "🟢 RESOLVED",
}

_BUDGET_MIN: Final[int] = 100
_BUDGET_MAX: Final[int] = 100_000
_BUDGET_DEFAULT: Final[int] = 5_000

_PRICING_SOURCE_LABELS: Final[dict[str, str]] = {
    "live": "🟢 Azure Retail API",
    "static": "🟡 Static catalog",
}


# ── Pure helpers (unit-testable, no Streamlit calls) ────────────────────


def _parse_enum(enum_cls: type[Any], value: object, default: Any) -> Any:
    """Parse a raw form value into an enum member, falling back to ``default``."""
    if isinstance(value, enum_cls):
        return value
    try:
        return enum_cls(str(value))
    except ValueError:
        return default


def _parse_frameworks(values: list[str]) -> list[ComplianceFramework]:
    """Map multiselect values to compliance frameworks, dropping unknown ones."""
    parsed: list[ComplianceFramework] = []
    for value in values:
        try:
            parsed.append(ComplianceFramework(str(value)))
        except ValueError:
            continue
    return parsed


def build_session(
    project_name: str,
    workload_type: str,
    scale: str,
    region: str,
    frameworks: list[str],
    budget: float | None,
    services: str,
    context: str,
) -> Session:
    """Build a validated :class:`Session` from raw form values.

    Every user-supplied string is cleaned with :func:`clean_input` first, so
    hostile input (XSS, SQL, null bytes) never reaches the agents or the UI.
    """
    budget_value: float | None = None
    if budget is not None and budget > 0:
        budget_value = float(budget)

    return Session(
        project_name=clean_input(project_name, max_length=120),
        workload_type=_parse_enum(WorkloadType, workload_type, WorkloadType.MIXED),
        scale=_parse_enum(DeploymentScale, scale, DeploymentScale.MEDIUM),
        region=_parse_enum(AzureRegion, region, AzureRegion.UAE_NORTH),
        compliance_frameworks=_parse_frameworks(frameworks),
        budget=budget_value,
        services=clean_input(services),
        user_prompt=clean_input(context),
        status="pending",
    )


def agent_display_name(agent_type: object) -> str:
    """Human-readable label for an agent type (tolerates str or enum)."""
    try:
        key = AgentType(str(agent_type)) if not isinstance(agent_type, AgentType) else agent_type
    except ValueError:
        return str(agent_type)
    return DISPLAY_NAMES.get(key, key.value)


def conflict_severity(conflict: Conflict) -> str:
    """Map a conflict to a severity bucket: ``high``, ``medium``, or ``resolved``.

    Resolved conflicts are green; unresolved ones involving security or
    compliance are high; everything else is medium.
    """
    if conflict.resolution:
        return "resolved"
    dimension = conflict.dimension.lower()
    if "security" in dimension or "compliance" in dimension:
        return "high"
    return "medium"


def format_currency(value: float | int | None) -> str:
    """Format a number as USD, or ``"—"`` when absent."""
    if value is None or isinstance(value, bool):
        return "—"
    try:
        return f"${float(value):,.2f}"
    except (TypeError, ValueError):
        return "—"


def artifact_bytes(artifact: Artifact) -> bytes:
    """UTF-8 bytes of an artifact's content for download buttons."""
    return artifact.content.encode("utf-8")


def live_pricing_rows(session: Session) -> tuple[list[dict[str, Any]], str]:
    """Real Azure Retail Prices rows for the services a design mentions.

    Scans the user's services text plus the architect's validated JSON for
    known Azure services and prices each against the live Retail Prices API
    (static catalog as the offline fallback). Pure — no Streamlit calls, so
    it is unit-testable.

    Args:
        session: A completed (or running) analysis session.

    Returns:
        ``(rows, region)`` where each row is
        ``{"service", "price", "source"}`` and ``region`` is the ARM region
        the prices were fetched for.
    """
    texts: list[str | None] = [session.services, session.user_prompt]
    for turn in session.agent_turns:
        if turn.agent_type == AgentType.ARCHITECT and "error" not in turn.output:
            try:
                texts.append(json.dumps(turn.output))
            except (TypeError, ValueError):  # pragma: no cover - defensive
                texts.append(None)
            break
    names = extract_services(*texts)
    region = str(getattr(session.region, "value", session.region) or "uaenorth")
    return live_prices(names, region), region


def session_status_badge(session: Session) -> str:
    """A color-coded status badge for a session."""
    return {
        "pending": ":blue[PENDING]",
        "running": ":orange[RUNNING]",
        "completed": ":green[COMPLETED]",
        "failed": ":red[FAILED]",
    }.get(session.status, session.status)


def build_agent_markdown(turn: AgentTurn) -> str:
    """Render an agent's structured output as safe Markdown text.

    All model-produced strings are passed through :func:`clean_output` so
    injected HTML renders as inert text.
    """
    output = turn.output
    if "error" in output:
        return clean_output(str(output.get("error")))

    lines: list[str] = []
    for key, value in output.items():
        if isinstance(value, dict):
            lines.append(f"**{key}**")
            for sub_key, sub_value in value.items():
                lines.append(f"- *{sub_key}*: {clean_output(str(sub_value))}")
        elif isinstance(value, list):
            lines.append(f"**{key}**")
            for item in value:
                if isinstance(item, dict):
                    parts = ", ".join(f"{k}: {clean_output(str(v))}" for k, v in item.items())
                    lines.append(f"- {parts}")
                else:
                    lines.append(f"- {clean_output(str(item))}")
        else:
            lines.append(f"**{key}**: {clean_output(str(value))}")
    return "\n\n".join(lines)


def _uptime() -> str:
    """Human-readable uptime since the dashboard module was imported."""
    elapsed = int(time.time() - _START_TIME)
    minutes, seconds = divmod(elapsed, 60)
    hours, minutes = divmod(minutes, 60)
    if hours:
        return f"{hours}h {minutes}m {seconds}s"
    if minutes:
        return f"{minutes}m {seconds}s"
    return f"{seconds}s"


def _total_latency_ms(session: Session) -> float:
    """Sum of all agent turn latencies, in milliseconds."""
    return sum(turn.latency_ms for turn in session.agent_turns)


# ── Streamlit UI ────────────────────────────────────────────────────────


def _init_state() -> None:
    st.session_state.setdefault("orchestrator", None)
    st.session_state.setdefault("orchestrator_key", None)
    st.session_state.setdefault("demo_mode", True)
    st.session_state.setdefault("current_session", None)
    st.session_state.setdefault("session_history", [])
    st.session_state.setdefault("running", False)
    st.session_state.setdefault("thread", None)


def _ensure_orchestrator() -> None:
    """Build (or rebuild) the orchestrator for the current demo-mode setting."""
    provider_key = "mock" if st.session_state.demo_mode else "live"
    if st.session_state.orchestrator is None or st.session_state.orchestrator_key != provider_key:
        settings = Settings(llm_provider="mock") if st.session_state.demo_mode else Settings()
        st.session_state.orchestrator = create_orchestrator(settings)
        st.session_state.orchestrator_key = provider_key


def _render_sidebar() -> None:
    with st.sidebar:
        st.title("☁️ CloudOptima")
        st.caption("Multi-agent cloud architecture designer")

        demo_mode = st.toggle(
            "Demo mode (mock data)",
            value=st.session_state.demo_mode,
            help="Uses the Mock LLM client — no API keys, instant results.",
        )
        if demo_mode != st.session_state.demo_mode:
            st.session_state.demo_mode = demo_mode
            st.session_state.orchestrator = None  # rebuild on next rerun

        st.divider()

        st.subheader("Past sessions")
        history = st.session_state.session_history
        if history:
            options = {s.session_id: s.project_name for s in history}
            selected_id = st.selectbox(
                "Load an analysis",
                options=list(options),
                format_func=lambda sid: options[sid],
                label_visibility="collapsed",
            )
            if st.button("Load", use_container_width=True):
                st.session_state.current_session = next(
                    s for s in history if s.session_id == selected_id
                )
                st.rerun()
        else:
            st.caption("No analyses yet — run one and it appears here.")

        st.divider()

        st.subheader("System status")
        st.write(f"Version **{__version__}**")
        st.write(f"Uptime **{_uptime()}**")
        status = overall_status(check_all())
        label = {
            "healthy": ":green[● healthy]",
            "degraded": ":orange[● degraded]",
            "unhealthy": ":red[● unhealthy]",
        }[status]
        st.write(label)
        st.caption(f"Provider: **{st.session_state.orchestrator_key}**")


def _render_input_form() -> None:
    """The analysis input form; returns the built session on submit."""
    with st.form("analysis_form"):
        st.subheader("Describe your infrastructure")
        col1, col2 = st.columns(2)
        with col1:
            project_name = st.text_input("Project name", placeholder="e.g. E-Shop UAE")
            workload_type = st.selectbox(
                "Workload type",
                options=[w.value for w in WorkloadType],
                index=3,  # MIXED
            )
            scale = st.selectbox(
                "Deployment scale",
                options=[d.value for d in DeploymentScale],
                index=1,  # MEDIUM
            )
            region = st.selectbox(
                "Azure region",
                options=[r.value for r in AzureRegion],
                index=0,  # UAE North
            )
        with col2:
            frameworks = st.multiselect(
                "Compliance frameworks",
                options=[f.value for f in ComplianceFramework],
                default=["pdpl"],
            )
            budget = st.number_input(
                "Monthly budget (USD)",
                min_value=0,
                max_value=_BUDGET_MAX,
                value=_BUDGET_DEFAULT,
                step=100,
                help=f"Between ${_BUDGET_MIN:,} and ${_BUDGET_MAX:,}; 0 = no budget cap.",
            )
            services = st.text_area(
                "Services & stack",
                placeholder="e.g. Web app (React), REST API, PostgreSQL, Redis, Blob storage",
                height=90,
            )
            context = st.text_area(
                "Requirements & context",
                placeholder=(
                    "e.g. Serve 50k users in the UAE, needs to scale "
                    "for Ramadan peak, multi-AZ for HA"
                ),
                height=90,
            )

        submitted = st.form_submit_button(
            "🚀 Analyze", use_container_width=True, disabled=st.session_state.running
        )
        if submitted:
            st.session_state.current_session = build_session(
                project_name=project_name,
                workload_type=workload_type,
                scale=scale,
                region=region,
                frameworks=frameworks,
                budget=budget,
                services=services,
                context=context,
            )
            st.session_state.thread = threading.Thread(
                target=st.session_state.orchestrator.run,
                args=(st.session_state.current_session,),
                daemon=True,
            )
            st.session_state.running = True
            st.session_state.thread.start()


def _render_progress() -> None:
    """Poll the running pipeline and update the progress bar as turns complete."""
    session = st.session_state.current_session
    bar = st.progress(0.0, text="Starting the five-agent pipeline…")
    status_box = st.empty()

    thread = st.session_state.thread
    while thread is not None and thread.is_alive():
        completed = len(session.agent_turns)
        fraction = min(completed / _TOTAL_STEPS, 1.0)
        bar.progress(fraction)
        if completed < len(_PIPELINE_TYPES):
            name = agent_display_name(_PIPELINE_TYPES[min(completed, len(_PIPELINE_TYPES) - 1)])
            status_box.info(f"Running **{name}**…")
        else:
            status_box.info("Resolving conflicts and generating artifacts…")
        time.sleep(0.05)

    # Thread finished — refresh the bar to full and show the outcome.
    completed = len(session.agent_turns)
    bar.progress(min(completed / _TOTAL_STEPS, 1.0))
    if session.status == "completed":
        status_box.success(f"Analysis complete in {_total_latency_ms(session):,.0f} ms.")
    else:
        message = session.error_message or (
            "Analysis failed or was interrupted — see the Agents tab."
        )
        status_box.error(clean_output(message))

    st.session_state.running = False
    st.session_state.thread = None

    # Remember this session in the sidebar history.
    history = st.session_state.session_history
    if not any(s.session_id == session.session_id for s in history):
        history.append(session)


# ── Result tabs ─────────────────────────────────────────────────────────


def _render_overview_tab(session: Session) -> None:
    st.subheader("Overview")

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total time", f"{_total_latency_ms(session):,.0f} ms")
    k2.metric("Agent turns", len(session.agent_turns))
    k3.metric("Conflicts", len(session.conflicts))
    k4.metric("Artifacts", len(session.artifacts))
    st.write(f"Status: {session_status_badge(session)}")
    st.write(f"Budget: **{format_currency(session.budget)}**")

    _render_live_pricing(session)

    st.markdown("### Latency per agent (ms)")
    if session.agent_turns:
        chart = pd.DataFrame(
            {
                "latency_ms": [turn.latency_ms for turn in session.agent_turns],
            },
            index=[agent_display_name(turn.agent_type) for turn in session.agent_turns],
        )
        st.bar_chart(chart)

    judge = next((t for t in session.agent_turns if t.agent_type == AgentType.JUDGE), None)
    if judge is not None and "error" not in judge.output:
        st.markdown("### Judge summary")
        st.write(
            "**Final recommendation:** "
            f"{clean_output(str(judge.output.get('final_recommendation', '')))}"
        )
        overridden = judge.output.get("overridden_agents", [])
        overridden_text = ", ".join(str(a) for a in overridden) if overridden else "none"
        st.write(f"**Overridden agents:** {overridden_text}")


def _render_live_pricing(session: Session) -> None:
    """Render the live Azure Retail Prices panel in the Overview tab."""
    st.markdown("### 💵 Live Azure pricing")
    rows, region = live_pricing_rows(session)
    if not rows:
        st.caption(
            f"No Azure services matched in the design (region {region}) — "
            "nothing to price."
        )
        return
    frame = pd.DataFrame(rows)
    frame["price"] = frame["price"].map(lambda p: f"${float(p):,.2f}")
    frame = frame.rename(
        columns={
            "service": "Service",
            "price": "List price (USD)",
            "unit": "Unit",
            "source": "Source",
        }
    )
    frame["Source"] = frame["Source"].map(_PRICING_SOURCE_LABELS)
    st.dataframe(frame, use_container_width=True, hide_index=True)
    st.caption(
        "Real list prices from the Azure Retail Prices API (free, no auth, "
        "cached 1 hour) — the unit varies by service (per hour, per GB-Mo, "
        "per month). The static catalog appears only when a service is "
        "missing or the API is offline."
    )


def _render_agents_tab(session: Session) -> None:
    st.subheader("Agent reports")
    if not session.agent_turns:
        st.info("No agent output yet.")
        return

    for turn in session.agent_turns:
        with st.expander(
            f"{agent_display_name(turn.agent_type)} — "
            f"{turn.latency_ms:,.0f} ms · {turn.tokens_used} tokens",
            expanded=False,
        ):
            st.markdown(build_agent_markdown(turn))
            if st.checkbox(
                "Show raw JSON",
                key=f"raw_{turn.agent_type}_{turn.timestamp}",
            ):
                st.json(turn.output)


def _render_conflicts_tab(session: Session) -> None:
    st.subheader("Conflicts")
    if not session.conflicts:
        st.success("No conflicts detected between the agents.")
        return

    for conflict in session.conflicts:
        severity = conflict_severity(conflict)
        agents = ", ".join(agent_display_name(a) for a in conflict.agents)
        st.markdown(f"**{_SEVERITY_LABELS[severity]}** · `{conflict.dimension}` · {agents}")
        st.write(f"**Issue:** {clean_output(conflict.issue)}")
        resolution = (
            clean_output(conflict.resolution) if conflict.resolution else "*pending arbitration*"
        )
        st.write(f"**Resolution:** {resolution}")
        st.divider()


def _render_artifacts_tab(session: Session) -> None:
    st.subheader("Generated artifacts")
    if not session.artifacts:
        st.info("No artifacts generated.")
        return

    languages = {"bicep": "bicep", "json": "json", "markdown": "markdown"}
    for artifact in session.artifacts:
        st.markdown(f"### {artifact.name}")
        st.caption(clean_output(artifact.description))
        st.download_button(
            f"⬇️ Download {artifact.name}",
            data=artifact_bytes(artifact),
            file_name=artifact.name,
            mime="text/plain",
            key=f"download_{artifact.artifact_id}",
        )
        with st.expander("Preview", expanded=artifact.type == "iac_bicep"):
            st.code(
                artifact.content,
                language=languages.get(artifact.format, "text"),
            )


def _render_results(session: Session) -> None:
    st.title("Analysis results")
    st.caption(f"Project: **{clean_output(session.project_name)}**")

    tab_overview, tab_agents, tab_conflicts, tab_artifacts = st.tabs(
        ["Overview", "Agents", "Conflicts", "Artifacts"]
    )
    with tab_overview:
        _render_overview_tab(session)
    with tab_agents:
        _render_agents_tab(session)
    with tab_conflicts:
        _render_conflicts_tab(session)
    with tab_artifacts:
        _render_artifacts_tab(session)


# ── Entry point ─────────────────────────────────────────────────────────


def main() -> None:
    """Render the full dashboard page."""
    st.set_page_config(
        page_title=_PAGE_TITLE,
        page_icon="☁️",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    _init_state()
    _ensure_orchestrator()
    _render_sidebar()

    if not st.session_state.running:
        _render_input_form()
    if st.session_state.running:
        _render_progress()

    current = st.session_state.current_session
    if current is not None and not st.session_state.running:
        _render_results(current)


if __name__ == "__main__":
    main()
