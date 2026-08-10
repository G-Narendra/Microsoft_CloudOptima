"""Tests for action governance (issue #5) — policy verdicts, fail-closed,
and YAML/Python policy drift detection. All tests run without AGT installed.
"""

from __future__ import annotations

import re

import pytest

from cloudoptima.config import Settings
from cloudoptima.governance import (
    POLICY_PATH,
    GovernanceDeniedError,
    Verdict,
    check_action,
    enforce_action,
    governed_callable,
)

# ── check_action verdicts ─────────────────────────────────────────────────


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


def test_governance_disabled_allows_everything() -> None:
    settings = Settings(governance_enabled=False)
    assert check_action({"type": "deploy"}, settings) == Verdict.ALLOW


# ── enforce_action ────────────────────────────────────────────────────────


def test_enforce_allowed_does_not_raise() -> None:
    enforce_action({"type": "get_live_price"})  # no exception


def test_enforce_denied_raises() -> None:
    with pytest.raises(GovernanceDeniedError):
        enforce_action({"type": "deploy"})


def test_enforce_send_email_raises_denied() -> None:
    with pytest.raises(GovernanceDeniedError):
        enforce_action({"type": "send_email"})


# ── governed_callable ─────────────────────────────────────────────────────


def test_governed_callable_runs_allowed_tools() -> None:
    calls: list[str] = []

    def _tool(service: str) -> str:
        calls.append(service)
        return f"price for {service}"

    wrapped = governed_callable(_tool, "get_live_price")
    assert wrapped(service="vm") == "price for vm"
    assert calls == ["vm"]


def test_governed_callable_blocks_denied_tools() -> None:
    def _tool() -> str:  # pragma: no cover - must never run
        raise AssertionError("denied tool executed")

    wrapped = governed_callable(_tool, "deploy")
    with pytest.raises(GovernanceDeniedError):
        wrapped()


# ── YAML policy stays in sync with the Python mirror ──────────────────────


def _yaml_policy() -> dict[str, str]:
    """Crude YAML reader for tools.yaml — enough to catch drift in the rules.

    Handles both rule shapes: ``action.type in [...]`` lists and
    ``action.type == 'x'`` equality conditions.
    """
    text = POLICY_PATH.read_text(encoding="utf-8")
    rules: dict[str, str] = {}
    for block in text.split("  - name:"):
        action = re.search(r"^\s*action: (\w+)", block, re.M)
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
    from cloudoptima.governance import _POLICY

    yaml_rules = _yaml_policy()
    assert yaml_rules, "policy YAML should contain rules"
    python_rules = {name: verdict.value for name, verdict in _POLICY.items()}
    assert yaml_rules == python_rules
