"""Data models and enumerations for CloudOptima.

Provides type-safe Pydantic v2 domain models for agent interactions,
architectural configurations, conflicts, artifacts, and multi-agent sessions.
Automatically sanitizes all text input fields by stripping null bytes (\x00).
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

# ── Enumerations ─────────────────────────────────────────────────────────────


class AgentType(str, Enum):
    """Supported agent roles within the multi-agent system."""

    ARCHITECT = "architect"
    COST_ANALYST = "cost_analyst"
    SECURITY = "security"
    COMPLIANCE = "compliance"
    JUDGE = "judge"


class WorkloadType(str, Enum):
    """Target workload characteristic profiles."""

    REALTIME = "realtime"
    BATCH = "batch"
    STREAMING = "streaming"
    MIXED = "mixed"


class DeploymentScale(str, Enum):
    """Scale categories for target infrastructure."""

    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    ENTERPRISE = "enterprise"


class AzureRegion(str, Enum):
    """Major Azure deployment regions."""

    UAE_NORTH = "uaenorth"
    EAST_US = "eastus"
    EAST_US_2 = "eastus2"
    WEST_US = "westus"
    WEST_US_2 = "westus2"
    WEST_EUROPE = "westeurope"
    NORTH_EUROPE = "northeurope"
    SOUTHEAST_ASIA = "southeastasia"
    EAST_ASIA = "eastasia"
    UK_SOUTH = "uksouth"
    UK_WEST = "ukwest"
    GERMANY_WEST_CENTRAL = "germanywestcentral"
    SWITZERLAND_NORTH = "switzerlandnorth"
    CENTRAL_INDIA = "centralindia"
    JAPAN_EAST = "japaneast"
    AUSTRALIA_EAST = "australiaeast"
    BRAZIL_SOUTH = "brazilsouth"


class ComplianceFramework(str, Enum):
    """Supported regulatory and compliance frameworks."""

    PDPL = "pdpl"
    HIPAA = "hipaa"
    SOC2 = "soc2"
    ISO27001 = "iso27001"
    GDPR = "gdpr"


# ── Base Model with Automatic Null Byte Sanitization ──────────────────────────


def sanitize_null_bytes(val: Any) -> Any:
    """Recursively strip null bytes (\x00) from string values in strings, dicts, and lists."""
    if isinstance(val, str):
        return val.replace("\x00", "")
    elif isinstance(val, dict):
        return {sanitize_null_bytes(k): sanitize_null_bytes(v) for k, v in val.items()}
    elif isinstance(val, list):
        return [sanitize_null_bytes(item) for item in val]
    return val


class SanitizedBaseModel(BaseModel):
    """Base Pydantic model that strips null bytes from all text fields automatically.

    Extra fields are forbidden (``extra="forbid"``) so unexpected keys in LLM
    output or user input fail validation instead of being silently accepted.
    """

    model_config = ConfigDict(
        use_enum_values=True,
        populate_by_name=True,
        validate_assignment=True,
        extra="forbid",
    )

    @model_validator(mode="before")
    @classmethod
    def strip_null_bytes_from_all_fields(cls, data: Any) -> Any:
        """Strip null bytes from input data prior to field validation."""
        if isinstance(data, dict):
            return sanitize_null_bytes(data)
        return data


# ── Domain Models ─────────────────────────────────────────────────────────────


class AgentTurn(SanitizedBaseModel):
    """Record of a single agent's analysis or proposal turn."""

    agent_type: AgentType = Field(description="The agent role performing this turn")
    output: dict[str, Any] = Field(
        default_factory=dict,
        description="Structured output dictionary produced by the agent",
    )
    latency_ms: float = Field(default=0.0, ge=0.0, description="Execution latency in milliseconds")
    tokens_used: int = Field(default=0, ge=0, description="Total tokens consumed during turn")
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="UTC timestamp of when the turn completed",
    )


class Conflict(SanitizedBaseModel):
    """Disagreement between two or more agents, with its issue description and resolution."""

    dimension: str = Field(
        default="",
        description="Conflict dimension (e.g. cost_vs_security, architect_vs_compliance)",
    )
    agents: list[AgentType] = Field(
        description="List of agents involved in the conflict (minimum 2)"
    )
    issue: str = Field(description="Description of the disagreement issue")
    resolution: str = Field(description="Resolution provided by Judge agent")

    @field_validator("agents")
    @classmethod
    def validate_min_agents(cls, v: list[AgentType]) -> list[AgentType]:
        """Ensure a conflict involves at least two agents."""
        if len(v) < 2:
            raise ValueError("Conflict must involve at least 2 disagreeing agents")
        return v


class Artifact(SanitizedBaseModel):
    """Generated architecture output file (e.g. IaC Bicep, Terraform, Cost Report)."""

    artifact_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique identifier for the artifact",
    )
    name: str = Field(description="Filename or title of the artifact")
    type: str = Field(description="Type of artifact (e.g. iac_bicep, cost_report, diagram)")
    format: str = Field(
        default="text", description="Content format (e.g. bicep, terraform, json, text)"
    )
    content: str = Field(description="Raw text content of the generated artifact")
    description: str = Field(default="", description="Summary description of the artifact")


class Session(SanitizedBaseModel):
    """Complete session capturing user inputs, agent turns, conflicts, and generated artifacts."""

    session_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique session identifier UUID",
    )
    project_name: str = Field(description="User-defined project or workload name")
    workload_type: WorkloadType = Field(
        default=WorkloadType.MIXED, description="Category of workload"
    )
    scale: DeploymentScale = Field(
        default=DeploymentScale.MEDIUM, description="Infrastructure deployment scale"
    )
    region: AzureRegion = Field(
        default=AzureRegion.UAE_NORTH, description="Primary Azure target region"
    )
    compliance_frameworks: list[ComplianceFramework] = Field(
        default_factory=list, description="Target compliance standards"
    )
    budget: float | None = Field(
        default=None, description="User-specified monthly budget in USD (None if not provided)"
    )
    services: str = Field(
        default="", description="User-described services/stack (comma-separated text)"
    )
    status: str = Field(
        default="pending", description="Pipeline status: pending, running, completed, failed"
    )
    user_prompt: str = Field(default="", description="Original user prompt or requirements text")
    agent_turns: list[AgentTurn] = Field(
        default_factory=list, description="Ordered list of agent turns"
    )
    conflicts: list[Conflict] = Field(
        default_factory=list, description="List of detected and resolved conflicts"
    )
    artifacts: list[Artifact] = Field(
        default_factory=list, description="Generated IaC and documentation artifacts"
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Session creation timestamp",
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Session last update timestamp",
    )
