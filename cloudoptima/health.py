"""System health checks and registry."""

from __future__ import annotations

from collections.abc import Callable
import datetime
import logging
import shutil
import sys
from typing import Final, TypeAlias

try:
    import psutil
    _PSUTIL_AVAILABLE = True
except ImportError:
    psutil = None  # type: ignore
    _PSUTIL_AVAILABLE = False

from cloudoptima.config import Settings
from cloudoptima.llm_cache import LLMCache
from cloudoptima.llm_client import create_llm_client
from cloudoptima.llm_routing import create_routed_client
from cloudoptima.observability import DEFAULT_LOG_DIR, AuditLogger

_logger = logging.getLogger(__name__)

# Warning & critical thresholds
DISK_WARN_PCT: Final[float] = 85.0
DISK_CRIT_PCT: Final[float] = 95.0
MEM_WARN_PCT: Final[float] = 80.0
MEM_CRIT_PCT: Final[float] = 90.0

CheckResult: TypeAlias = tuple[bool, str]
CheckFn: TypeAlias = Callable[[], CheckResult]
HealthEntry: TypeAlias = dict[str, str | bool | float | datetime.datetime | None]

# Registry store
_registry: dict[str, CheckFn] = {}


def register(name: str) -> Callable[[CheckFn], CheckFn]:
    """Decorator to register a health check function by name."""
    def decorator(check_fn: CheckFn) -> CheckFn:
        if name in _registry:
            _logger.warning("Health check '%s' already registered — overwriting", name)
        _registry[name] = check_fn
        return check_fn

    return decorator


def unregister(name: str) -> None:
    """Remove a registered health check. No-op if not found."""
    _registry.pop(name, None)


def list_checks() -> list[str]:
    """Return names of all registered health checks."""
    return list(_registry.keys())


def check_all(
    include: list[str] | None = None, exclude: list[str] | None = None
) -> dict[str, HealthEntry]:
    """Run all registered health checks and collect results."""
    results: dict[str, HealthEntry] = {}
    now = datetime.datetime.now(datetime.UTC)

    for name, check_fn in _registry.items():
        if include is not None and name not in include:
            continue
        if exclude is not None and name in exclude:
            continue

        try:
            passed, detail = check_fn()
        except Exception as exc:
            _logger.exception("Health check '%s' raised an exception", name)
            passed = False
            detail = f"Exception: {type(exc).__name__}: {exc}"

        results[name] = {
            "passed": passed,
            "detail": detail,
            "timestamp": now,
        }

    return results


def overall_status(results: dict[str, HealthEntry] | None = None) -> str:
    """Collapse check results into one status label: healthy, degraded, or unhealthy."""
    if results is None:
        results = check_all()

    if not results:
        return "unhealthy"

    passed_count = sum(1 for r in results.values() if r["passed"])
    failed_count = len(results) - passed_count

    if passed_count == len(results):
        return "healthy"
    if failed_count == len(results):
        return "unhealthy"
    return "degraded"


# Pre-built health checks

@register("python_version")
def _check_python_version() -> CheckResult:
    """Verify Python >= 3.11 is running."""
    major, minor = sys.version_info[:2]
    if (major, minor) >= (3, 11):
        return True, f"Python {major}.{minor} — meets minimum 3.11 requirement"
    return False, f"Python {major}.{minor} — minimum 3.11 required, upgrade needed"


@register("disk_space")
def _check_disk_space() -> CheckResult:
    """Check available disk space on the working directory."""
    try:
        usage = shutil.disk_usage(".")
        pct_used = usage.used / usage.total * 100
        free_gb = usage.free / (1024**3)
        if pct_used < DISK_WARN_PCT:
            return True, f"Disk {pct_used:.1f}% used ({free_gb:.1f} GB free) — OK"
        if pct_used < DISK_CRIT_PCT:
            return True, (
                f"Disk {pct_used:.1f}% used ({free_gb:.1f} GB free) — "
                f"WARNING (>{DISK_WARN_PCT}%)"
            )
        return False, (
            f"Disk {pct_used:.1f}% used ({free_gb:.1f} GB free) — "
            f"CRITICAL (>{DISK_CRIT_PCT}%)"
        )
    except OSError as exc:
        return False, f"Could not check disk: {exc}"


@register("memory")
def _check_memory() -> CheckResult:
    """Check memory pressure via psutil."""
    if not _PSUTIL_AVAILABLE:
        return True, "Memory check skipped — psutil not installed"

    try:
        mem = psutil.virtual_memory()
        pct = mem.percent
        if pct < MEM_WARN_PCT:
            return True, (
                f"Memory {pct:.1f}% used "
                f"({mem.available / 1024**3:.1f} GB available) — OK"
            )
        if pct < MEM_CRIT_PCT:
            return True, (
                f"Memory {pct:.1f}% used "
                f"({mem.available / 1024**3:.1f} GB available) — WARNING"
            )
        return False, f"Memory {pct:.1f}% used — CRITICAL"
    except Exception as exc:
        return False, f"Memory check failed: {exc}"


@register("audit_log_dir")
def _check_audit_log_dir() -> CheckResult:
    """Verify the audit log directory is writable."""
    try:
        audit_logger = AuditLogger(DEFAULT_LOG_DIR)
        path = audit_logger.log_dir
        test_file = path / ".health_check_write_test"
        test_file.write_text("ok")
        test_file.unlink()
        return True, f"Audit log dir '{path}' is writable"
    except OSError as exc:
        return False, f"Audit log dir NOT writable: {exc}"


@register("llm_client_ping")
def _check_llm_client_ping() -> CheckResult:
    """Check that an LLM client can be instantiated."""
    try:
        settings = Settings()
        if settings.routing_enabled:
            routed = create_routed_client(settings)
            providers = ", ".join(sorted(set(routed.chosen_providers())))
            return True, f"Routed LLM client ready — providers: {providers}"

        provider = settings.llm_provider
        client = create_llm_client(settings)
        if client is not None:
            return True, f"LLM client '{provider}' created successfully"

        return False, f"LLM client factory returned None for provider '{provider}'"
    except Exception as exc:
        return False, f"LLM client creation failed: {type(exc).__name__}: {exc}"


@register("cache")
def _check_cache() -> CheckResult:
    """Check that the LLM response cache can be initialized."""
    try:
        cache = LLMCache()
        stats = cache.stats()
        return True, f"Cache initialised (entries={stats['entries']})"
    except Exception as exc:
        return False, f"Cache initialisation failed: {type(exc).__name__}: {exc}"
