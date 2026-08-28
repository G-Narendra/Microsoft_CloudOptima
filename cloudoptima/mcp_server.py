"""MCP server exposing tool registry over Model Context Protocol."""

from __future__ import annotations

import logging
import sys
from typing import Any

from cloudoptima.config import Settings
from cloudoptima.governance import governed_callable
from cloudoptima.tools import get_registry

_logger = logging.getLogger(__name__)

# Support both modern MCP 2.x and legacy 1.x FastMCP
try:
    from mcp.server.mcpserver import MCPServer
    _SERVER_CLS: Any = MCPServer
    MCP_AVAILABLE = True
except Exception:
    try:
        from mcp.server.fastmcp import FastMCP
        _SERVER_CLS = FastMCP
        MCP_AVAILABLE = True
    except Exception:
        _SERVER_CLS = None
        MCP_AVAILABLE = False

SERVER_NAME: str = "cloudoptima"


def create_server(settings: Settings | None = None) -> Any | None:
    """Build an MCP server over the tool registry."""
    if not MCP_AVAILABLE:
        return None
    server = _SERVER_CLS(SERVER_NAME)
    for spec in get_registry().list_tools():
        server.add_tool(
            governed_callable(spec.func, spec.governance_type, settings),
            name=spec.name,
            description=spec.description,
        )
    return server


def main() -> int:
    """Run the MCP server on stdio until the client disconnects."""
    server = create_server()
    if server is None:
        print(
            "mcp package not installed — run: pip install 'mcp[cli]'",
            file=sys.stderr,
        )
        return 1
    server.run("stdio")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
