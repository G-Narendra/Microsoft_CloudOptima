"""CloudOptima — Multi-agent cloud architecture design system.

A multi-agent AI system where users describe infrastructure needs,
specialist agents analyze the requirements, and a Judge agent resolves
conflicts to produce a complete architecture with cost, security,
and compliance reports.
"""

from __future__ import annotations

from cloudoptima.config import Settings
from cloudoptima.context import AppContext
from cloudoptima.llm_cache import LLMCache
from cloudoptima.llm_client import (
    BaseLLMClient,
    MockClient,
    create_llm_client,
    generate_with_retry,
)
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
from cloudoptima.orchestrator import Orchestrator

__version__ = "0.1.0"

__all__ = [
    "Settings",
    "AppContext",
    "BaseLLMClient",
    "MockClient",
    "create_llm_client",
    "generate_with_retry",
    "LLMCache",
    "Orchestrator",
    "AgentTurn",
    "AgentType",
    "Artifact",
    "AzureRegion",
    "ComplianceFramework",
    "Conflict",
    "DeploymentScale",
    "Session",
    "WorkloadType",
]
