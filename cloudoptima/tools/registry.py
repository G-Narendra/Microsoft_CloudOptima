"""Tool registry providing deterministic tool execution for agents."""

from __future__ import annotations

import json
import logging
import threading
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, Final

from cloudoptima.compliance.rag import ComplianceRAG
from cloudoptima.config import Settings
from cloudoptima.governance import enforce_action
from cloudoptima.models import AzureRegion
import cloudoptima.pricing.azure_api as azure_api
import cloudoptima.pricing.static_db as static_db
from cloudoptima.sanitize import clean_output, detect_injection, scan_llm_output

_logger = logging.getLogger(__name__)

# Execution timeout in seconds for tools
TOOL_TIMEOUT_SECONDS: Final[float] = 15.0

# Parameter type checks used to validate tool arguments against schemas
_TYPE_CHECKS: Final[dict[str, Callable[[Any], bool]]] = {
    "string": lambda v: isinstance(v, str),
    "integer": lambda v: isinstance(v, int) and not isinstance(v, bool),
    "number": lambda v: isinstance(v, (int, float)) and not isinstance(v, bool),
    "boolean": lambda v: isinstance(v, bool),
}


@dataclass(frozen=True)
class ToolSpec:
    """Metadata and callable for a registered tool."""

    name: str
    description: str
    func: Callable[..., Any] = field(compare=False, repr=False)
    parameters: dict[str, Any] = field(default_factory=dict)
    action_type: str = ""

    @property
    def governance_type(self) -> str:
        """The action type used for policy checks."""
        return self.action_type or self.name


class ToolRegistry:
    """Thread-safe registry of tools with governed, sanitized execution."""

    def __init__(self) -> None:
        self._tools: dict[str, ToolSpec] = {}
        self._lock = threading.Lock()

    def register(
        self,
        name: str,
        description: str,
        func: Callable[..., Any],
        parameters: dict[str, Any] | None = None,
        action_type: str = "",
    ) -> ToolSpec:
        """Register a tool in the registry."""
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
        """Return all registered tools in registration order."""
        with self._lock:
            return list(self._tools.values())

    def get(self, name: str) -> ToolSpec | None:
        """Return a tool spec by name, or None when unknown."""
        with self._lock:
            return self._tools.get(name)

    def call(
        self,
        name: str,
        args: dict[str, Any] | None = None,
        settings: Settings | None = None,
        logger: Any = None,
    ) -> dict[str, Any]:
        """Execute a tool with governance checks and output sanitization."""
        spec = self.get(name)
        if spec is None:
            return {"ok": False, "tool": name, "error": f"unknown tool: {name}", "result": None}

        try:
            enforce_action({"type": spec.governance_type, "params": args or {}}, settings, logger)
        except Exception as exc:
            return {
                "ok": False,
                "tool": name,
                "error": str(exc),
                "result": None,
            }

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

        try:
            text = json.dumps(result, ensure_ascii=False, default=str)
        except (TypeError, ValueError) as exc:
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
        except json.JSONDecodeError:
            cleaned = cleaned_text
        return {"ok": True, "tool": name, "result": cleaned, "source": "registry"}

    @staticmethod
    def _validate_args(
        spec: ToolSpec, args: dict[str, Any]
    ) -> tuple[dict[str, Any] | None, str | None]:
        """Merge defaults and validate args against parameter schema."""
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


# Timeout helper

def _call_with_timeout(func: Callable[..., Any], args: dict[str, Any], timeout: float) -> Any:
    """Call func(**args) on a daemon thread and enforce timeout."""
    box: dict[str, Any] = {}

    def runner() -> None:
        try:
            box["value"] = func(**args)
        except BaseException as exc:
            box["error"] = exc

    thread = threading.Thread(target=runner, daemon=True, name="cloudoptima-tool")
    thread.start()
    thread.join(timeout=timeout)
    if thread.is_alive():
        raise TimeoutError(
            f"tool exceeded the {timeout:.0f}s execution limit and was abandoned"
        )
    if "error" in box:
        raise box["error"]
    return box["value"]


# Built-in tools

def _get_live_price(service: str, region: str = "uaenorth") -> dict[str, Any]:
    """Retrieve live Azure retail price for service in region with static fallback."""
    result = azure_api.get_price_with_unit(service, region)
    if result is not None:
        price, unit = result
        return {
            "service": service,
            "region": region,
            "price": price,
            "unit": unit,
            "source": "azure_retail_api",
        }
    fallback = static_db.lookup(service)
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
    """Retrieve compliance guidance passages using RAG."""
    top_k = max(1, min(int(top_k), 5))
    rag = ComplianceRAG(Settings())
    passages = rag.query_rag(query, framework, top_k)
    return {"query": query, "framework": framework, "passages": passages}


def _list_regions() -> dict[str, Any]:
    """List supported Azure regions."""
    return {"regions": [region.value for region in AzureRegion]}


def build_default_registry() -> ToolRegistry:
    """Create and configure default tool registry with built-in tools."""
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


# Singleton instance
_registry: ToolRegistry | None = None
_registry_lock = threading.Lock()


def get_registry() -> ToolRegistry:
    """Return the process-wide ToolRegistry singleton."""
    global _registry
    if _registry is None:
        with _registry_lock:
            if _registry is None:
                _registry = build_default_registry()
    return _registry
