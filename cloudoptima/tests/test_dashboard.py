"""Phase 7 dashboard tests — pure helpers and Streamlit AppTest integration."""

from __future__ import annotations

from pathlib import Path

from streamlit.testing.v1 import AppTest

from cloudoptima.dashboard import (
    agent_display_name,
    artifact_bytes,
    build_agent_markdown,
    build_session,
    conflict_severity,
    format_currency,
    session_status_badge,
)
from cloudoptima.models import (
    AgentTurn,
    AgentType,
    Artifact,
    Conflict,
    Session,
    WorkloadType,
)

_DASHBOARD_PATH = Path(__file__).resolve().parents[1] / "dashboard.py"

# ── build_session ───────────────────────────────────────────────────────


class TestBuildSession:
    def test_cleans_all_user_input(self) -> None:
        session = build_session(
            project_name="<script>alert(1)</script>MyApp",
            workload_type="realtime",
            scale="medium",
            region="uaenorth",
            frameworks=["pdpl", "gdpr"],
            budget=5000,
            services="Web App; Azure SQL",
            context="Design  a  scalable app\x00 for the UAE",
        )
        assert "<script>" not in session.project_name
        assert session.project_name == "MyApp"
        assert "\x00" not in session.user_prompt
        assert session.workload_type == WorkloadType.REALTIME
        assert session.budget == 5000
        assert [str(f) for f in session.compliance_frameworks] == ["pdpl", "gdpr"]
        assert session.status == "pending"

    def test_invalid_enum_falls_back_to_sensible_defaults(self) -> None:
        session = build_session(
            project_name="App",
            workload_type="not_a_workload",
            scale="huge",
            region="mars",
            frameworks=[],
            budget=None,
            services="",
            context="",
        )
        # use_enum_values stores enum members as plain strings in the model.
        assert session.workload_type == "mixed"
        assert session.scale == "medium"
        assert session.region == "uaenorth"

    def test_zero_budget_becomes_none(self) -> None:
        session = build_session(
            project_name="App",
            workload_type="mixed",
            scale="small",
            region="eastus",
            frameworks=[],
            budget=0,
            services="",
            context="",
        )
        assert session.budget is None

    def test_unknown_frameworks_are_dropped(self) -> None:
        session = build_session(
            project_name="App",
            workload_type="mixed",
            scale="small",
            region="eastus",
            frameworks=["pdpl", "made_up"],
            budget=None,
            services="",
            context="",
        )
        assert [str(f) for f in session.compliance_frameworks] == ["pdpl"]


# ── Pure helpers ────────────────────────────────────────────────────────


class TestHelpers:
    def test_agent_display_name_accepts_str_and_enum(self) -> None:
        assert agent_display_name(AgentType.ARCHITECT) == "Architect"
        assert agent_display_name("cost_analyst") == "Cost Analyst"
        assert agent_display_name("nonsense") == "nonsense"

    def test_conflict_severity(self) -> None:
        resolved = Conflict(
            dimension="architect_vs_cost",
            agents=[AgentType.ARCHITECT, AgentType.COST_ANALYST],
            issue="over budget",
            resolution="trim compute",
        )
        assert conflict_severity(resolved) == "resolved"

        high = Conflict(
            dimension="cost_vs_security",
            agents=[AgentType.COST_ANALYST, AgentType.SECURITY],
            issue="firewall cost",
            resolution="",
        )
        assert conflict_severity(high) == "high"

        medium = Conflict(
            dimension="architect_vs_cost",
            agents=[AgentType.ARCHITECT, AgentType.COST_ANALYST],
            issue="over budget",
            resolution="",
        )
        assert conflict_severity(medium) == "medium"

    def test_format_currency(self) -> None:
        assert format_currency(4250.5) == "$4,250.50"
        assert format_currency(None) == "—"
        assert format_currency(True) == "—"

    def test_artifact_bytes_are_utf8(self) -> None:
        artifact = Artifact(
            name="a.bicep",
            type="iac_bicep",
            format="bicep",
            content="// ── Compute ──",
        )
        assert artifact_bytes(artifact) == "// ── Compute ──".encode()

    def test_session_status_badge(self) -> None:
        session = Session(project_name="App")
        assert session_status_badge(session) == ":blue[PENDING]"
        session.status = "completed"
        assert session_status_badge(session) == ":green[COMPLETED]"

    def test_build_agent_markdown_strips_html(self) -> None:
        turn = AgentTurn(
            agent_type=AgentType.SECURITY,
            output={
                "overall_risk_rating": "MEDIUM",
                "findings": [{"control": "<script>alert(1)</script>XSS", "status": "WARNING"}],
            },
        )
        rendered = build_agent_markdown(turn)
        assert "<script>" not in rendered
        assert "XSS" in rendered

    def test_build_agent_markdown_error_turn(self) -> None:
        turn = AgentTurn(agent_type=AgentType.ARCHITECT, output={"error": "LLM call failed"})
        assert build_agent_markdown(turn) == "LLM call failed"


# ── Streamlit integration (AppTest) ─────────────────────────────────────


class TestDashboardApp:
    # The full-flow reruns poll a real 5-agent pipeline on a background thread;
    # under full-suite load those reruns can take tens of seconds, so the
    # per-run AppTest timeout must be generous (the pipeline itself is what
    # the test exercises, not a slow network call).
    _RUN_TIMEOUT = 90

    def _run_analysis(
        self,
        project_name: str = "E-Shop",
        context: str = "Design a scalable web app for the UAE market",
    ) -> AppTest:
        app = AppTest.from_file(str(_DASHBOARD_PATH), default_timeout=self._RUN_TIMEOUT)
        app.run()
        assert not app.exception

        # Form widgets (index order matches the form layout).
        app.text_input[0].set_value(project_name)
        app.multiselect[0].set_value(["pdpl"])
        app.text_area[0].set_value("Web app, API, PostgreSQL")
        app.text_area[1].set_value(context)
        app.button[0].click()
        app.run()
        assert not app.exception
        # One more rerun: the sidebar history is populated on the next pass,
        # exactly as a user would see it after the analysis completes.
        app.run()
        assert not app.exception
        return app

    def test_full_flow_produces_results(self) -> None:
        app = self._run_analysis()
        titles = [t.value for t in app.title]
        assert "Analysis results" in titles
        markdown = [m.value for m in app.markdown]
        assert any("architecture.bicep" in m for m in markdown)
        assert any("cost_forecast.json" in m for m in markdown)
        assert any("compliance_report.md" in m for m in markdown)
        assert any("arbitration_summary.md" in m for m in markdown)
        # Judge summary should be present (mock judge succeeds).
        assert any("Final recommendation" in m for m in markdown)
        # Session history persists: the sidebar placeholder is replaced.
        captions = [c.value for c in app.caption]
        assert not any("No analyses yet" in c for c in captions)

    def test_xss_in_project_name_is_escaped(self) -> None:
        app = self._run_analysis(project_name="<script>alert(1)</script>EvilStore")
        rendered = " ".join(
            [t.value for t in app.title]
            + [m.value for m in app.markdown]
            + [c.value for c in app.caption]
        )
        assert "EvilStore" in rendered
        assert "<script>" not in rendered

    def test_initial_page_shows_form(self) -> None:
        app = AppTest.from_file(str(_DASHBOARD_PATH), default_timeout=self._RUN_TIMEOUT)
        app.run()
        assert not app.exception
        # Sanity: initial page shows the input form and no results yet.
        titles = [t.value for t in app.title]
        assert "Analysis results" not in titles
        assert any(s.value == "Describe your infrastructure" for s in app.subheader)
