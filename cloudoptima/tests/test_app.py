"""Tests for the app module (CLI entry point)."""

import json
import pytest
from unittest.mock import patch, MagicMock
from io import StringIO
import sys

from cloudoptima.app import main, _configure_utf8_stdio, _read_stdin_payload

def test_main_no_stdin(capsys):
    with patch("sys.stdin.isatty", return_value=True):
        assert main() == 2
        
def test_main_empty_stdin(capsys):
    with patch("sys.stdin.isatty", return_value=False), patch("sys.stdin.read", return_value="   "):
        assert main() == 2

def test_main_invalid_json(capsys):
    with patch("sys.stdin.isatty", return_value=False), patch("sys.stdin.read", return_value="invalid"):
        assert main() == 2
        assert "not valid JSON" in capsys.readouterr().err

def test_main_not_dict(capsys):
    with patch("sys.stdin.isatty", return_value=False), patch("sys.stdin.read", return_value="[]"):
        assert main() == 2
        assert "expected a JSON object" in capsys.readouterr().err

def test_main_validation_error(capsys):
    payload = {"project_name": 123} # Invalid type
    with patch("sys.stdin.isatty", return_value=False), patch("sys.stdin.read", return_value=json.dumps(payload)):
        with patch("cloudoptima.app.create_orchestrator"):
            assert main() == 2
            assert "invalid session JSON" in capsys.readouterr().err

def test_main_success(capsys):
    payload = {"project_name": "test project"}
    with patch("sys.stdin.isatty", return_value=False), patch("sys.stdin.read", return_value=json.dumps(payload)):
        with patch("cloudoptima.app.create_orchestrator") as mock_create:
            mock_orchestrator = MagicMock()
            
            # Need to mock the async run method
            async def mock_run(session):
                session.status = "completed"
                return session
                
            mock_orchestrator.run.side_effect = mock_run
            mock_create.return_value = mock_orchestrator
            
            # Need to mock moderate_input_fields
            with patch("cloudoptima.app.moderate_input_fields", return_value=(payload, ["blocked_field"])):
                assert main() == 0
                out, err = capsys.readouterr()
                assert "blocked input field(s)" in err
                assert "test project" in out

def test_main_run_exception(capsys):
    payload = {"project_name": "test project"}
    with patch("sys.stdin.isatty", return_value=False), patch("sys.stdin.read", return_value=json.dumps(payload)):
        with patch("cloudoptima.app.create_orchestrator") as mock_create:
            mock_orchestrator = MagicMock()
            mock_orchestrator.run.side_effect = Exception("pipeline failed")
            mock_create.return_value = mock_orchestrator
            
            assert main() == 1
            assert "pipeline failed" in capsys.readouterr().err

def test_configure_utf8_stdio():
    # Mock sys.stdout.reconfigure
    mock_stdout = MagicMock()
    mock_stdout.reconfigure = MagicMock()
    
    mock_stderr = MagicMock()
    mock_stderr.reconfigure = MagicMock(side_effect=OSError("test"))
    
    with patch.object(sys, "stdout", mock_stdout), patch.object(sys, "stderr", mock_stderr):
        _configure_utf8_stdio()
        mock_stdout.reconfigure.assert_called_with(encoding="utf-8", errors="replace")
        mock_stderr.reconfigure.assert_called_with(encoding="utf-8", errors="replace")
