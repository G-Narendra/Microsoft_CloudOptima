"""Streamlit dashboard (Phase 7)."""

from __future__ import annotations

import asyncio
import json
import os
import queue
import threading
import time
from typing import Any, Final

import pandas as pd
import streamlit as st

from cloudoptima import __version__
from cloudoptima.agents import DISPLAY_NAMES
from cloudoptima.app import create_orchestrator
from cloudoptima.auth import authenticate, can_approve, can_deploy
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
from cloudoptima.safety import moderate_input_fields
from cloudoptima.sanitize import clean_input, clean_output

# Constants

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


# Pure helpers (unit-testable, no Streamlit calls)


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
    settings: Settings | None = None,
) -> Session:
    """Build a validated :class:`Session` from raw form values.

    Every user-supplied string is cleaned with :func:`clean_input` first, so
    hostile input (XSS, SQL, null bytes) never reaches the agents or the UI.
    When ``settings`` has Azure AI Content Safety enabled (issue #2), the
    cleaned fields are additionally moderated and blocked values are blanked.
    """
    budget_value: float | None = None
    if budget is not None and budget > 0:
        budget_value = float(budget)

    cleaned: dict[str, str] = {
        "project_name": clean_input(project_name, max_length=120),
        "services": clean_input(services),
        "user_prompt": clean_input(context),
    }
    if settings is not None:
        cleaned, _blocked = moderate_input_fields(cleaned, settings)

    return Session(
        project_name=cleaned["project_name"],
        workload_type=_parse_enum(WorkloadType, workload_type, WorkloadType.MIXED),
        scale=_parse_enum(DeploymentScale, scale, DeploymentScale.MEDIUM),
        region=_parse_enum(AzureRegion, region, AzureRegion.UAE_NORTH),
        compliance_frameworks=_parse_frameworks(frameworks),
        budget=budget_value,
        services=cleaned["services"],
        user_prompt=cleaned["user_prompt"],
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
        "pending_approval": ":orange[PENDING APPROVAL]",
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


# Streamlit UI


def _init_state() -> None:
    # Read DEMO_MODE from environment — don't default to True when the user
    # has set DEMO_MODE=false in their .env. Streamlit loads .env via Settings.
    env_demo = os.environ.get("DEMO_MODE", "false").lower() in ("1", "true", "yes")
    st.session_state.setdefault("orchestrator", None)
    st.session_state.setdefault("orchestrator_key", None)
    st.session_state.setdefault("demo_mode", env_demo)
    st.session_state.setdefault("current_session", None)
    st.session_state.setdefault("session_history", [])
    st.session_state.setdefault("running", False)
    st.session_state.setdefault("thread", None)
    # Dev auto-login: when DEBUG=true, skip login screen and log in as admin.
    debug_mode = os.environ.get("DEBUG", "false").lower() in ("1", "true", "yes")
    if debug_mode and "role" not in st.session_state:
        st.session_state.role = "admin"
        st.session_state.username = "dev-auto-login"


def _ensure_orchestrator() -> None:
    """Build (or rebuild) the orchestrator for the current demo-mode setting."""
    provider_key = "mock" if st.session_state.demo_mode else "live"
    if st.session_state.orchestrator is None or st.session_state.orchestrator_key != provider_key:
        settings = Settings(llm_provider="mock") if st.session_state.demo_mode else Settings()
        st.session_state.orchestrator = create_orchestrator(settings)
        st.session_state.orchestrator_key = provider_key


@st.cache_data(ttl=30)
def _get_health_status() -> str:
    """Cached health check — runs at most every 30 seconds to avoid render lag."""
    return overall_status(check_all())


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
            if st.button("Load", width="stretch"):
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
        status = _get_health_status()
        label = {
            "healthy": ":green[● healthy]",
            "degraded": ":orange[● degraded]",
            "unhealthy": ":red[● unhealthy]",
        }[status]
        st.write(label)
        st.caption(f"Provider: **{st.session_state.orchestrator_key}**")
        # Show logged-in user
        username = st.session_state.get("username", "")
        role = st.session_state.get("role", "")
        if username:
            st.caption(f"👤 **{username}** ({role})")



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

        is_viewer = st.session_state.get("role") == "viewer"
        submitted = st.form_submit_button(
            "🚀 Analyze", width="stretch", disabled=st.session_state.running or is_viewer
        )
        if is_viewer:
            st.caption("🔒 Viewers cannot run new analyses.")
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
                settings=st.session_state.orchestrator.config,
            )
            session = st.session_state.current_session
            orchestrator = st.session_state.orchestrator
            
            if os.environ.get("LLM_PROVIDER") == "mock":
                # In tests, run synchronously to avoid AppTest thread hangs
                session = asyncio.run(orchestrator.run(session))
                st.session_state.current_session = session
                
                # Remember this session in the sidebar history
                history = st.session_state.session_history
                if not any(s.session_id == session.session_id for s in history):
                    history.append(session)
                    
                st.session_state.running = False
                st.rerun()
            else:
                q = queue.Queue()
                st.session_state.token_queue = q
                
                def stream_callback(agent_type, chunk):
                    q.put(chunk)
                    
                session.on_token = stream_callback
                
                def background_task() -> None:
                    try:
                        asyncio.run(orchestrator.run(session))
                    finally:
                        q.put(None)
                
                st.session_state.running = True
                st.session_state.thread = threading.Thread(
                    target=background_task,
                    daemon=True,
                )
                st.session_state.thread.start()
                st.rerun()


