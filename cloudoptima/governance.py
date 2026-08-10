"""Action governance (issue #5) — every tool call is checked against policy.

This is the app-level control surface backed by Microsoft's **Agent
Governance Toolkit (AGT)**: before a tool executes, :func:`check_action`
evaluates the requested action against the declarative policy in
``cloudoptima/policies/tools.yaml`` and returns an ``allow`` / ``deny`` /
``require_approval`` verdict. Every decision is written to the tamper-evident
audit trail.

Enforcement is fail-closed and layered:

1. **Offline mirror** (:data:`_POLICY`) — deterministic Python copy of the
   policy, always enforced, fully tested, works with zero extra packages.
2. **AGT policy engine** — when ``agent-governance-toolkit`` is installed,
   :func:`check_action` loads the *same* YAML into
   ``agentmesh.governance.PolicyEngine`` and evaluates the action there. The
   verdicts are merged fail-closed: **the strictest of the two wins** (a deny
   from either side is a deny), so AGT can only ever narrow enforcement,
   never widen it. Any AGT hiccup falls back to the mirror (governance never
   becomes a crash point). The policy file passes ``agt lint-policy`` and is
   auditable with ``agt verify``.

:func:`enforce_action` raises :class:`GovernanceDeniedError` /
:class:`GovernanceNeedsApprovalError` on a non-allow verdict — the tool layer
never executes an action the policy does not permit.

Typical usage:
    >>> enforce_action({"type": "get_live_price", "params": {"service": "vm"}})
    >>> enforce_action({"type": "deploy", "params": {}})
    GovernanceDeniedError: ...  # denied by policy rule 'deny-write-actions'
"""

from __future__ import annotations

import functools
import logging
import threading
from enum import StrEnum
from pathlib import Path
from typing import Any, Final

from cloudoptima.config import Settings
from cloudoptima.observability import TraceEvent, get_audit_logger

_logger = logging.getLogger(__name__)

# Guarded import: agent-governance-toolkit is an optional dependency (extra
# `governance`). Without it the mirrored offline policy below keeps enforcing.
try:  # pragma: no cover - exercised only when AGT is installed
    from agentmesh.governance import PolicyEngine as _PolicyEngine

    AGT_AVAILABLE = True
except Exception:  # pragma: no cover - exercised only when the package is missing
    AGT_AVAILABLE = False

#: Path to the declarative policy (source of truth for AGT + `agt verify`).
POLICY_PATH: Final[Path] = Path(__file__).parent / "policies" / "tools.yaml"

#: The agent DID CloudOptima acts as inside AGT policies.
_AGT_AGENT_ID: Final[str] = "cloudoptima"

#: Lazily-built AGT PolicyEngine (built once, reused for every check).
_agt_engine_instance: Any | None = None
_agt_engine_failed: bool = False
_agt_lock = threading.Lock()


class Verdict(StrEnum):
    """The three verdicts the policy can return for an action."""

    ALLOW = "allow"
    DENY = "deny"
    REQUIRE_APPROVAL = "require_approval"


class GovernanceDeniedError(Exception):
    """Raised when the policy denies an action (fail closed)."""


class GovernanceNeedsApprovalError(Exception):
    """Raised when an action needs human approval before it may run."""


#: Fail-closed ordering used when merging AGT + mirror verdicts: a deny is
#: always stricter than an approval, which is stricter than an allow.
_VERDICT_STRICTNESS: Final[dict[Verdict, int]] = {
    Verdict.ALLOW: 0,
    Verdict.REQUIRE_APPROVAL: 1,
    Verdict.DENY: 2,
}


def _verdict_stricter(candidate: Verdict, current: Verdict) -> bool:
    """True when ``candidate`` is stricter than ``current`` (deny > approval > allow)."""
    return _VERDICT_STRICTNESS[candidate] > _VERDICT_STRICTNESS[current]


# ── Offline policy (mirrors cloudoptima/policies/tools.yaml) ──────────────
# action type -> verdict. Anything not listed is DENIED (fail closed) — a
# tool that forgets to declare itself simply cannot run.
_POLICY: Final[dict[str, Verdict]] = {
    # Read-only lookups are the only tools we expose today.
    "get_live_price": Verdict.ALLOW,
    "compliance_lookup": Verdict.ALLOW,
    "list_regions": Verdict.ALLOW,
    # Not an exposed tool; denied here (AGT CLI linter accepts allow/deny/warn
    # only — require_approval stays available in the runtime engine mapping).
    "send_email": Verdict.DENY,
    # Destructive / state-changing actions are structurally impossible.
    "deploy": Verdict.DENY,
    "create": Verdict.DENY,
    "delete": Verdict.DENY,
    "drop": Verdict.DENY,
    "shell": Verdict.DENY,
}


def _verdict_for(action_type: str) -> Verdict:
    """Look up the policy verdict for an action type (unknown => deny)."""
    return _POLICY.get(action_type, Verdict.DENY)


