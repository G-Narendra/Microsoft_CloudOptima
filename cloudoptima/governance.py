"""Action governance enforcing policies before tool execution."""

from __future__ import annotations

from enum import StrEnum
import functools
import logging
from pathlib import Path
import threading
from typing import Any, Final

from cloudoptima.config import Settings
from cloudoptima.observability import AuditLogger, TraceEvent

_logger = logging.getLogger(__name__)

# Optional Agent Governance Toolkit import
try:
    from agentmesh.governance import PolicyEngine
    AGT_AVAILABLE = True
except Exception:
    AGT_AVAILABLE = False
    PolicyEngine = None  # type: ignore

_AGT_AVAILABLE = AGT_AVAILABLE

POLICY_PATH: Final[Path] = Path(__file__).parent / "policies" / "tools.yaml"
_AGT_AGENT_ID: Final[str] = "cloudoptima"

_agt_engine_instance: Any | None = None
_agt_engine_failed: bool = False
_agt_lock = threading.Lock()


class Verdict(StrEnum):
    """The three verdicts the policy can return for an action."""

    ALLOW = "allow"
    DENY = "deny"
    REQUIRE_APPROVAL = "require_approval"


class GovernanceDeniedError(Exception):
    """Raised when the policy denies an action."""

    def __init__(self, message: str, verdict: Verdict = Verdict.DENY) -> None:
        super().__init__(message)
        self.verdict = verdict


class GovernanceNeedsApprovalError(Exception):
    """Raised when an action requires human approval before execution."""


_VERDICT_STRICTNESS: Final[dict[Verdict, int]] = {
    Verdict.ALLOW: 0,
    Verdict.REQUIRE_APPROVAL: 1,
    Verdict.DENY: 2,
}


def _verdict_stricter(candidate: Verdict, current: Verdict) -> bool:
    """True when candidate is stricter than current (deny > approval > allow)."""
    return _VERDICT_STRICTNESS[candidate] > _VERDICT_STRICTNESS[current]


# Offline policy mirror (fail closed for any undeclared action)
_POLICY: Final[dict[str, Verdict]] = {
    "get_live_price": Verdict.ALLOW,
    "compliance_lookup": Verdict.ALLOW,
    "list_regions": Verdict.ALLOW,
    "send_email": Verdict.DENY,
    "deploy": Verdict.DENY,
    "create": Verdict.DENY,
    "delete": Verdict.DENY,
    "drop": Verdict.DENY,
    "shell": Verdict.DENY,
}


def _verdict_for(action_type: str) -> Verdict:
    """Look up the policy verdict for an action type (unknown defaults to deny)."""
    return _POLICY.get(action_type, Verdict.DENY)


def check_action(
    action: dict[str, Any],
    settings: Settings | None = None,
    logger: AuditLogger | None = None,
) -> Verdict:
    """Evaluate an action against the policy and audit the decision."""
    if settings is not None and not settings.governance_enabled:
        return Verdict.ALLOW

    action_type = str(action.get("type", ""))
    verdict = _verdict_for(action_type)

    is_avail = globals().get("_AGT_AVAILABLE", AGT_AVAILABLE)
    if is_avail:
        agt_verdict = _agt_evaluate(action)
        if agt_verdict is not None and _verdict_stricter(agt_verdict, verdict):
            verdict = agt_verdict

    if logger:
        try:
            logger.log(
                TraceEvent(
                    event_type="governance_decision",
                    agent_name="Governance",
                    status=verdict.value,
                    extra={
                        "action_type": action_type,
                        "rule": f"policy:{action_type}",
                        "verdict": verdict.value,
                        "agt": is_avail,
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
    """Return the lazily-built AGT PolicyEngine, or None."""
    global _agt_engine_instance, _agt_engine_failed
    is_avail = globals().get("_AGT_AVAILABLE", AGT_AVAILABLE)
    pe_cls = globals().get("PolicyEngine", None)
    if not is_avail or pe_cls is None:
        return None
    if _agt_engine_instance is not None and getattr(_agt_engine_instance, "__class__", None) is pe_cls:
        return _agt_engine_instance
    with _agt_lock:
        try:
            engine = pe_cls()
            if hasattr(engine, "load_yaml_file"):
                engine.load_yaml_file(str(POLICY_PATH))
            _agt_engine_instance = engine
            return _agt_engine_instance
        except Exception:
            _agt_engine_failed = True
            _logger.debug(
                "AGT PolicyEngine failed to load — using offline policy", exc_info=True
            )
            return None


def _agt_evaluate(action: dict[str, Any]) -> Verdict | None:
    """Evaluate action through AGT policy engine."""
    engine = _agt_engine()
    if engine is None:
        return None
    try:
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
        action_val = str(getattr(decision, "action", "")).lower()
        if hasattr(getattr(decision, "action", None), "value"):
            action_val = str(decision.action.value).lower()
        mapping = {
            "allow": Verdict.ALLOW,
            "deny": Verdict.DENY,
            "require_approval": Verdict.REQUIRE_APPROVAL,
            "warn": Verdict.ALLOW,
        }
        return mapping.get(action_val)
    except Exception:
        _logger.debug("AGT evaluation failed — using offline policy", exc_info=True)
        return None


def enforce_action(
    action: dict[str, Any],
    settings: Settings | None = None,
    logger: AuditLogger | None = None,
) -> None:
    """Enforce the policy verdict for action — raises when not allowed."""
    verdict = check_action(action, settings, logger)
    if verdict == Verdict.DENY:
        raise GovernanceDeniedError(
            f"Action denied by policy rule '{action.get('type', '')}' — "
            "destructive operations are not permitted",
            verdict=Verdict.DENY,
        )
    if verdict == Verdict.REQUIRE_APPROVAL:
        raise GovernanceNeedsApprovalError(
            f"Action '{action.get('type', '')}' requires human approval"
        )


def governed_callable(
    action_or_func: Any,
    func_or_action: Any = None,
    settings: Settings | None = None,
) -> Any:
    """Wrap func so every call is governance-checked before execution."""
    if callable(action_or_func) and isinstance(func_or_action, str):
        func = action_or_func
        action_type = func_or_action
    elif isinstance(action_or_func, str) and callable(func_or_action):
        action_type = action_or_func
        func = func_or_action
    else:
        func = action_or_func
        action_type = str(func_or_action)

    @functools.wraps(func)
    def wrapped(*args: Any, **kwargs: Any) -> Any:
        enforce_action({"type": action_type, "params": kwargs}, settings)
        return func(*args, **kwargs)

    return wrapped


# Shared settings helper
_settings_lock = threading.Lock()
_shared_settings: Settings | None = None


def set_shared_settings(settings: Settings | None) -> None:
    """Point the module at a settings instance."""
    global _shared_settings
    with _settings_lock:
        _shared_settings = settings


def get_shared_settings() -> Settings | None:
    """Return configured settings instance."""
    with _settings_lock:
        return _shared_settings
