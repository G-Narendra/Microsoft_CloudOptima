"""Tests for MCP bridge."""

import json
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from cloudoptima.config import Settings
from cloudoptima.mcp_bridge import MCPBridge, get_tool_executor, call_tool

def test_list_tools_registry_fallback():
    bridge = MCPBridge()
    with patch.object(MCPBridge, "mode", "registry"):
        tools = bridge.list_tools()
        assert len(tools) > 0
        assert "name" in tools[0]

def test_list_tools_mcp_exception():
    bridge = MCPBridge()
    with patch.object(MCPBridge, "mode", "mcp"), patch.object(MCPBridge, "_list_tools_mcp", side_effect=Exception("mcp fail")):
        tools = bridge.list_tools()
        assert len(tools) > 0

def test_call_tool_mcp_exception():
    bridge = MCPBridge()
    with patch.object(MCPBridge, "mode", "mcp"), patch.object(MCPBridge, "_call_tool_mcp", side_effect=Exception("mcp fail")):
        # Mock registry fallback
        with patch("cloudoptima.mcp_bridge.get_registry") as mock_reg:
            mock_reg.return_value.call.return_value = {"result": "registry_fallback"}
            res = bridge.call_tool("test_tool")
            assert res["result"] == "registry_fallback"

def test_truncate_result():
    bridge = MCPBridge()
    
    # None result
    assert bridge._truncate_result({"result": None}) == {"result": None}
    
    # Not serializable -> str
    class NotSerializable:
        def __str__(self): return "x" * 5000
    
    res = bridge._truncate_result({"result": NotSerializable()})
    assert len(res["result"]) < 4100
    assert "TRUNCATED" in res["result"]
    
    # Huge string JSON
    res = bridge._truncate_result({"result": "x" * 5000})
    assert len(res["result"]) < 4100
    assert "TRUNCATED" in res["result"]

@pytest.mark.asyncio
async def test_call_tool_mcp_internals():
    bridge = MCPBridge()
    
    with patch("cloudoptima.mcp_bridge.stdio_client") as mock_stdio, \
         patch("cloudoptima.mcp_bridge.ClientSession") as mock_client:
         
         mock_stdio.return_value.__aenter__.return_value = (MagicMock(), MagicMock())
         
         mock_session = AsyncMock()
         mock_client.return_value.__aenter__.return_value = mock_session
         
         # Mock list tools to not include our tool
         mock_tools = MagicMock()
         mock_tools.tools = [MagicMock(name="other_tool")]
         mock_session.list_tools.return_value = mock_tools
         
         # Tool not found
         res = await bridge._call_tool_mcp("missing_tool", {})
         assert res["ok"] is False
         assert "not exposed" in res["error"]
         
         # Decode error
         mock_tools.tools = [MagicMock(name="test_tool")]
         mock_tools.tools[0].name = "test_tool"
         
         mock_result = MagicMock()
         mock_part = MagicMock()
         mock_part.text = "invalid json"
         mock_result.content = [mock_part]
         mock_session.call_tool.return_value = mock_result
         
         res = await bridge._call_tool_mcp("test_tool", {})
         assert res["result"] == "invalid json"

def test_convenience_functions():
    with patch("cloudoptima.mcp_bridge.MCPBridge") as mock_bridge:
        mock_instance = MagicMock()
        mock_bridge.return_value = mock_instance
        
        get_tool_executor()
        assert mock_bridge.called
        
        call_tool("test_tool")
        mock_instance.call_tool.assert_called_with("test_tool", None)
