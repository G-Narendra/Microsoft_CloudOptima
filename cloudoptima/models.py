"""Data models and enumerations for CloudOptima."""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Any
import uuid

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


# Enumerations

class UserRole(StrEnum):
    """Roles for local RBAC login simulation."""
    VIEWER = "viewer"
    REVIEWER = "reviewer"
    ADMIN = "admin"


class User(BaseModel):
    """Represents an authenticated user in the local RBAC system."""
    username: str
    role: UserRole


class AgentType(StrEnum):
    """Supported agent roles within the multi-agent system."""

    ARCHITECT = "architect"
    COST_ANALYST = "cost_analyst"
    SECURITY = "security"
    COMPLIANCE = "compliance"
    JUDGE = "judge"


class WorkloadType(StrEnum):
    """Workload type patterns (realtime, batch, streaming, mixed)."""

    REALTIME = "realtime"
    BATCH = "batch"
    STREAMING = "streaming"
    MIXED = "mixed"


class DeploymentScale(StrEnum):
    """Deployment scale tiers."""

    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    ENTERPRISE = "enterprise"


class AzureRegion(StrEnum):
    """Supported Azure regions."""

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
    """Supported compliance and regulatory frameworks."""

    PDPL = "pdpl"
    HIPAA = "hipaa"
    SOC2 = "soc2"
    ISO27001 = "iso27001"
    GDPR = "gdpr"


# Base Model with Automatic Null Byte Sanitization

def sanitize_null_bytes(val: Any) -> Any:
    """Recursively remove null bytes from strings inside dicts and lists."""
    if isinstance(val, str):
        return val.replace("\x00", "")
    elif isinstance(val, dict):
        return {sanitize_null_bytes(k): sanitize_null_bytes(v) for k, v in val.items()}
    elif isinstance(val, list):
        return [sanitize_null_bytes(item) for item in val]
    return val


class SanitizedBaseModel(BaseModel):
    """Base Pydantic model that strips null bytes from all text fields automatically."""

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


# Domain Models

class AgentTurn(SanitizedBaseModel):
    """Single agent turn output, execution timing, and token usage."""

    agent_type: AgentType = Field(description="The agent role performing this turn")
    output: dict[str, Any] = Field(
        default_factory=dict,
        description="Structured output dictionary produced by the agent",
    )
    latency_ms: float = Field(default=0.0, ge=0.0, description="Execution time in milliseconds")
    tokens_used: int = Field(default=0, ge=0, description="Tokens consumed by this turn")
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="UTC timestamp of turn completion",
    )


class Conflict(SanitizedBaseModel):
    """Conflict between agents and its arbitration resolution."""

    dimension: str = Field(
        default="",
        description="Conflict dimension (e.g. cost_vs_security, architect_vs_compliance)",
    )
    agents: list[AgentType] = Field(
        description="List of agents involved in the conflict (minimum 2)"
    )
    issue: str = Field(description="Description of disagreement")
    resolution: str = Field(description="Arbitration resolution from Judge agent")

    @field_validator("agents")
    @classmethod
    def validate_min_agents(cls, v: list[AgentType]) -> list[AgentType]:
        """Ensure a conflict involves at least two agents."""
        if len(v) < 2:
            raise ValueError("Conflict must involve at least 2 disagreeing agents")
        return v


class Artifact(SanitizedBaseModel):
    """Generated deliverable (e.g. Bicep template, cost forecast, markdown report)."""

    artifact_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique identifier for the artifact",
    )
    name: str = Field(description="Filename of the artifact")
    type: str = Field(
        description="Artifact kind: iac_bicep, cost_forecast, compliance_report, etc."
    )
    format: str = Field(
        default="text",
        description="Content format: bicep, json, markdown",
    )
    content: str = Field(description="Raw text content of the generated artifact")
    description: str = Field(default="", description="Summary description of the artifact")


class Session(SanitizedBaseModel):
    """Session state encompassing user input, agent turns, conflicts, and artifacts."""

    session_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique session identifier UUID",
    )
    project_name: str = Field(description="User-provided project or workload name")
    workload_type: WorkloadType = Field(
        default=WorkloadType.MIXED, description="Kind of workload being designed for"
    )
    scale: DeploymentScale = Field(
        default=DeploymentScale.MEDIUM, description="Deployment scale"
    )
    region: AzureRegion = Field(
        default=AzureRegion.UAE_NORTH, description="Target Azure region"
    )
    compliance_frameworks: list[ComplianceFramework] = Field(
        default_factory=list, description="Target compliance frameworks"
    )
    budget: float | None = Field(
        default=None,
        description="Monthly budget in USD (None for unconstrained)",
    )
    services: str = Field(
        default="", description="User-requested services"
    )
    status: str = Field(
        default="pending", description="Lifecycle: pending, running, pending_approval, completed, failed"
    )
    hitl_approved: bool = Field(
        default=False, description="Whether design has been approved prior to artifact generation"
    )
    error_message: str = Field(
        default="",
        description="Error or rate-limit message if failed",
    )
    user_prompt: str = Field(default="", description="Requirements prompt")
    on_token: Any = Field(default=None, exclude=True, description="Streaming callback hook")
    agent_turns: list[AgentTurn] = Field(
        default_factory=list, description="Agent turns in pipeline order"
    )
    conflicts: list[Conflict] = Field(
        default_factory=list, description="Detected conflicts and resolutions"
    )
    artifacts: list[Artifact] = Field(
        default_factory=list, description="Generated artifacts"
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Session creation timestamp",
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Session last update timestamp",
    )
