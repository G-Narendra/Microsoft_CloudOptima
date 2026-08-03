"""Tests for the health check registry (BUILD_CHECKLIST Phase 9.3).

Covers the registry pattern (register / unregister / list_checks), check_all()
result collection with include/exclude filters and exception safety, and
overall_status() aggregation to healthy / degraded / unhealthy.
"""

from __future__ import annotations

import datetime

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


def _entry(passed: bool, detail: str = "") -> dict[str, object]:
    """Build a single HealthEntry-shaped result dict."""
    return {"passed": passed, "detail": detail, "timestamp": _now()}


# ── Registry ──────────────────────────────────────────────────────────────


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
    unregister("does_not_exist")  # must not raise


# ── check_all ─────────────────────────────────────────────────────────────


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
        assert "RuntimeError" in results["test_throwing_check"]["detail"]
    finally:
        unregister("test_throwing_check")


# ── overall_status ────────────────────────────────────────────────────────


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


# ── Real environment smoke test ───────────────────────────────────────────


def test_real_health_checks_do_not_crash() -> None:
    """Running all real checks in the dev environment never raises."""
    results = check_all()
    assert results
    for entry in results.values():
        assert isinstance(entry["passed"], bool)
        assert isinstance(entry["detail"], str)


# ── Module-level sanity (also ensures health module is importable) ────────


def test_health_module_is_registry_backed() -> None:
    """The health module exposes the documented public API."""
    assert callable(health.register)
    assert callable(health.unregister)
    assert callable(health.check_all)
    assert callable(health.overall_status)
    assert callable(health.list_checks)
