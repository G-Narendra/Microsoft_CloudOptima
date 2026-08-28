"""Tests for action governance — policy verdicts, fail-closed, and YAML/Python policy drift detection."""

from __future__ import annotations

import re
from unittest.mock import MagicMock, patch

import pytest

from cloudoptima.config import Settings
from cloudoptima.governance import (
    _POLICY,
    POLICY_PATH,
    GovernanceDeniedError,
    Verdict,
    check_action,
    enforce_action,
    governed_callable,
)


def test_read_only_actions_allowed() -> None:
    for action_type in ("get_live_price", "compliance_lookup", "list_regions"):
        assert check_action({"type": action_type}) == Verdict.ALLOW


def test_destructive_actions_denied() -> None:
    for action_type in ("deploy", "create", "delete", "drop", "shell"):
        assert check_action({"type": action_type}) == Verdict.DENY


def test_unknown_action_fails_closed() -> None:
    """Anything not listed in the policy is denied — never a silent allow."""
    assert check_action({"type": "mystery_action"}) == Verdict.DENY


def test_email_send_denied() -> None:
    """send_email is not an exposed tool — the policy denies it outright."""
    assert check_action({"type": "send_email"}) == Verdict.DENY


def test_missing_type_field_fails_closed() -> None:
    assert check_action({}) == Verdict.DENY
    assert check_action({"not_type": "deploy"}) == Verdict.DENY


def test_enforce_action_allows_read_only() -> None:
    enforce_action({"type": "get_live_price"})


def test_enforce_action_raises_on_deny() -> None:
    with pytest.raises(GovernanceDeniedError) as exc_info:
        enforce_action({"type": "deploy"})
    assert "deploy" in str(exc_info.value)
    assert exc_info.value.verdict == Verdict.DENY


def test_governed_callable_wraps_allowed() -> None:
    def _read() -> str:
        return "allowed"

    wrapped = governed_callable("get_live_price", _read)
    assert wrapped() == "allowed"


def test_governed_callable_blocks_denied() -> None:
    called = False

    def _write() -> None:
        nonlocal called
        called = True

    wrapped = governed_callable("deploy", _write)
    with pytest.raises(GovernanceDeniedError):
        wrapped()
    assert not called


def test_governed_callable_passes_args() -> None:
    def _add(a: int, b: int) -> int:
        return a + b

    wrapped = governed_callable("get_live_price", _add)
    assert wrapped(2, 3) == 5


def test_governance_disabled_allows_everything() -> None:
    settings = Settings(governance_enabled=False)
    assert check_action({"type": "deploy"}, settings) == Verdict.ALLOW
    enforce_action({"type": "deploy"}, settings)


def test_policy_yaml_exists_and_parses() -> None:
    assert POLICY_PATH.exists(), f"policy YAML missing at {POLICY_PATH}"
    content = POLICY_PATH.read_text(encoding="utf-8")
    assert "apiVersion: governance.toolkit/v1" in content
    assert "name: cloudoptima-tools" in content


def _yaml_policy() -> dict[str, str]:
    content = POLICY_PATH.read_text(encoding="utf-8")
    rules: dict[str, str] = {}
    for block in content.split("- name:")[1:]:
        action = re.search(r"action:\s*(\w+)", block)
        if action is None:
            continue
        listed = re.search(r"action\.type in \[([^\]]+)\]", block)
        if listed is not None:
            for action_type in re.findall(r"'([^']+)'", listed.group(1)):
                rules[action_type] = action.group(1)
            continue
        equality = re.search(r"action\.type == '([^']+)'", block)
        if equality is not None:
            rules[equality.group(1)] = action.group(1)
    return rules


def test_yaml_policy_mirrors_python_policy() -> None:
    """The AGT source of truth and the offline mirror must agree."""
    yaml_rules = _yaml_policy()
    assert yaml_rules, "policy YAML should contain rules"
    python_rules = {name: verdict.value for name, verdict in _POLICY.items()}
    assert yaml_rules == python_rules


def test_check_action_logging():
    mock_logger = MagicMock()
    check_action({"type": "get_live_price"}, logger=mock_logger)
    assert mock_logger.log.called


def test_check_action_logging_exception():
    mock_logger = MagicMock()
    mock_logger.log.side_effect = Exception("log error")
    verdict = check_action({"type": "get_live_price"}, logger=mock_logger)
    assert verdict == Verdict.ALLOW


def test_agt_integration_branch():
    mock_engine_cls = MagicMock()
    mock_engine = MagicMock()
    mock_engine.evaluate.return_value = MagicMock(action=MagicMock(value="ALLOW"))
    mock_engine_cls.return_value = mock_engine
    
    with patch("cloudoptima.governance.PolicyEngine", mock_engine_cls):
        with patch("cloudoptima.governance._AGT_AVAILABLE", True):
            verdict = check_action({"type": "get_live_price"})
            assert verdict == Verdict.ALLOW
            assert mock_engine.evaluate.called

def test_agt_integration_branch_deny():
    mock_engine_cls = MagicMock()
    mock_engine = MagicMock()
    mock_engine.evaluate.return_value = MagicMock(action=MagicMock(value="DENY"))
    mock_engine_cls.return_value = mock_engine
    
    with patch("cloudoptima.governance.PolicyEngine", mock_engine_cls):
        with patch("cloudoptima.governance._AGT_AVAILABLE", True):
            verdict = check_action({"type": "deploy"})
            assert verdict == Verdict.DENY
            assert mock_engine.evaluate.called

def test_agt_integration_branch_exception():
    mock_engine_cls = MagicMock()
    mock_engine = MagicMock()
    mock_engine.evaluate.side_effect = Exception("AGT failed")
    mock_engine_cls.return_value = mock_engine
    
    with patch("cloudoptima.governance.PolicyEngine", mock_engine_cls):
        with patch("cloudoptima.governance._AGT_AVAILABLE", True):
            verdict = check_action({"type": "get_live_price"})
            assert verdict == Verdict.ALLOW
