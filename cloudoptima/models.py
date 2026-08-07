"""Data models and enumerations for CloudOptima.

Provides type-safe Pydantic v2 domain models for agent interactions,
architectural configurations, conflicts, artifacts, and multi-agent sessions.
Automatically sanitizes all text input fields by stripping null bytes (\x00).
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

# ── Enumerations ─────────────────────────────────────────────────────────────


class AgentType(StrEnum):
    """Supported agent roles within the multi-agent system."""

    ARCHITECT = "architect"
    COST_ANALYST = "cost_analyst"
    SECURITY = "security"
    COMPLIANCE = "compliance"
    JUDGE = "judge"


class WorkloadType(StrEnum):
    """How the workload hits the infrastructure (spiky, steady, continuous)."""

    REALTIME = "realtime"
    BATCH = "batch"
    STREAMING = "streaming"
    MIXED = "mixed"


class DeploymentScale(StrEnum):
    """How big the deployment is — drives sizing and cost assumptions."""

    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    ENTERPRISE = "enterprise"


class AzureRegion(StrEnum):
    """Regions we let users pick from (data residency matters for compliance)."""

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


class ComplianceFramework(StrEnum):
    """Regulatory frameworks the compliance agent can be asked to check."""

    PDPL = "pdpl"
    HIPAA = "hipaa"
    SOC2 = "soc2"
    ISO27001 = "iso27001"
    GDPR = "gdpr"


# ── Base Model with Automatic Null Byte Sanitization ──────────────────────────


def sanitize_null_bytes(val: Any) -> Any:
    """Recursively remove null bytes (\x00) from strings inside dicts and lists."""
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
    """One agent's contribution to a session — its output, timing, and token use."""

    agent_type: AgentType = Field(description="The agent role performing this turn")
    output: dict[str, Any] = Field(
        default_factory=dict,
        description="Structured output dictionary produced by the agent",
    )
    latency_ms: float = Field(default=0.0, ge=0.0, description="Wall-clock time the turn took")
    tokens_used: int = Field(default=0, ge=0, description="Tokens consumed by this turn")
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="UTC timestamp of when the turn completed",
    )


class Conflict(SanitizedBaseModel):
    """Two agents disagreeing — what about, who's involved, and how it got resolved."""

    dimension: str = Field(
        default="",
        description="Conflict dimension (e.g. cost_vs_security, architect_vs_compliance)",
    )
    agents: list[AgentType] = Field(
        description="List of agents involved in the conflict (minimum 2)"
    )
    issue: str = Field(description="What the agents disagree on")
    resolution: str = Field(description="How the Judge settled it (empty until arbitration)")

    @field_validator("agents")
    @classmethod
    def validate_min_agents(cls, v: list[AgentType]) -> list[AgentType]:
        """Ensure a conflict involves at least two agents."""
        if len(v) < 2:
            raise ValueError("Conflict must involve at least 2 disagreeing agents")
        return v


class Artifact(SanitizedBaseModel):
    """A generated deliverable — Bicep template, cost report, or summary doc."""

    artifact_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique identifier for the artifact",
    )
    name: str = Field(description="Filename of the artifact (e.g. architecture.bicep)")
    type: str = Field(
        description="Artifact kind: iac_bicep, cost_forecast, compliance_report, etc."
    )
    format: str = Field(
        default="text",
        description="Content format for syntax highlighting: bicep, json, markdown",
    )
    content: str = Field(description="Raw text content of the generated artifact")
    description: str = Field(default="", description="Summary description of the artifact")


class Session(SanitizedBaseModel):
    """Everything about one analysis: the user's inputs and everything the pipeline produced."""

    session_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique session identifier UUID",
    )
    project_name: str = Field(description="User-provided project or workload name")
    workload_type: WorkloadType = Field(
        default=WorkloadType.MIXED, description="Kind of workload being designed for"
    )
    scale: DeploymentScale = Field(
        default=DeploymentScale.MEDIUM, description="How big the deployment is"
    )
    region: AzureRegion = Field(
        default=AzureRegion.UAE_NORTH, description="Primary Azure region to target"
    )
    compliance_frameworks: list[ComplianceFramework] = Field(
        default_factory=list, description="Regulations to check against"
    )
    budget: float | None = Field(
        default=None,
        description="Monthly budget in USD — None means the user didn't set a cap",
    )
    services: str = Field(
        default="", description="Services/stack the user described (free text)"
    )
    status: str = Field(
        default="pending", description="Lifecycle: pending, running, completed, failed"
    )
    error_message: str = Field(
        default="",
        description="Human-readable failure or rate-limit reason (empty on success)",
    )
    user_prompt: str = Field(default="", description="The user's requirements text")
    agent_turns: list[AgentTurn] = Field(
        default_factory=list, description="Agent turns in pipeline order"
    )
    conflicts: list[Conflict] = Field(
        default_factory=list, description="Disagreements found (and their resolutions)"
    )
    artifacts: list[Artifact] = Field(
        default_factory=list, description="Generated deliverables"
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Session creation timestamp",
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Session last update timestamp",
    )
