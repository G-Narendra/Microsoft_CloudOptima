"""Observability: structured tracing, append-only audit logs, and trace decorator."""

from __future__ import annotations

import asyncio
from collections.abc import Callable
from dataclasses import asdict, dataclass, field
import datetime
import functools
import json
import logging
from pathlib import Path
import threading
import time
from typing import Any, Final, TypeAlias, TypeVar

try:
    from azure.monitor.opentelemetry import configure_azure_monitor
    from opentelemetry import trace as otel_trace
    HAS_OPENTELEMETRY = True
    
    try:
        configure_azure_monitor()
    except Exception:
        pass
    
    _tracer = otel_trace.get_tracer(__name__)
except ImportError:
    HAS_OPENTELEMETRY = False
    _tracer = None

_logger = logging.getLogger(__name__)

RETENTION_DAYS: Final[int] = 90
DEFAULT_LOG_DIR: Final[str] = "logs"
_DATETIME_FMT: Final[str] = "%Y-%m-%dT%H:%M:%S.%fZ"

F = TypeVar("F", bound=Callable[..., Any])
JsonSerializable: TypeAlias = dict[str, Any] | list[Any] | str | int | float | bool | None


@dataclass
class DriftMetric:
    """MLOps model drift metric."""
    metric_name: str
    value: float
    model_version: str
    timestamp: str = field(default_factory=lambda: datetime.datetime.now(datetime.UTC).isoformat())

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# TraceEvent

@dataclass
class TraceEvent:
    """One observable event — typed, timestamped, immutable."""

    event_type: str
    agent_name: str = "unknown"
    session_id: str | None = None
    latency_ms: float = 0.0
    tokens_used: int = 0
    input_summary: dict[str, JsonSerializable] = field(default_factory=dict)
    output_summary: dict[str, JsonSerializable] = field(default_factory=dict)
    cache_hit: bool = False
    validation_passed: bool = True
    error_message: str | None = None
    metadata: dict[str, JsonSerializable] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.datetime.now(datetime.UTC).strftime(_DATETIME_FMT))
    trace_id: str | None = None
    span_id: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to a JSON-serializable dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> TraceEvent:
        """Construct a TraceEvent from a dictionary."""
        known_fields = cls.__dataclass_fields__.keys()
        filtered = {k: v for k, v in data.items() if k in known_fields}
        return cls(**filtered)


_global_logger: AuditLogger | None = None


def get_audit_logger() -> AuditLogger:
    global _global_logger
    if _global_logger is None:
        _global_logger = AuditLogger()
    return _global_logger


# AuditLogger — append-only JSONL

class AuditLogger:
    """Append-only daily JSONL audit log."""

    def __init__(self, log_dir: str | Path = DEFAULT_LOG_DIR) -> None:
        self._log_dir = Path(log_dir)
        self._lock = threading.Lock()
        self._log_dir.mkdir(parents=True, exist_ok=True)

    # Public API

    def log(self, event: TraceEvent) -> None:
        """Append one event to today's audit file. Thread-safe."""
        if HAS_OPENTELEMETRY:
            span_context = otel_trace.get_current_span().get_span_context()
            if span_context.is_valid:
                if not event.trace_id:
                    event.trace_id = format(span_context.trace_id, "032x")
                if not event.span_id:
                    event.span_id = format(span_context.span_id, "016x")

        try:
            line = json.dumps(event.to_dict(), default=str, ensure_ascii=False)
            path = self._daily_path()
            with self._lock:
                with open(path, "a", encoding="utf-8") as fh:
                    fh.write(line + "\n")
                    fh.flush()
            self._prune_old_logs()
        except OSError:
            _logger.exception("AuditLogger: failed to write event")
        except Exception:
            _logger.exception("AuditLogger: unexpected error — event dropped")

    def log_drift(self, drift: DriftMetric) -> None:
        """Write a drift metric to a separate daily JSONL file."""
        if not self._log_dir.exists():
            self._log_dir.mkdir(parents=True, exist_ok=True)
            
        today = datetime.date.today()
        path = self._log_dir / f"drift-{today.isoformat()}.jsonl"
        line = json.dumps(drift.to_dict(), separators=(",", ":"))
        try:
            with self._lock:
                with open(path, "a", encoding="utf-8") as fh:
                    fh.write(line + "\n")
                    fh.flush()
        except OSError:
            _logger.exception("AuditLogger: failed to write drift metric")

    def query(
        self,
        start: datetime.date | None = None,
        end: datetime.date | None = None,
        agent_name: str | None = None,
        event_type: str | None = None,
    ) -> list[TraceEvent]:
        """Filter events across log files within a date range."""
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

    # Internal helpers

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
            date_str = path.stem.replace("audit-", "", 1)
            file_date = datetime.date.fromisoformat(date_str)
            if file_date < cutoff:
                path.unlink()
                _logger.info("AuditLogger: pruned old log %s", path.name)
        except (ValueError, OSError):
            pass


# @trace decorator