def _render_progress() -> None:
    """Stream tokens to the UI while the background thread runs."""
    session = st.session_state.current_session
    if "token_queue" in st.session_state:
        q = st.session_state.token_queue

        def token_generator():
            while True:
                try:
                    token = q.get(timeout=60)  # 60s max wait per token
                except Exception:
                    break
                if token is None:
                    break
                yield token

        st.markdown("### ⚙️ Pipeline Execution Stream")
        st.write_stream(token_generator())
        # Stream is done — clean up queue and re-read session state
        del st.session_state["token_queue"]
    else:
        with st.spinner("Running analysis..."):
            thread = st.session_state.get("thread")
            if thread:
                thread.join(timeout=300)

    # Re-read from session_state — the background thread updates the session in-place
    session = st.session_state.current_session
    if session.status == "completed":
        st.success(f"✅ Analysis complete in {_total_latency_ms(session):,.0f} ms.")
    elif session.status == "pending_approval":
        st.warning(
            f"✋ Analysis finished in {_total_latency_ms(session):,.0f} ms. "
            "Design is pending HITL approval."
        )
    else:
        message = getattr(session, "error_message", None) or (
            "Analysis failed or was interrupted — check Azure OpenAI credentials."
        )
        st.error(clean_output(message))

    st.session_state.running = False
    st.session_state.thread = None

    # Save to sidebar history
    history = st.session_state.session_history
    if not any(s.session_id == session.session_id for s in history):
        history.append(session)

    # Trigger a rerun so the results tabs appear immediately
    st.rerun()


# Result tabs


def _render_overview_tab(session: Session) -> None:
    st.subheader("Overview")

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total time", f"{_total_latency_ms(session):,.0f} ms")
    k2.metric("Agent turns", len(session.agent_turns))
    k3.metric("Conflicts", len(session.conflicts))
    k4.metric("Artifacts", len(session.artifacts))
    st.write(f"Status: {session_status_badge(session)}")
    st.write(f"Budget: **{format_currency(session.budget)}**")

    if session.status == "pending_approval":
        st.warning("This design is pending Human-in-the-Loop (HITL) approval before artifacts are generated.")
        role = st.session_state.get("role", "viewer")
        if role == "admin":
            if st.button("Approve Design & Generate Artifacts", type="primary"):
                orchestrator = st.session_state.orchestrator
                # Run the resume coroutine in a background thread or synchronously
                session = asyncio.run(orchestrator.resume_approval(session))
                st.session_state.current_session = session
                st.rerun()
        else:
            st.info("You do not have the Admin role required to approve this design.")

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
    
    if session.status == "pending_approval":
        st.warning("Architecture design is complete. Pending Human-in-the-Loop (HITL) review.")
        role = st.session_state.get("role", "")
        if can_approve(role):
            st.info(f"You are logged in as **{role}**. You can approve this design to generate artifacts.")
            if st.button("Approve Architecture & Generate Artifacts", type="primary"):
                orchestrator = st.session_state.orchestrator
                orchestrator.approve_session(session)
                st.rerun()
        else:
            st.info(f"You are logged in as **{role}**. You do not have permission to approve deployments. Waiting for a reviewer or admin.")
        return
        
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


# Entry point


def _render_auth_gate(settings: Settings) -> None:
    """Renders either an OIDC gate or a local mock login screen."""
    if not settings.auth_enabled:
        # Local mock RBAC login
        if "role" not in st.session_state:
            st.session_state.role = None

        if st.session_state.role is not None:
            return

        st.title("☁️ CloudOptima (Local Dev)")
        st.info("Log in with a mock account (viewer, reviewer, admin).")
        
        with st.form("mock_login"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Sign In")
            
            if submit:
                profile = authenticate(username, password)
                if profile:
                    st.session_state.role = profile["role"]
                    st.session_state.username = profile["username"]
                    st.rerun()
                else:
                    st.error("Invalid credentials.")
        st.stop()

    if hasattr(st, "user") and st.user.is_logged_in:
        groups = st.user.get("groups", [])
        if "ArchitectsGroup" in groups or "AdminGroup" in groups:
            st.session_state.role = "admin"
        elif "ReviewersGroup" in groups:
            st.session_state.role = "reviewer"
        else:
            st.session_state.role = "viewer"
        return
        
    st.title("☁️ CloudOptima")
    st.warning("This dashboard requires a Microsoft account to continue.")
    if hasattr(st, "login"):
        st.button("Sign in with Microsoft", on_click=st.login)
    else:
        st.error("Streamlit native Auth API missing.")
    st.stop()



def main() -> None:
    """Render the full dashboard page."""
    st.set_page_config(
        page_title=_PAGE_TITLE,
        page_icon="☁️",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Phase 7 (Security): Inject Content Security Policy via meta tag
    # Prevents XSS execution even if HTML is somehow rendered in the UI
    st.markdown(
        """
        <meta http-equiv="Content-Security-Policy" 
              content="default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:;">
        """,
        unsafe_allow_html=True
    )

    _init_state()
    _ensure_orchestrator()
    _render_auth_gate(st.session_state.orchestrator.config)
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
