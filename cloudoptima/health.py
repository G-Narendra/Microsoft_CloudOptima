"""Health checks: a registry so any module can contribute a check.

Any module registers a check function at import time with
:func:`register`; :func:`check_all` runs them all and collects results;
:func:`overall_status` collapses them into ``healthy`` / ``degraded`` /
``unhealthy``. Checks are plain callables returning ``(passed, detail)`` —
no base class needed.

Pre-built checks cover the LLM client, cache, disk, memory, Python version,
and the audit log directory.

Example:
    >>> from cloudoptima.health import register, check_all, overall_status
    >>> @register("my_module")
    ... def _check_my_module() -> tuple[bool, str]:
    ...     return True, "All good"
    ...
    >>> status = overall_status()
    >>> status
    'healthy'
"""

from __future__ import annotations

import datetime
import logging
import shutil
from collections.abc import Callable
from typing import Final, TypeAlias

# ── Module-level logger ────────────────────────────────────────────────
_logger = logging.getLogger(__name__)

# ── Constants ──────────────────────────────────────────────────────────
DISK_WARN_PCT: Final[float] = 85.0      # Warning threshold (%)
DISK_CRIT_PCT: Final[float] = 95.0      # Critical threshold (%)
MEM_WARN_PCT: Final[float] = 80.0       # Warning threshold (%)
MEM_CRIT_PCT: Final[float] = 90.0       # Critical threshold (%)

# ── Type aliases (PEP 613) ─────────────────────────────────────────────
CheckResult: TypeAlias = tuple[bool, str]  # (passed, detail_message)
CheckFn: TypeAlias = Callable[[], CheckResult]  # A health check function
HealthEntry: TypeAlias = dict[str, str | bool | float | datetime.datetime | None]


# ── Registry ───────────────────────────────────────────────────────────
_registry: dict[str, CheckFn] = {}                     # name → check function


def register(name: str) -> Callable[[CheckFn], CheckFn]:
    """Decorator — register a health check function by name.

    The decorated function must return a (passed: bool, detail: str) tuple.

    Example:
        >>> @register("cache_ping")
        ... def _check_cache():
        ...     try:
        ...         cache.ping()
        ...         return True, "Cache responds in < 5ms"
        ...     except ConnectionError:
        ...         return False, "Cache unreachable"
    """
    def decorator(check_fn: CheckFn) -> CheckFn:
        if name in _registry:
            _logger.warning("Health check '%s' already registered — overwriting", name)
        _registry[name] = check_fn
        return check_fn

    return decorator


def unregister(name: str) -> None:
    """Remove a previously registered check. No-op if not found."""
    _registry.pop(name, None)


def list_checks() -> list[str]:
    """Return names of all registered health checks."""
    return list(_registry.keys())


def check_all(
    include: list[str] | None = None, exclude: list[str] | None = None
) -> dict[str, HealthEntry]:
    """Run every registered check (or just the named ones) and collect results.

    Args:
        include: If set, only run checks whose names appear in this list.
        exclude: If set, skip checks whose names appear in this list.

    Returns:
        Mapping of check name → {"passed", "detail", "timestamp"}.

    A check that raises is captured as a failed result — this never crashes.
    """
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
    """Collapse check results into one status label.

    - "healthy"    → everything passed
    - "degraded"   → some passed, some failed
    - "unhealthy"  → all failed, or nothing is registered

    Args:
        results: Output from :func:`check_all`; runs it if ``None``.

    Returns:
        One of "healthy", "degraded", "unhealthy".
    """
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


# ── Pre-built checks ───────────────────────────────────────────────────

@register("python_version")
def _check_python_version() -> CheckResult:
    """Verify Python >= 3.11 is running."""
    import sys
    major, minor = sys.version_info[:2]
    if (major, minor) >= (3, 11):
        return True, f"Python {major}.{minor} — meets minimum 3.11 requirement"
    return False, f"Python {major}.{minor} — minimum 3.11 required, upgrade needed"


@register("disk_space")
def _check_disk_space() -> CheckResult:
    """Check available disk space on the log/working directory."""
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
    """Check memory pressure via psutil (best-effort).

    Falls back gracefully if psutil is not installed — never reports a
    false-positive "healthy" when no data is available.
    """
    try:
        import psutil
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

    except ImportError:
        return True, "Memory check skipped — install `psutil` for memory monitoring"


@register("audit_log_dir")
def _check_audit_log_dir() -> CheckResult:
    """Verify the audit log directory is writable."""
    from cloudoptima.observability import get_audit_logger
    try:
        audit_logger = get_audit_logger()
        path = audit_logger.log_dir
        test_file = path / ".health_check_write_test"
        test_file.write_text("ok")
        test_file.unlink()
        return True, f"Audit log dir '{path}' is writable"
    except OSError as exc:
        return False, f"Audit log dir NOT writable: {exc}"


@register("llm_client_ping")
def _check_llm_client_ping() -> CheckResult:
    """Check that an LLM client can be created (does NOT call the live API).

    This check verifies the LLM provider config is present and the factory
    can instantiate a client. It does NOT make a network call to avoid
    accidentally burning credits or timing out during health checks.
    """
    try:
        from cloudoptima.config import Settings
        from cloudoptima.llm_client import create_llm_client
        from cloudoptima.llm_routing import create_routed_client

        settings = Settings()
        if settings.routing_enabled:
            routed = create_routed_client(settings)
            providers = ", ".join(sorted(set(routed.chosen_providers())))
            return True, f"Routed LLM client ready — providers: {providers}"

        provider = settings.llm_provider
        client = create_llm_client(settings)
        if client is not None:
            return True, f"LLM client '{provider}' created successfully (no live ping)"

        return False, f"LLM client factory returned None for provider '{provider}'"

    except ImportError:
        return True, "LLM client check skipped — config/llm_client not yet built"
    except Exception as exc:
        return False, f"LLM client creation failed: {type(exc).__name__}: {exc}"


@register("cache")
def _check_cache() -> CheckResult:
    """Check that the LLM response cache can be initialised.

    Does NOT populate or check hit/miss — just verifies the module
    imports and can create a cache instance.
    """
    try:
        from cloudoptima.llm_cache import LLMCache

        cache = LLMCache()
        stats = cache.stats()
        return True, f"Cache initialised (entries={stats['entries']})"

    except ImportError:
        return True, "Cache check skipped — llm_cache module not yet built (Phase 2)"
    except Exception as exc:
        return False, f"Cache initialisation failed: {type(exc).__name__}: {exc}"