def trace(
    event_type: str = "function_call",
    agent_name: str = "unknown",
    logger: AuditLogger | None = None,
) -> Callable[[F], F]:
    """Decorator to auto-log a TraceEvent around any function."""

    def decorator(func: F) -> F:
        func_name = getattr(func, "__qualname__", getattr(func, "__name__", "unknown"))
        effective_agent = agent_name if agent_name != "unknown" else func_name

        @functools.wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            audit = logger or get_audit_logger()
            session_id = _extract_session_id(args, kwargs)
            start = _now_monotonic()
            error_msg: str | None = None
            result: Any = None

            try:
                result = func(*args, **kwargs)
                return result
            except Exception as exc:
                error_msg = f"{type(exc).__name__}: {exc}"
                raise
            finally:
                elapsed_ms = (_now_monotonic() - start) * 1000.0
                event = TraceEvent(
                    event_type=event_type,
                    agent_name=effective_agent,
                    session_id=session_id,
                    latency_ms=round(elapsed_ms, 2),
                    input_summary=_safe_args(func_name, args, kwargs),
                    validation_passed=(error_msg is None),
                    error_message=error_msg,
                )
                audit.log(event)

        @functools.wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            audit = logger or get_audit_logger()
            session_id = _extract_session_id(args, kwargs)
            start = _now_monotonic()
            error_msg: str | None = None
            result: Any = None

            try:
                result = await func(*args, **kwargs)
                return result
            except Exception as exc:
                error_msg = f"{type(exc).__name__}: {exc}"
                raise
            finally:
                elapsed_ms = (_now_monotonic() - start) * 1000.0
                event = TraceEvent(
                    event_type=event_type,
                    agent_name=effective_agent,
                    session_id=session_id,
                    latency_ms=round(elapsed_ms, 2),
                    input_summary=_safe_args(func_name, args, kwargs),
                    validation_passed=(error_msg is None),
                    error_message=error_msg,
                )
                audit.log(event)

        if asyncio.iscoroutinefunction(func):
            return async_wrapper  # type: ignore[return-value]
        return sync_wrapper  # type: ignore[return-value]

    return decorator


def _extract_session_id(args: tuple[Any, ...], kwargs: dict[str, Any]) -> str | None:
    """Best-effort extraction of a session_id from args or kwargs."""
    if "session_id" in kwargs and isinstance(kwargs["session_id"], str):
        return kwargs["session_id"]
    if "session" in kwargs and hasattr(kwargs["session"], "session_id"):
        return str(kwargs["session"].session_id)
    for arg in args:
        if hasattr(arg, "session_id"):
            return str(arg.session_id)
    return None


# Anomaly detection

@dataclass
class _AnomalyBaseline:
    """Per-agent rolling baselines (EWMA) for response length and tokens."""

    length_ewma: float = 0.0
    tokens_ewma: float = 0.0
    samples: int = 0


class AnomalyDetector:
    """Flags unusually short/long responses and token drops."""

    WARMUP_SAMPLES: Final[int] = 5
    ALPHA: Final[float] = 0.3
    TOKEN_DROP_FRACTION: Final[float] = 0.5
    LENGTH_LOW_FRACTION: Final[float] = 0.4
    LENGTH_HIGH_FRACTION: Final[float] = 2.5

    def __init__(self) -> None:
        self._baselines: dict[str, _AnomalyBaseline] = {}
        self._lock = threading.Lock()

    def record(self, agent: str, response_length: int, tokens_used: int) -> list[str]:
        """Feed one observation and return any anomaly flags raised."""
        flags: list[str] = []
        with self._lock:
            base = self._baselines.setdefault(agent, _AnomalyBaseline())
            if base.samples >= self.WARMUP_SAMPLES and base.length_ewma > 0:
                low = base.length_ewma * self.LENGTH_LOW_FRACTION
                high = base.length_ewma * self.LENGTH_HIGH_FRACTION
                if response_length < low or response_length > high:
                    flags.append("response_length_anomaly")

            if (
                base.samples >= self.WARMUP_SAMPLES
                and tokens_used > 0
                and base.tokens_ewma > 0
            ):
                drop_threshold = base.tokens_ewma * (1.0 - self.TOKEN_DROP_FRACTION)
                if tokens_used < drop_threshold:
                    flags.append("token_usage_drop")

            self._update(base, response_length, tokens_used)
        return flags

    def baseline_for(self, agent: str) -> dict[str, float | int]:
        """Return a snapshot of the current baseline for ``agent``."""
        with self._lock:
            base = self._baselines.get(agent)
            if base is None:
                return {"samples": 0, "length_ewma": 0.0, "tokens_ewma": 0.0}
            return {
                "samples": base.samples,
                "length_ewma": round(base.length_ewma, 1),
                "tokens_ewma": round(base.tokens_ewma, 1),
            }

    def _update(
        self, base: _AnomalyBaseline, response_length: int, tokens_used: int
    ) -> None:
        """Update EWMA with one observation."""
        if base.samples == 0:
            base.length_ewma = float(response_length)
            base.tokens_ewma = float(tokens_used) if tokens_used > 0 else 0.0
        else:
            base.length_ewma = (
                self.ALPHA * float(response_length)
                + (1.0 - self.ALPHA) * base.length_ewma
            )
            if tokens_used > 0:
                if base.tokens_ewma == 0.0:
                    base.tokens_ewma = float(tokens_used)
                else:
                    base.tokens_ewma = (
                        self.ALPHA * float(tokens_used)
                        + (1.0 - self.ALPHA) * base.tokens_ewma
                    )
        base.samples += 1


# Internal helpers

def _utcnow_iso() -> str:
    """Return current UTC time as ISO 8601 string."""
    return datetime.datetime.now(datetime.UTC).strftime(_DATETIME_FMT)


def _now_monotonic() -> float:
    """Return monotonic clock value."""
    return time.monotonic()


def _safe_args(
    func_name: str, args: tuple[Any, ...], kwargs: dict[str, Any]
) -> dict[str, JsonSerializable]:
    """Build a safe summary of function arguments."""
    return {
        "function": func_name,
        "arg_count": len(args),
        "kwarg_names": list(kwargs.keys()),
    }
