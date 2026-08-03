"""Observability: structured tracing, append-only audit logging, and @trace decorator.

Architecture decisions:
- Logs are written to a daily JSONL file under a configurable log_dir (default logs/).
- Files are never modified after creation — strictly append-only.
- Logs older than RETENTION_DAYS (90) are pruned on every write.
- The @trace decorator auto-records every agent/function call with timing.
- API keys, passwords, and raw secrets are NEVER written to logs.

Example:
    >>> from cloudoptima.observability import AuditLogger, TraceEvent, trace
    >>> logger = AuditLogger()
    >>> event = TraceEvent(
    ...     event_type="agent_call", agent_name="Architect",
    ...     latency_ms=120.5, tokens_used=450,
    ... )
    >>> logger.log(event)
    >>> @trace("my_function")
    ... def do_stuff():
    ...     return 42
"""

from __future__ import annotations

import datetime
import functools
import json
import logging
import threading
from collections.abc import Callable
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Final, TypeAlias, TypeVar

# ── Module-level logger ────────────────────────────────────────────────
_logger = logging.getLogger(__name__)

# ── Constants ──────────────────────────────────────────────────────────
RETENTION_DAYS: Final[int] = 90  # Logs older than this are pruned
DEFAULT_LOG_DIR: Final[str] = "logs"
_DATETIME_FMT: Final[str] = "%Y-%m-%dT%H:%M:%S.%fZ"  # ISO 8601 UTC

# ── Type variables ─────────────────────────────────────────────────────
F = TypeVar("F", bound=Callable[..., Any])
JsonSerializable: TypeAlias = dict[str, Any] | list[Any] | str | int | float | bool | None


# ── TraceEvent ─────────────────────────────────────────────────────────
@dataclass
class TraceEvent:
    """A single observability event — structured, timestamped, immutable.

    Attributes:
        event_type:  High-level category (e.g. "agent_call", "orchestrator_run", "cache_hit").
        agent_name:  The component that produced this event (e.g. "Architect", "LLMCache").
        latency_ms:  Elapsed wall-clock time in milliseconds. 0 if not applicable.
        tokens_used: Token count consumed (0 if unknown or not applicable).
        status:      Outcome — "success", "error", "warning", "rate_limited".
        session_id:  Optional session this event belongs to.
        extra:       Arbitrary JSON-serialisable metadata (never contains secrets).
    """

    event_type: str = "generic"
    agent_name: str = "unknown"
    latency_ms: float = 0.0
    tokens_used: int = 0
    status: str = "success"
    session_id: str = ""
    extra: dict[str, JsonSerializable] = field(default_factory=dict)
    _timestamp: str = field(default_factory=lambda: _utcnow_iso(), init=False, repr=False)

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a JSON-friendly dict (includes computed _timestamp)."""
        result = asdict(self)
        result["timestamp"] = result.pop("_timestamp")
        return result

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> TraceEvent:
        """Deserialise from a dict (restores _timestamp from 'timestamp' key).

        Note: _timestamp is init=False on the dataclass, so we bypass the
        constructor and set it directly via object.__setattr__.
        """
        raw = dict(data)
        timestamp_str: str = raw.pop("timestamp", _utcnow_iso())
        # Ignore unknown keys so a corrupt or hostile log line can never crash
        # the reader — unmatched keys would otherwise raise TypeError here.
        known = {name for name in cls.__dataclass_fields__ if name != "_timestamp"}
        filtered = {k: v for k, v in raw.items() if k in known}
        result = cls(**filtered)
        object.__setattr__(result, "_timestamp", timestamp_str)
        return result


# ── AuditLogger — append-only JSONL ────────────────────────────────────
class AuditLogger:
    """Append-only daily-rotating JSONL audit log.

    File layout:
        logs/audit-2026-07-30.jsonl   (one JSON object per line)

    Thread-safe (locking on write). Old logs are pruned automatically
    after RETENTION_DAYS on every write.

    Never crashes — errors are logged and swallowed so callers don't break.
    """

    def __init__(self, log_dir: str | Path = DEFAULT_LOG_DIR) -> None:
        self._log_dir = Path(log_dir)
        self._lock = threading.Lock()
        self._log_dir.mkdir(parents=True, exist_ok=True)

    # ── Public API ─────────────────────────────────────────────────

    def log(self, event: TraceEvent) -> None:
        """Append one event to today's audit file. Thread-safe."""
        try:
            line = json.dumps(event.to_dict(), default=str, ensure_ascii=False)
            path = self._daily_path()
            with self._lock:
                with open(path, "a", encoding="utf-8") as fh:
                    fh.write(line + "\n")
                    fh.flush()  # Ensure durability
            # Opportunistic prune — once per write
            self._prune_old_logs()
        except OSError:
            _logger.exception("AuditLogger: failed to write event")
        except Exception:
            _logger.exception("AuditLogger: unexpected error — event dropped")

    def query(
        self,
        start: datetime.date | None = None,
        end: datetime.date | None = None,
        agent_name: str | None = None,
        event_type: str | None = None,
    ) -> list[TraceEvent]:
        """Filter events across log files within a date range.

        Args:
            start:  Inclusive start date (defaults to RETENTION_DAYS ago).
            end:    Inclusive end date (defaults to today).
            agent_name:  Optional filter by agent name.
            event_type:  Optional filter by event type.

        Returns:
            Chronologically ordered list of matching TraceEvent objects.
        """
        today = datetime.date.today()
        start = start or (today - datetime.timedelta(days=RETENTION_DAYS))
        end = end or today
        results: list[TraceEvent] = []

        current = start
        while current <= end:
            path = self._daily_path(current)
            if path.exists():
                results.extend(self._read_file(path, agent_name, event_type))
            current += datetime.timedelta(days=1)

        return results

    @property
    def log_dir(self) -> Path:
        """The directory where audit files are stored."""
        return self._log_dir

    # ── Internal helpers ───────────────────────────────────────────

    def _daily_path(self, day: datetime.date | None = None) -> Path:
        day = day or datetime.date.today()
        filename = f"audit-{day.isoformat()}.jsonl"
        return self._log_dir / filename

    def _read_file(
        self,
        path: Path,
        agent_name: str | None,
        event_type: str | None,
    ) -> list[TraceEvent]:
        events: list[TraceEvent] = []
        try:
            with open(path, encoding="utf-8") as fh:
                for line in fh:
                    stripped = line.strip()
                    if not stripped:
                        continue
                    try:
                        data = json.loads(stripped)
                    except json.JSONDecodeError:
                        _logger.warning(
                            "AuditLogger: malformed JSON line in %s — skipping", path.name
                        )
                        continue
                    event = TraceEvent.from_dict(data)
                    if agent_name and event.agent_name != agent_name:
                        continue
                    if event_type and event.event_type != event_type:
                        continue
                    events.append(event)
        except OSError:
            _logger.warning("AuditLogger: could not read %s — skipping", path.name)
        return events

    def _prune_old_logs(self) -> None:
        """Delete audit files older than RETENTION_DAYS."""
        cutoff = datetime.date.today() - datetime.timedelta(days=RETENTION_DAYS)
        try:
            for child in self._log_dir.iterdir():
                if child.name.startswith("audit-") and child.suffix == ".jsonl":
                    self._prune_single(child, cutoff)
        except OSError:
            _logger.warning("AuditLogger: failed to prune old logs")

    @staticmethod
    def _prune_single(path: Path, cutoff: datetime.date) -> None:
        try:
            # audit-2026-04-01.jsonl → 2026-04-01
            date_str = path.stem.replace("audit-", "", 1)
            file_date = datetime.date.fromisoformat(date_str)
            if file_date < cutoff:
                path.unlink()
                _logger.info("AuditLogger: pruned old log %s", path.name)
        except (ValueError, OSError):
            pass  # Skip files with unexpected naming


