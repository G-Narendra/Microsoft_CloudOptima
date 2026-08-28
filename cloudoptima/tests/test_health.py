"""Tests for the health check registry (BUILD_CHECKLIST Phase 9.3).

Covers the registry pattern (register / unregister / list_checks), check_all()
result collection with include/exclude filters and exception safety, and
overall_status() aggregation to healthy / degraded / unhealthy.
"""

from collections import namedtuple
import datetime
from unittest.mock import MagicMock, patch

try:
    import psutil
except ImportError:
    psutil = None  # type: ignore

from cloudoptima import health
from cloudoptima.health import (
    check_all,
    list_checks,
    overall_status,
    register,
    unregister,
)


def _now() -> datetime.datetime:
    """A timestamp for hand-built health entries."""
    return datetime.datetime.now(datetime.UTC)


def _entry(
    passed: bool, detail: str = ""
) -> dict[str, str | bool | float | datetime.datetime | None]:
    """Build a single HealthEntry-shaped result dict."""
    return {"passed": passed, "detail": detail, "timestamp": _now()}


# Registry tests

def test_registry_has_all_prebuilt_checks() -> None:
    """All six pre-built checks are registered at import time."""
    names = list_checks()
    assert "python_version" in names
    assert "disk_space" in names
    assert "memory" in names
    assert "audit_log_dir" in names
    assert "llm_client_ping" in names
    assert "cache" in names
    assert len(names) >= 6


def test_register_and_unregister() -> None:
    """A custom check can be registered and removed; missing names are no-ops."""

    @register("test_custom_check")
    def _custom() -> tuple[bool, str]:
        return True, "ok"

    assert "test_custom_check" in list_checks()
    unregister("test_custom_check")
    assert "test_custom_check" not in list_checks()
    unregister("does_not_exist")


# check_all tests

def test_check_all_returns_typed_entries() -> None:
    """Every registered check produces a (passed, detail, timestamp) result."""
    results = check_all()
    assert results
    for name, entry in results.items():
        assert isinstance(entry["passed"], bool)
        assert isinstance(entry["detail"], str)
        assert "timestamp" in entry


def test_check_all_include_filter() -> None:
    """include= runs only the named checks."""
    results = check_all(include=["python_version"])
    assert set(results) == {"python_version"}


def test_check_all_exclude_filter() -> None:
    """exclude= skips the named checks."""
    results = check_all(exclude=["cache"])
    assert "cache" not in results
    assert "python_version" in results


def test_check_all_never_crashes_on_throwing_check() -> None:
    """A check that raises is captured as a failed result, not a crash."""

    @register("test_throwing_check")
    def _throwing() -> tuple[bool, str]:
        raise RuntimeError("kaboom")

    try:
        results = check_all(include=["test_throwing_check"])
        assert results["test_throwing_check"]["passed"] is False
        detail = results["test_throwing_check"]["detail"]
        assert isinstance(detail, str) and "RuntimeError" in detail
    finally:
        unregister("test_throwing_check")


# overall_status tests

def test_overall_status_healthy() -> None:
    results = {"a": _entry(True), "b": _entry(True)}
    assert overall_status(results) == "healthy"


def test_overall_status_degraded() -> None:
    results = {"a": _entry(True), "b": _entry(False, "boom")}
    assert overall_status(results) == "degraded"


def test_overall_status_unhealthy() -> None:
    results = {"a": _entry(False, "boom")}
    assert overall_status(results) == "unhealthy"


def test_overall_status_empty_is_unhealthy() -> None:
    assert overall_status({}) == "unhealthy"


def test_overall_status_runs_checks_when_none() -> None:
    """overall_status() without args runs check_all() itself."""
    status = overall_status()
    assert status in {"healthy", "degraded", "unhealthy"}


# Real environment smoke test

