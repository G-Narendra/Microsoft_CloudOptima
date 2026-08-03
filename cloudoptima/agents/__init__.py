"""Agent implementations for CloudOptima.

Exports all five agent classes plus discovery helpers used by the orchestrator
and dashboard:

- ``ALL_AGENTS`` — the five agent classes in pipeline order.
- ``DISPLAY_NAMES`` — human-readable labels keyed by :class:`AgentType`.
"""

from __future__ import annotations

from typing import Final

from cloudoptima.agent_base import BaseAgent
from cloudoptima.agents.architect import ArchitectAgent
from cloudoptima.agents.compliance import ComplianceOfficerAgent
from cloudoptima.agents.cost_analyst import CostAnalystAgent
from cloudoptima.agents.judge import JudgeAgent
from cloudoptima.agents.security import SecurityEngineerAgent
from cloudoptima.models import AgentType

# The five agents, in pipeline execution order (Phase 6 runs them in this
# order; the judge always comes last so it can see every other output).
ALL_AGENTS: Final[list[type[BaseAgent]]] = [
    ArchitectAgent,
    CostAnalystAgent,
    SecurityEngineerAgent,
    ComplianceOfficerAgent,
    JudgeAgent,
]

# Display labels for the dashboard (Phase 7).
DISPLAY_NAMES: Final[dict[AgentType, str]] = {
    AgentType.ARCHITECT: "Architect",
    AgentType.COST_ANALYST: "Cost Analyst",
    AgentType.SECURITY: "Security Engineer",
    AgentType.COMPLIANCE: "Compliance Officer",
    AgentType.JUDGE: "Judge",
}

__all__ = [
    "ALL_AGENTS",
    "DISPLAY_NAMES",
    "ArchitectAgent",
    "ComplianceOfficerAgent",
    "CostAnalystAgent",
    "JudgeAgent",
    "SecurityEngineerAgent",
]
