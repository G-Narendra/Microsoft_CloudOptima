"""Tests for observability: TraceEvent, AuditLogger, and @trace decorator.

Covers BUILD_CHECKLIST Phase 9.3: TraceEvent round-trip, daily JSONL file
writing, query filters (date range / agent_name / event_type), @trace timing
on success and error branches, and the never-crash guarantees.
"""

from __future__ import annotations

import datetime
import json
from pathlib import Path

import pytest

from cloudoptima.observability import (
    AuditLogger,
    TraceEvent,
    get_audit_logger,
    trace,
)


def _make_event() -> TraceEvent:
    """A fully-populated TraceEvent for reuse across tests."""
    return TraceEvent(
        event_type="agent_call",
        agent_name="Architect",
        latency_ms=12.5,
        tokens_used=100,
        status="success",
        session_id="sess-123",
        extra={"detail": "ok"},
    )


# ── TraceEvent ─────────────────────────────────────────────────────────────


def test_trace_event_defaults() -> None:
    """A bare TraceEvent carries sensible defaults."""
    event = TraceEvent()
    assert event.event_type == "generic"
    assert event.agent_name == "unknown"
    assert event.latency_ms == 0.0
    assert event.tokens_used == 0
    assert event.status == "success"
    assert event.session_id == ""
    assert event.extra == {}


def test_trace_event_round_trip() -> None:
    """dict → event → dict preserves every field, including the timestamp."""
    original = _make_event()
    restored = TraceEvent.from_dict(original.to_dict())

    assert restored.event_type == original.event_type
    assert restored.agent_name == original.agent_name
    assert restored.latency_ms == original.latency_ms
    assert restored.tokens_used == original.tokens_used
    assert restored.status == original.status
    assert restored.session_id == original.session_id
    assert restored.extra == original.extra
    assert restored._timestamp == original._timestamp


def test_trace_event_to_dict_is_json_serializable() -> None:
    """to_dict() output must be encodable as JSON (dashboard/CI friendly)."""
    payload = _make_event().to_dict()
    json.dumps(payload)  # must not raise
    assert "timestamp" in payload


def test_trace_event_from_dict_tolerates_unknown_keys() -> None:
    """A corrupt/hostile log line with extra keys must not crash the reader."""
    data = _make_event().to_dict()
    data["mystery_field"] = "boom"
    data["extra"] = {"still": "dict"}

    restored = TraceEvent.from_dict(data)  # must not raise
    assert restored.event_type == "agent_call"


# ── AuditLogger ────────────────────────────────────────────────────────────


def test_audit_logger_writes_daily_file(tmp_path: Path) -> None:
    """log() appends one JSON line to today's audit-YYYY-MM-DD.jsonl."""
    logger = AuditLogger(tmp_path)
    logger.log(_make_event())

    day = datetime.date.today()
    path = tmp_path / f"audit-{day.isoformat()}.jsonl"
    assert path.exists()

    lines = path.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 1
    data = json.loads(lines[0])
    assert data["event_type"] == "agent_call"
    assert data["agent_name"] == "Architect"


def test_audit_logger_is_append_only(tmp_path: Path) -> None:
    """Two log() calls produce two lines; nothing is overwritten."""
    logger = AuditLogger(tmp_path)
    logger.log(_make_event())
    logger.log(_make_event())

    day = datetime.date.today()
    path = tmp_path / f"audit-{day.isoformat()}.jsonl"
    lines = path.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 2


def test_query_filters_by_agent_and_type(tmp_path: Path) -> None:
    """query() filters by agent_name and event_type independently and together."""
    logger = AuditLogger(tmp_path)
    logger.log(TraceEvent(event_type="agent_call", agent_name="Architect"))
    logger.log(TraceEvent(event_type="agent_call", agent_name="Judge"))
    logger.log(TraceEvent(event_type="cache_hit", agent_name="LLMCache"))

    assert len(logger.query(agent_name="Architect")) == 1
    assert len(logger.query(event_type="cache_hit")) == 1
    assert len(logger.query(agent_name="Judge", event_type="agent_call")) == 1
    assert logger.query(agent_name="Nope") == []


def test_query_date_range_with_missing_day(tmp_path: Path) -> None:
    """Querying a day with no log file returns an empty list, not an error."""
    logger = AuditLogger(tmp_path)
    logger.log(_make_event())  # today

    past = datetime.date.today() - datetime.timedelta(days=3)
    assert logger.query(start=past, end=past) == []


def test_audit_logger_skips_malformed_lines(tmp_path: Path) -> None:
    """Corrupt JSON lines are skipped; valid ones are still parsed."""
    logger = AuditLogger(tmp_path)
    day = datetime.date.today()
    path = tmp_path / f"audit-{day.isoformat()}.jsonl"
    path.write_text("this is not json\n", encoding="utf-8")
    logger.log(_make_event())

    events = logger.query()
    assert len(events) == 1
    assert events[0].event_type == "agent_call"


def test_audit_logger_log_dir_property(tmp_path: Path) -> None:
    """log_dir exposes the configured directory."""
    logger = AuditLogger(tmp_path)
    assert logger.log_dir == tmp_path


# ── @trace decorator ───────────────────────────────────────────────────────


def test_trace_success_records_event(tmp_path: Path) -> None:
    """@trace logs a success event with function name, arg count, and latency."""
    logger = AuditLogger(tmp_path)

    @trace("my_function", "Tester", logger=logger)
    def add(a: int, b: int) -> int:
        return a + b

    assert add(2, 3) == 5

    events = logger.query(event_type="my_function")
    assert len(events) == 1
    assert events[0].status == "success"
    assert events[0].agent_name == "Tester"
    assert events[0].latency_ms >= 0
    assert events[0].extra["function"] == "add"
    assert events[0].extra["arg_count"] == 2


def test_trace_error_records_event_and_reraises(tmp_path: Path) -> None:
    """@trace logs an error event, then re-raises — it only observes."""
    logger = AuditLogger(tmp_path)

    @trace("failing", "Tester", logger=logger)
    def boom() -> None:
        raise ValueError("kaboom")

    with pytest.raises(ValueError, match="kaboom"):
        boom()

    events = logger.query(event_type="failing")
    assert len(events) == 1
    assert events[0].status == "error"
    assert events[0].extra["error_type"] == "ValueError"


# ── Singleton ──────────────────────────────────────────────────────────────


def test_get_audit_logger_is_singleton() -> None:
    """get_audit_logger() returns the same shared instance each call."""
    first = get_audit_logger()
    second = get_audit_logger()
    assert first is second