def test_real_health_checks_do_not_crash() -> None:
    """Running all real checks in the dev environment never raises."""
    results = check_all()
    assert results
    for entry in results.values():
        assert isinstance(entry["passed"], bool)
        assert isinstance(entry["detail"], str)


# Module-level sanity

def test_health_module_is_registry_backed() -> None:
    """The health module exposes the documented public API."""
    assert callable(health.register)
    assert callable(health.unregister)
    assert callable(health.check_all)
    assert callable(health.overall_status)
    assert callable(health.list_checks)


# Coverage tests for specific checks

def test_register_overwrite(caplog):
    """Test that registering an existing check logs a warning."""
    @register("test_overwrite")
    def _test1(): return True, "1"
    
    @register("test_overwrite")
    def _test2(): return True, "2"
    
    assert "already registered" in caplog.text
    unregister("test_overwrite")

def test_python_version_fail():
    with patch("sys.version_info", (3, 10, 0)):
        passed, msg = health._check_python_version()
        assert not passed
        assert "upgrade needed" in msg

def test_disk_space_branches():
    Usage = namedtuple("Usage", ["used", "total", "free"])
    
    # Warning
    with patch("shutil.disk_usage", return_value=Usage(86, 100, 14)):
        passed, msg = health._check_disk_space()
        assert passed
        assert "WARNING" in msg
        
    # Critical
    with patch("shutil.disk_usage", return_value=Usage(96, 100, 4)):
        passed, msg = health._check_disk_space()
        assert not passed
        assert "CRITICAL" in msg
        
    # Exception
    with patch("shutil.disk_usage", side_effect=OSError("disk error")):
        passed, msg = health._check_disk_space()
        assert not passed
        assert "disk error" in msg

def test_memory_branches():
    Mem = namedtuple("Mem", ["percent", "available"])
    
    # Warning
    with patch("cloudoptima.health.psutil") as mock_psutil, patch("cloudoptima.health._PSUTIL_AVAILABLE", True):
        mock_psutil.virtual_memory.return_value = Mem(85.0, 1024**3)
        passed, msg = health._check_memory()
        assert passed
        assert "WARNING" in msg
        
    # Critical
    with patch("cloudoptima.health.psutil") as mock_psutil, patch("cloudoptima.health._PSUTIL_AVAILABLE", True):
        mock_psutil.virtual_memory.return_value = Mem(95.0, 1024**3)
        passed, msg = health._check_memory()
        assert not passed
        assert "CRITICAL" in msg

def test_audit_log_dir_fail():
    with patch("cloudoptima.health.AuditLogger", side_effect=OSError("permission denied")):
        passed, msg = health._check_audit_log_dir()
        assert not passed
        assert "NOT writable" in msg

def test_llm_client_ping_branches():
    # Routed
    with patch("cloudoptima.health.Settings") as mock_settings:
        mock_s = MagicMock()
        mock_s.routing_enabled = True
        mock_settings.return_value = mock_s
        
        with patch("cloudoptima.health.create_routed_client") as mock_crc:
            mock_crc.return_value.chosen_providers.return_value = ["mock1", "mock2"]
            passed, msg = health._check_llm_client_ping()
            assert passed
            assert "mock1, mock2" in msg
            
    # Factory returns None
    with patch("cloudoptima.health.Settings") as mock_settings:
        mock_s = MagicMock()
        mock_s.routing_enabled = False
        mock_s.llm_provider = "invalid"
        mock_settings.return_value = mock_s
        
        with patch("cloudoptima.health.create_llm_client", return_value=None):
            passed, msg = health._check_llm_client_ping()
            assert not passed
            assert "returned None" in msg
            
    # Exception
    with patch("cloudoptima.health.Settings", side_effect=Exception("config error")):
        passed, msg = health._check_llm_client_ping()
        assert not passed
        assert "config error" in msg

def test_cache_branches():
    with patch("cloudoptima.health.LLMCache", side_effect=Exception("cache error")):
        passed, msg = health._check_cache()
        assert not passed
        assert "cache error" in msg
