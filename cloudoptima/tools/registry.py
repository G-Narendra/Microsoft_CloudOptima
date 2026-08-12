"""Tool registry (issue #7) — the deterministic tool layer agents can call.

Tools are plain Python functions (no LLM in the loop) wrapping existing
modules: live pricing, compliance lookup, and region listing. Every tool
output is treated as **untrusted** — it is serialized, cleaned, and
injection-scanned before it can reach a prompt or the UI (the same rule the
RAG module applies to retrieved passages).

Execution order inside :meth:`ToolRegistry.call`:

1. **Governance** — :func:`cloudoptima.governance.enforce_action` checks the
   tool's action type against the policy (fail closed).
2. **Run** — the tool function executes (read-only lookups only today).
3. **Sanitize** — the output is scanned with :func:`scan_llm_output` and
   :func:`detect_injection`; a flagged result is withheld, never returned.

The registry is the in-process backend. :mod:`cloudoptima.mcp_server` exposes
the same tools over the Model Context Protocol, and
:mod:`cloudoptima.mcp_bridge` picks between the two transports.
"""

from __future__ import annotations

import json
import logging
import threading
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, Final

from cloudoptima.config import Settings
from cloudoptima.governance import enforce_action
from cloudoptima.sanitize import clean_output, detect_injection, scan_llm_output

_logger = logging.getLogger(__name__)

#: Tools must answer within this many seconds or the call fails. The LLM
#: clients have timeouts; the tools need the same guarantee — a hung pricing
#: API call or slow RAG query must never block the pipeline indefinitely
#: (external principal-engineer review finding).
TOOL_TIMEOUT_SECONDS: Final[float] = 15.0

#: Parameter type checks used to validate tool arguments against the declared
#: schema before execution (booleans are deliberately excluded from "number").
_TYPE_CHECKS: Final[dict[str, Callable[[Any], bool]]] = {
    "string": lambda v: isinstance(v, str),
    "integer": lambda v: isinstance(v, int) and not isinstance(v, bool),
    "number": lambda v: isinstance(v, (int, float)) and not isinstance(v, bool),
    "boolean": lambda v: isinstance(v, bool),
}


@dataclass(frozen=True)
class ToolSpec:
    """Metadata + callable for one registered tool.

    Attributes:
        name:        Unique tool name (also the action type for governance).
        description: What the tool does, shown to models and in listings.
        parameters:  JSON-schema-ish parameter map: name ->
            ``{\"type\": ..., \"required\": bool, \"default\": ..., \"description\": ...}``.
        action_type: The governance action type (defaults to ``name``).
        func:        The callable implementing the tool.
    """

    name: str
    description: str
    func: Callable[..., Any] = field(compare=False, repr=False)
    parameters: dict[str, Any] = field(default_factory=dict)
    action_type: str = ""

    @property
    def governance_type(self) -> str:
        """The action type used for policy checks (defaults to the tool name)."""
        return self.action_type or self.name


