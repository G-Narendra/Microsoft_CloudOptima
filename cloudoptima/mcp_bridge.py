"""MCP bridge (issue #7) — tool calls over MCP, with a registry fallback.

:class:`MCPBridge` gives callers one entry point for tools regardless of
transport:

- ``mode == "mcp"`` — a stdio client session talks to
  :mod:`cloudoptima.mcp_server` (needs ``settings.mcp_enabled`` and the
  optional ``mcp`` package).
- ``mode == "registry"`` — calls execute directly through the in-process
  :class:`cloudoptima.tools.ToolRegistry` (same tools, same governance).

The bridge **never raises**: any MCP failure (missing package, subprocess
error, timeouts) degrades to the registry for that call, so tool execution
has no new failure mode.
"""

from __future__ import annotations

import asyncio
import json
import logging
import sys
from typing import Any

from cloudoptima.config import Settings
from cloudoptima.tools import get_registry

_logger = logging.getLogger(__name__)

try:  # pragma: no cover - exercised only when the mcp package is installed
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    MCP_AVAILABLE = True
except Exception:  # pragma: no cover - exercised only when the package is missing
    MCP_AVAILABLE = False


class MCPBridge:
    """Execute tools via MCP when enabled, else directly through the registry."""

    def __init__(self, settings: Settings | None = None) -> None:
        self._settings = settings

    @property
    def mode(self) -> str:
        """``\"mcp\"`` when enabled + available, otherwise ``\"registry\"``."""
        if (
            self._settings is not None
            and self._settings.mcp_enabled
            and MCP_AVAILABLE
        ):
            return "mcp"
        return "registry"

    # ── Public API ──────────────────────────────────────────────────

    def list_tools(self) -> list[dict[str, Any]]:
        """Tool names + descriptions, from MCP or the registry."""
        specs = get_registry().list_tools()
        fallback = [
            {
                "name": spec.name,
                "description": spec.description,
                "parameters": spec.parameters,
            }
            for spec in specs
        ]
        if self.mode == "registry":
            return fallback
        try:
            result = asyncio.run(self._list_tools_mcp())
            return result or fallback
        except Exception as exc:
            _logger.warning("MCP list_tools failed — using registry: %s", exc)
            return fallback

    def call_tool(
        self,
        name: str,
        args: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Call one tool; never raises (MCP errors fall back to the registry)."""
        if self.mode == "registry":
            return get_registry().call(name, args or {}, self._settings)
        try:
            return asyncio.run(self._call_tool_mcp(name, args or {}))
        except Exception as exc:
            _logger.warning("MCP call %r failed — falling back to registry: %s", name, exc)
            return get_registry().call(name, args or {}, self._settings)

    # ── MCP transport (async internals) ─────────────────────────────

    @staticmethod
    def _server_params() -> StdioServerParameters:
        return StdioServerParameters(
            command=sys.executable,
            args=["-m", "cloudoptima.mcp_server"],
        )

    async def _list_tools_mcp(self) -> list[dict[str, Any]]:
        async with stdio_client(self._server_params()) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                result = await session.list_tools()
                return [
                    {"name": tool.name, "description": tool.description, "parameters": {}}
                    for tool in result.tools
                ]

    async def _call_tool_mcp(self, name: str, args: dict[str, Any]) -> dict[str, Any]:
        async with stdio_client(self._server_params()) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                tools = await session.list_tools()
                if not any(tool.name == name for tool in tools.tools):
                    return {
                        "ok": False,
                        "tool": name,
                        "error": "tool not exposed by the MCP server",
                        "result": None,
                    }
                result = await session.call_tool(name, arguments=args)
                text = "".join(
                    part.text for part in result.content if hasattr(part, "text")
                )
                try:
                    parsed: Any = json.loads(text) if text.strip() else None
                except json.JSONDecodeError:
                    parsed = text
                return {"ok": True, "tool": name, "result": parsed, "source": "mcp"}


def get_tool_executor(settings: Settings | None = None) -> MCPBridge:
    """Convenience — build a bridge for the given settings."""
    return MCPBridge(settings)


def call_tool(
    name: str,
    args: dict[str, Any] | None = None,
    settings: Settings | None = None,
) -> dict[str, Any]:
    """One-shot tool call through the bridge (MCP or registry)."""
    return MCPBridge(settings).call_tool(name, args)
