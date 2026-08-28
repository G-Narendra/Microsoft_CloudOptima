"""Tests for MCP server."""

import sys
import pytest
from unittest.mock import patch, MagicMock

from cloudoptima.mcp_server import main, create_server
import cloudoptima.mcp_server as mcp_server_module

def test_create_server_not_available():
    with patch.object(mcp_server_module, "MCP_AVAILABLE", False):
        assert create_server() is None

def test_main_not_available(capsys):
    with patch("cloudoptima.mcp_server.create_server", return_value=None):
        assert main() == 1
        assert "not installed" in capsys.readouterr().err

def test_main_available():
    mock_server = MagicMock()
    with patch("cloudoptima.mcp_server.create_server", return_value=mock_server):
        assert main() == 0
        mock_server.run.assert_called_with("stdio")


