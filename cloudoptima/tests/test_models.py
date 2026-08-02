"""Tests for domain data models and enumerations."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

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


def test_enum_values() -> None:
    """Test string representations and enum values."""
    assert AgentType.ARCHITECT.value == "architect"
    assert AgentType.JUDGE.value == "judge"
    assert WorkloadType.REALTIME.value == "realtime"
    assert DeploymentScale.ENTERPRISE.value == "enterprise"
    assert AzureRegion.UAE_NORTH.value == "uaenorth"
    assert ComplianceFramework.PDPL.value == "pdpl"
    assert ComplianceFramework.HIPAA.value == "hipaa"


def test_session_full_creation() -> None:
    """Test creating a full Session with nested models."""
    turn = AgentTurn(
        agent_type=AgentType.ARCHITECT,
        output={"architecture": "Microservices on AKS", "services": ["AKS", "Azure SQL"]},
        latency_ms=1250.5,
        tokens_used=500,
    )
    conflict = Conflict(
        agents=[AgentType.COST_ANALYST, AgentType.SECURITY],
        issue="Security prefers Premium Firewall; Cost prefers Standard",
        resolution="Judge resolved: Use Standard Firewall with custom NSGs",
    )
    artifact = Artifact(
        name="main.bicep",
        type="iac_bicep",
        content="param location string = 'uaenorth'",
        description="Main infrastructure template",
    )

    session = Session(
        project_name="ECommerce Scale Up",
        workload_type=WorkloadType.STREAMING,
        scale=DeploymentScale.LARGE,
        region=AzureRegion.UAE_NORTH,
        compliance_frameworks=[ComplianceFramework.PDPL, ComplianceFramework.SOC2],
        user_prompt="Build high-availability architecture in UAE",
        agent_turns=[turn],
        conflicts=[conflict],
        artifacts=[artifact],
    )

    assert session.project_name == "ECommerce Scale Up"
    assert len(session.agent_turns) == 1
    assert session.agent_turns[0].agent_type == AgentType.ARCHITECT
    assert len(session.conflicts) == 1
    assert len(session.artifacts) == 1
    assert session.artifacts[0].name == "main.bicep"


def test_null_byte_stripped() -> None:
    """Test that null bytes (\x00) are automatically stripped from string fields."""
    session = Session(
        project_name="Project\x00Name\x00WithNulls",
        user_prompt="Deploy\x00 App",
    )
    assert session.project_name == "ProjectNameWithNulls"
    assert session.user_prompt == "Deploy App"


def test_null_byte_in_agent_turn() -> None:
    """Test null byte stripping in nested dictionaries within AgentTurn."""
    turn = AgentTurn(
        agent_type=AgentType.SECURITY,
        output={"key\x00name": "val\x00ue", "details": ["safe\x00text"]},
    )
    assert "keyname" in turn.output
    assert turn.output["keyname"] == "value"
    assert turn.output["details"] == ["safetext"]


def test_session_round_trip() -> None:
    """Test dict dump and validation round-trip."""
    original = Session(
        project_name="RoundTrip Test",
        workload_type=WorkloadType.BATCH,
        scale=DeploymentScale.SMALL,
        region=AzureRegion.EAST_US,
        compliance_frameworks=[ComplianceFramework.HIPAA],
    )

    dumped = original.model_dump()
    reconstructed = Session.model_validate(dumped)

    assert reconstructed.session_id == original.session_id
    assert reconstructed.project_name == original.project_name
    assert reconstructed.workload_type == original.workload_type
    assert reconstructed.scale == original.scale
    assert reconstructed.region == original.region
    assert reconstructed.compliance_frameworks == original.compliance_frameworks


def test_session_json_round_trip() -> None:
    """Test JSON serialization and deserialization round-trip."""
    original = Session(
        project_name="JSON RoundTrip Test",
        user_prompt="Test prompt",
        agent_turns=[
            AgentTurn(
                agent_type=AgentType.JUDGE,
                output={"verdict": "APPROVED"},
                latency_ms=300.0,
                tokens_used=150,
            )
        ],
    )

    json_str = original.model_dump_json()
    reconstructed = Session.model_validate_json(json_str)

    assert reconstructed.session_id == original.session_id
    assert reconstructed.project_name == original.project_name
    assert len(reconstructed.agent_turns) == 1
    assert reconstructed.agent_turns[0].agent_type == AgentType.JUDGE
    assert reconstructed.agent_turns[0].output == {"verdict": "APPROVED"}


def test_conflict_requires_two_agents() -> None:
    """Test that Conflict validation fails if fewer than 2 agents are provided."""
    with pytest.raises(ValidationError):
        Conflict(
            agents=[AgentType.ARCHITECT],
            issue="Single agent cannot have a conflict",
            resolution="N/A",
        )


def test_session_defaults() -> None:
    """Test default values on Session model."""
    session = Session(project_name="Minimal Session")
    assert session.session_id is not None
    assert len(session.session_id) > 0
    assert session.workload_type == WorkloadType.MIXED
    assert session.scale == DeploymentScale.MEDIUM
    assert session.region == AzureRegion.UAE_NORTH
    assert session.compliance_frameworks == []
    assert session.agent_turns == []
    assert session.conflicts == []
    assert session.artifacts == []