class ToolRegistry:
    """Thread-safe registry of tools with governed, sanitized execution."""

    def __init__(self) -> None:
        self._tools: dict[str, ToolSpec] = {}
        self._lock = threading.Lock()

    # ── Registration ────────────────────────────────────────────────

    def register(
        self,
        name: str,
        description: str,
        func: Callable[..., Any],
        parameters: dict[str, Any] | None = None,
        action_type: str = "",
    ) -> ToolSpec:
        """Register a tool; replacing an existing name is an error.

        Raises:
            ValueError: If ``name`` is already registered.
        """
        with self._lock:
            if name in self._tools:
                raise ValueError(f"tool already registered: {name}")
            spec = ToolSpec(
                name=name,
                description=description,
                parameters=parameters or {},
                action_type=action_type,
                func=func,
            )
            self._tools[name] = spec
            return spec

    def list_tools(self) -> list[ToolSpec]:
        """All registered tools in registration order."""
        with self._lock:
            return list(self._tools.values())

    def get(self, name: str) -> ToolSpec | None:
        """Return a tool spec by name, or ``None`` when unknown."""
        with self._lock:
            return self._tools.get(name)

    # ── Execution ───────────────────────────────────────────────────

    def call(
        self,
        name: str,
        args: dict[str, Any] | None = None,
        settings: Settings | None = None,
    ) -> dict[str, Any]:
        """Execute one tool with governance + output sanitization.

        Never raises: every failure path returns ``{\"ok\": False, ...}`` so the
        caller (orchestrator, dashboard, MCP server) can degrade gracefully.

        Args:
            name:     Tool name.
            args:     Keyword arguments for the tool.
            settings: App settings (governance + feature toggles).

        Returns:
            ``{\"ok\": True, \"tool\": name, \"result\": <value>, \"source\": \"registry\"}``
            on success, or ``{\"ok\": False, \"tool\": name, \"error\": ...}`` when
            the tool is unknown, the policy denies it, it raises, or its
            output was withheld as suspicious.
        """
        spec = self.get(name)
        if spec is None:
            return {"ok": False, "tool": name, "error": f"unknown tool: {name}", "result": None}

        #        # Governance first — a denied action never reaches the tool.
        try:
            enforce_action({"type": spec.governance_type, "params": args or {}}, settings)
        except Exception as exc:
            return {
                "ok": False,
                "tool": name,
                "error": str(exc),
                "result": None,
            }

        # Validate the arguments against the tool's declared parameter schema
        # BEFORE execution: a model passing {"service": 42} must be rejected at
        # the schema layer, not explode inside the tool function (external
        # principal-engineer review finding).
        effective_args, arg_error = self._validate_args(spec, args or {})
        if arg_error is not None:
            return {
                "ok": False,
                "tool": name,
                "error": f"invalid arguments: {arg_error}",
                "result": None,
            }

        try:
            result = _call_with_timeout(
                spec.func, effective_args or {}, TOOL_TIMEOUT_SECONDS
            )
        except TimeoutError as exc:
            _logger.warning("Tool %r timed out after %ss", name, TOOL_TIMEOUT_SECONDS)
            return {"ok": False, "tool": name, "error": str(exc), "result": None}
        except Exception as exc:
            _logger.warning("Tool %r raised: %s", name, exc)
            return {"ok": False, "tool": name, "error": f"tool failed: {exc}", "result": None}


        # Tool output is untrusted: serialize, clean, scan, withhold on flags.
        try:
            text = json.dumps(result, ensure_ascii=False, default=str)
        except (TypeError, ValueError) as exc:  # pragma: no cover - defensive
            return {
                "ok": False,
                "tool": name,
                "error": f"output not serializable: {exc}",
                "result": None,
            }

        flags = scan_llm_output(text)
        if flags or detect_injection(text):
            _logger.warning(
                "Tool %r output withheld — suspicious content: %s",
                name,
                flags or ["injection"],
            )
            return {
                "ok": False,
                "tool": name,
                "error": "tool output withheld (suspicious content)",
                "result": None,
            }

        cleaned_text = clean_output(text)
        try:
            cleaned: Any = json.loads(cleaned_text)
        except json.JSONDecodeError:  # pragma: no cover - defensive
            cleaned = cleaned_text
        return {"ok": True, "tool": name, "result": cleaned, "source": "registry"}

    # ── Argument validation & timeout helpers ─────────────────────────

    @staticmethod
    def _validate_args(
        spec: ToolSpec, args: dict[str, Any]
    ) -> tuple[dict[str, Any] | None, str | None]:
        """Merge defaults and validate ``args`` against the parameter schema.

        Args:
            spec: The tool specification (its ``parameters`` map).
            args: Raw keyword arguments from the caller (model, user, test).

        Returns:
            ``(effective_args, None)`` when valid — declared defaults filled
            in — or ``(None, error_message)`` when a required parameter is
            missing or a value has the wrong type. Tools without a parameter
            schema accept anything (schema-less helpers like ``list_regions``).
        """
        schema = spec.parameters or {}
        effective = dict(args)
        for name, meta in schema.items():
            meta = meta if isinstance(meta, dict) else {}
            if name not in effective:
                if meta.get("required", False):
                    return None, f"missing required parameter '{name}'"
                default = meta.get("default")
                if default is not None:
                    effective[name] = default
                continue
            expected = str(meta.get("type", "string"))
            checker = _TYPE_CHECKS.get(expected)
            if checker is not None and not checker(effective[name]):
                return (
                    None,
                    f"parameter '{name}' must be {expected}, "
                    f"got {type(effective[name]).__name__}",
                )
        return effective, None


# ── Timeout execution ─────────────────────────────────────────────────────


