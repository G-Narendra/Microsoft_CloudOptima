"""MCP server — expose the tool registry over the Model Context Protocol.

Issue #7: this module turns CloudOptima's deterministic tools (live pricing,
compliance lookup, region listing) into MCP tools, so any MCP-capable agent
or client — including our own :mod:`cloudoptima.mcp_bridge` — can call them
through the standard protocol.

Two SDK generations are supported so the server works whether the optional
``mcp`` extra resolves to the current 2.x line (``MCPServer``) or an older
1.x install (``FastMCP``):

- ``from mcp.server.mcpserver import MCPServer``   (MCP 2.x, Aug 2026)
- ``from mcp.server.fastmcp import FastMCP``       (MCP 1.x legacy)

Both expose ``add_tool(fn, name=..., description=...)`` and ``run(\"stdio\")``,
so one code path covers either. Without the ``mcp`` package at all,
:func:`create_server` returns ``None`` and the registry fallback in
:mod:`cloudoptima.mcp_bridge` keeps everything working.

Run the server standalone (stdio transport):

    $ python -m cloudoptima.mcp_server
"""

from __future__ import annotations

import logging
import sys
from typing import Any

from cloudoptima.config import Settings
from cloudoptima.governance import governed_callable
from cloudoptima.tools import get_registry

_logger = logging.getLogger(__name__)

# MCP 2.x (current line) first, then 1.x legacy FastMCP. Tool schema is
# derived from the function signature in both, so governed wrappers must
# preserve signatures (functools.wraps in governance.governed_callable).
try:  # pragma: no cover - exercised only when mcp is installed
    from mcp.server.mcpserver import MCPServer

    _SERVER_CLS: Any = MCPServer
    MCP_AVAILABLE = True
except Exception:  # pragma: no cover - exercised only when mcp is missing
    try:  # pragma: no cover - exercised only when only 1.x is installed
        from mcp.server.fastmcp import FastMCP

        _SERVER_CLS = FastMCP
        MCP_AVAILABLE = True
    except Exception:
        _SERVER_CLS = None
        MCP_AVAILABLE = False

#: Server name clients see in the MCP handshake.
SERVER_NAME: str = "cloudoptima"


def create_server(settings: Settings | None = None) -> Any | None:
    """Build an MCP server over the tool registry.

    Every tool is registered through :func:`governed_callable` so calls that
    arrive over MCP are still checked against the action policy (issue #5) —
    governance applies no matter which transport the call used.

    Args:
        settings: App settings used for governance (may be ``None``).

    Returns:
        A configured MCP server (``MCPServer`` on 2.x, ``FastMCP`` on 1.x),
        or ``None`` when the optional ``mcp`` package is not installed.
    """
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