# ── Singleton logger instance ──────────────────────────────────────────
_audit_logger: AuditLogger | None = None
_audit_logger_lock = threading.Lock()


def get_audit_logger(log_dir: str | Path | None = None) -> AuditLogger:
    """Return the shared AuditLogger instance (lazily initialised)."""
    global _audit_logger
    if _audit_logger is None:
        with _audit_logger_lock:
            if _audit_logger is None:
                _audit_logger = AuditLogger(log_dir or DEFAULT_LOG_DIR)
    return _audit_logger


# ── @trace decorator ───────────────────────────────────────────────────
def trace(
    event_type: str = "function_call",
    agent_name: str = "unknown",
    logger: AuditLogger | None = None,
) -> Callable[[F], F]:
    """Decorator — auto-log a TraceEvent around any function.

    Records the function name, arguments summary, return status, and
    wall-clock latency. Never logs secrets.

    Args:
        event_type:  Category label for the event.
        agent_name:  Component identifier.
        logger:      AuditLogger instance (uses global singleton if None).

    Example:
        >>> @trace("agent_call", "Architect")
        ... def analyze(session):
        ...     return {"result": "ok"}

    The decorator will emit one TraceEvent on success and one on error.
    """
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            _log = logger or get_audit_logger()
            start = _now_monotonic()

            try:
                result = func(*args, **kwargs)
                latency = (_now_monotonic() - start) * 1000  # ms

                event = TraceEvent(
                    event_type=event_type,
                    agent_name=agent_name,
                    latency_ms=round(latency, 2),
                    status="success",
                    extra=_safe_args(func.__name__, args, kwargs),
                )
                _log.log(event)
                return result

            except Exception as exc:
                latency = (_now_monotonic() - start) * 1000

                event = TraceEvent(
                    event_type=event_type,
                    agent_name=agent_name,
                    latency_ms=round(latency, 2),
                    status="error",
                    extra={
                        "function": func.__name__,
                        "error_type": type(exc).__name__,
                        "error_message": str(exc),
                    },
                )
                _log.log(event)
                raise  # Re-raise — we only observe, we don't swallow

        return wrapper  # type: ignore[return-value]

    return decorator


# ── Internal helpers ───────────────────────────────────────────────────

def _utcnow_iso() -> str:
    """Return current UTC time as ISO 8601 string (microsecond precision)."""
    return datetime.datetime.now(datetime.UTC).strftime(_DATETIME_FMT)


def _now_monotonic() -> float:
    """Return monotonic clock value (for duration measurement)."""
    import time
    return time.monotonic()


def _safe_args(
    func_name: str, args: tuple[Any, ...], kwargs: dict[str, Any]
) -> dict[str, JsonSerializable]:
    """Build a safe summary of function arguments — never include secrets.

    Only includes positional arg count and keyword arg names (not their values).
    """
    return {
        "function": func_name,
        "arg_count": len(args),
        "kwarg_names": list(kwargs.keys()),
    }