def check_action(
    action: dict[str, Any],
    settings: Settings | None = None,
) -> Verdict:
    """Evaluate one action against the policy and audit the decision.

    When AGT is installed and ``settings.governance_enabled`` is true we
    attempt to delegate to the AGT policy engine; any AGT hiccup falls back to
    the offline policy so governance never becomes a crash point. The decision
    (verdict + rule + action) is always written to the audit trail.

    Args:
        action:   The action request, e.g. ``{\"type\": \"deploy\", \"params\": {}}``.
        settings: App settings; ``governance_enabled=False`` turns the check
            into an unconditional ``allow`` (feature switch, not default).

    Returns:
        The :class:`Verdict` the policy produced.
    """
    if settings is not None and not settings.governance_enabled:
        return Verdict.ALLOW

    action_type = str(action.get("type", ""))
    verdict = _verdict_for(action_type)

    # Delegate to AGT when present; on any failure keep the offline verdict.
    # Fail-closed merge: the strictest verdict wins. AGT may only narrow
    # (deny what the mirror would allow) — it can never widen a mirror deny,
    # so policy drift between the YAML and the mirror cannot open a bypass.
    if AGT_AVAILABLE:
        agt_verdict = _agt_evaluate(action)
        if agt_verdict is not None and _verdict_stricter(agt_verdict, verdict):
            verdict = agt_verdict

    try:
        get_audit_logger().log(
            TraceEvent(
                event_type="governance_decision",
                agent_name="Governance",
                status=verdict.value,
                extra={
                    "action_type": action_type,
                    "rule": f"policy:{action_type}",
                    "verdict": verdict.value,
                    "agt": AGT_AVAILABLE,
                },
            )
        )
    except Exception:
        _logger.debug("Failed to audit governance decision", exc_info=True)

    if verdict != Verdict.ALLOW:
        _logger.warning(
            "Governance %s for action %r", verdict.value, action_type
        )
    return verdict


def _agt_engine() -> Any | None:
    """Return the lazily-built AGT :class:`PolicyEngine`, or ``None``.

    Built once from ``cloudoptima/policies/tools.yaml`` — the same file
    ``agt lint-policy`` validates — so the runtime verdicts come from the
    toolkit's own engine, not a look-alike. A failed load is remembered so we
    do not retry (and spam the logs) on every check.
    """
    global _agt_engine_instance, _agt_engine_failed
    if (
        _agt_engine_instance is not None
        or _agt_engine_failed
        or not AGT_AVAILABLE
    ):
        return _agt_engine_instance
    with _agt_lock:
        if _agt_engine_instance is None and not _agt_engine_failed:
            try:  # pragma: no cover - depends on the installed AGT version
                engine = _PolicyEngine()
                engine.load_yaml_file(str(POLICY_PATH))
                _agt_engine_instance = engine
            except Exception:
                _agt_engine_failed = True
                _logger.debug(
                    "AGT PolicyEngine failed to load — using offline policy", exc_info=True
                )
    return _agt_engine_instance


def _agt_evaluate(action: dict[str, Any]) -> Verdict | None:
    """AGT policy-engine evaluation; ``None`` means "no answer".

    Runs the action through ``agentmesh.governance.PolicyEngine.evaluate``
    (stage ``pre_tool``) with the context shape AGT's condition language
    expects (``action.type`` / ``action.params`` via dot notation). The AGT
    verdict overrides the mirror when AGT answers; on any toolkit hiccup we
    return ``None`` and the offline policy remains authoritative (fail closed).
    """
    engine = _agt_engine()
    if engine is None:
        return None
    try:  # pragma: no cover - depends on the installed AGT version
        decision = engine.evaluate(
            _AGT_AGENT_ID,
            {
                "action": {
                    "type": str(action.get("type", "")),
                    "params": action.get("params", {}),
                }
            },
            stage="pre_tool",
        )
        mapping = {
            "allow": Verdict.ALLOW,
            "deny": Verdict.DENY,
            "require_approval": Verdict.REQUIRE_APPROVAL,
            "warn": Verdict.ALLOW,  # warn = allowed but logged
        }
        return mapping.get(str(getattr(decision, "action", "")))
    except Exception:  # pragma: no cover - defensive
        _logger.debug("AGT evaluation failed — using offline policy", exc_info=True)
        return None


def enforce_action(
    action: dict[str, Any],
    settings: Settings | None = None,
) -> None:
    """Enforce the policy verdict for ``action`` — raises when not allowed.

    Args:
        action:   The action request (see :func:`check_action`).
        settings: App settings.

    Raises:
        GovernanceDeniedError: The policy denied the action (fail closed).
        GovernanceNeedsApprovalError: The action requires human approval first.
    """
    verdict = check_action(action, settings)
    if verdict == Verdict.DENY:
        raise GovernanceDeniedError(
            f"Action denied by policy rule '{action.get('type', '')}' — "
            "destructive operations are not permitted"
        )
    if verdict == Verdict.REQUIRE_APPROVAL:
        raise GovernanceNeedsApprovalError(
            f"Action '{action.get('type', '')}' requires human approval"
        )


def governed_callable(
    func: Any,
    action_type: str,
    settings: Settings | None = None,
) -> Any:
    """Wrap ``func`` so every call is governance-checked before it runs.

    The wrapper enforces the policy verdict before the call runs (fail
    closed). Enforcement goes through :func:`check_action`, which consults
    the AGT ``PolicyEngine`` when the toolkit is installed and always falls
    back to the deterministic mirror — so governance never depends on an
    optional package, and AGT's declarative policy file is what
    ``agt verify`` audits.

    Args:
        func:        The callable to guard.
        action_type: The action type used for policy lookup.
        settings:    App settings (may be ``None`` to use defaults).

    Returns:
        A wrapped callable with the same signature.
    """
    @functools.wraps(func)
    def wrapped(*args: Any, **kwargs: Any) -> Any:
        enforce_action({"type": action_type, "params": kwargs}, settings)
        return func(*args, **kwargs)

    return wrapped


# ── Shared settings helper for modules without a Settings instance ────────
_settings_lock = threading.Lock()
_shared_settings: Settings | None = None


def set_shared_settings(settings: Settings | None) -> None:
    """Point the module at a settings instance (used by the orchestrator)."""
    global _shared_settings
    with _settings_lock:
        _shared_settings = settings


def get_shared_settings() -> Settings | None:
    """Return the settings instance configured via :func:`set_shared_settings`."""
    with _settings_lock:
        return _shared_settings
