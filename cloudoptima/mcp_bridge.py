"""MCP bridge providing tool calls over MCP with registry fallback."""

from __future__ import annotations

import asyncio
import json
import logging
import sys
from typing import Any

from cloudoptima.config import Settings
from cloudoptima.tools import get_registry

_logger = logging.getLogger(__name__)

try:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    MCP_AVAILABLE = True
except Exception:
    MCP_AVAILABLE = False


class MCPBridge:
    """Execute tools via MCP when enabled, else directly through the registry."""

    def __init__(self, settings: Settings | None = None) -> None:
        self._settings = settings

    @property
    def mode(self) -> str:
        """Return 'mcp' when enabled and available, otherwise 'registry'."""
        if (
            self._settings is not None
            and self._settings.mcp_enabled
            and MCP_AVAILABLE
        ):
            return "mcp"
        return "registry"

    # Public API

    def list_tools(self) -> list[dict[str, Any]]:
        """List tool names and descriptions from MCP or the registry."""
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
        """Call a tool; falls back to the registry on MCP errors."""
        if self.mode == "registry":
            result = get_registry().call(name, args or {}, self._settings)
        else:
            try:
                result = asyncio.run(self._call_tool_mcp(name, args or {}))
            except Exception as exc:
                _logger.warning("MCP call %r failed — falling back to registry: %s", name, exc)
                result = get_registry().call(name, args or {}, self._settings)
        
        return self._truncate_result(result)

    def _truncate_result(self, result: dict[str, Any], max_len: int = 4000) -> dict[str, Any]:
        """Truncate large tool responses to preserve LLM context window."""
        res_data = result.get("result")
        if res_data is None:
            return result
            
        try:
            dumped = json.dumps(res_data)
        except (TypeError, ValueError):
            dumped = str(res_data)
            
        if len(dumped) > max_len:
            _logger.info("Truncating tool result (%d bytes)", len(dumped))
            truncated = dumped[:max_len] + "... [TRUNCATED to preserve context]"
            result["result"] = truncated
            result["truncated"] = True
            
        return result

    # MCP transport internals

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
    """Build a tool bridge for the given settings."""
    return MCPBridge(settings)


def call_tool(
    name: str,
    args: dict[str, Any] | None = None,
    settings: Settings | None = None,
) -> dict[str, Any]:
    """Execute a single tool call through the bridge."""
    return MCPBridge(settings).call_tool(name, args)
