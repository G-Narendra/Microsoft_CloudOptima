"""Specialist agents for CloudOptima pipeline."""

from __future__ import annotations

from typing import Final

from cloudoptima.agent_base import BaseAgent
from cloudoptima.agents.architect import ArchitectAgent
from cloudoptima.agents.compliance import ComplianceOfficerAgent
from cloudoptima.agents.cost_analyst import CostAnalystAgent
from cloudoptima.agents.judge import JudgeAgent
from cloudoptima.agents.security import SecurityEngineerAgent
from cloudoptima.models import AgentType

ALL_AGENTS: Final[list[type[BaseAgent]]] = [
    ArchitectAgent,
    CostAnalystAgent,
    SecurityEngineerAgent,
    ComplianceOfficerAgent,
    JudgeAgent,
]

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