def _call_with_timeout(func: Callable[..., Any], args: dict[str, Any], timeout: float) -> Any:
    """Call ``func(**args)`` on a daemon thread and enforce ``timeout``.

    A tool that hangs (slow pricing API, blocking RAG query) must never block
    the pipeline: the call runs on a daemon thread and the caller waits at
    most ``timeout`` seconds. On timeout the thread is left to finish in the
    background — daemon threads never block interpreter exit — and the call
    raises :class:`TimeoutError`. Exceptions raised inside the tool propagate
    to the caller unchanged.

    Args:
        func:    The tool callable.
        args:    Keyword arguments for the call.
        timeout: Seconds to wait before giving up.

    Returns:
        The tool's return value.

    Raises:
        TimeoutError: The tool did not return within ``timeout`` seconds.
    """
    box: dict[str, Any] = {}

    def runner() -> None:
        try:
            box["value"] = func(**args)
        except BaseException as exc:  # propagate any failure to the caller
            box["error"] = exc

    thread = threading.Thread(target=runner, daemon=True, name="cloudoptima-tool")
    thread.start()
    thread.join(timeout=timeout)
    if thread.is_alive():
        raise TimeoutError(
            f"tool exceeded the {timeout:.0f}s execution limit and was abandoned"
        )
    if "error" in box:
        # The runner only ever stores a BaseException under "error".
        raise box["error"]
    return box["value"]


# ── Built-in tools ───────────────────────────────────────────────────────


def _get_live_price(service: str, region: str = "uaenorth") -> dict[str, Any]:
    """Live Azure retail price for ``service`` in ``region`` (static fallback).

    Imported lazily so tests can patch the source modules without touching
    this registry.
    """
    from cloudoptima.pricing.azure_api import get_price_with_unit
    from cloudoptima.pricing.static_db import lookup

    result = get_price_with_unit(service, region)
    if result is not None:
        price, unit = result
        return {
            "service": service,
            "region": region,
            "price": price,
            "unit": unit,
            "source": "azure_retail_api",
        }
    fallback = lookup(service)
    if fallback is not None:
        return {
            "service": service,
            "region": region,
            "price": fallback,
            "unit": "unit",
            "source": "static_catalog",
        }
    return {
        "service": service,
        "region": region,
        "price": None,
        "unit": "",
        "source": "unknown",
    }


def _compliance_lookup(query: str, framework: str = "", top_k: int = 3) -> dict[str, Any]:
    """Retrieve compliance guidance passages for a question (RAG lookup)."""
    from cloudoptima.compliance.rag import query_rag

    top_k = max(1, min(int(top_k), 5))
    passages = query_rag(query, framework, top_k)
    return {"query": query, "framework": framework, "passages": passages}


def _list_regions() -> dict[str, Any]:
    """All Azure regions CloudOptima lets users target."""
    from cloudoptima.models import AzureRegion

    return {"regions": [region.value for region in AzureRegion]}


def build_default_registry() -> ToolRegistry:
    """Registry pre-loaded with the built-in read-only tools."""
    registry = ToolRegistry()
    registry.register(
        "get_live_price",
        "Look up the live Azure retail price for a service in a region. "
        "Returns the price, its unit, and whether it came from the live API "
        "or the static catalog.",
        _get_live_price,
        parameters={
            "service": {
                "type": "string",
                "required": True,
                "description": "Azure service name, e.g. 'Virtual Machines'",
            },
            "region": {
                "type": "string",
                "required": False,
                "default": "uaenorth",
                "description": "ARM region name, e.g. 'uaenorth' or 'eastus'",
            },
        },
        action_type="get_live_price",
    )
    registry.register(
        "compliance_lookup",
        "Retrieve relevant compliance guidance passages for a question, "
        "optionally filtered by framework (pdpl/hipaa/soc2/iso27001/gdpr).",
        _compliance_lookup,
        parameters={
            "query": {
                "type": "string",
                "required": True,
                "description": "The compliance question to look up",
            },
            "framework": {
                "type": "string",
                "required": False,
                "default": "",
                "description": "Optional framework filter",
            },
            "top_k": {
                "type": "integer",
                "required": False,
                "default": 3,
                "description": "Max passages to return (1-5)",
            },
        },
        action_type="compliance_lookup",
    )
    registry.register(
        "list_regions",
        "List the Azure regions CloudOptima supports.",
        _list_regions,
        action_type="list_regions",
    )
    return registry


# ── Singleton ─────────────────────────────────────────────────────────────
_registry: ToolRegistry | None = None
_registry_lock = threading.Lock()


def get_registry() -> ToolRegistry:
    """Return the process-wide :class:`ToolRegistry` (lazily built)."""
    global _registry
    if _registry is None:
        with _registry_lock:
            if _registry is None:
                _registry = build_default_registry()
    return _registry
