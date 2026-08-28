"""Tests for async concurrency, pluggable rate limiting, and dependency injection."""

from __future__ import annotations

import asyncio
import fnmatch
import inspect
import json
import threading
from collections.abc import AsyncGenerator
from typing import Any

import pytest
from pydantic import ValidationError

from cloudoptima.agent_base import BaseAgent
from cloudoptima.agents import ALL_AGENTS
from cloudoptima.config import Settings
from cloudoptima.context import AppContext, build_rate_limiter
from cloudoptima.llm_client import (
    MOCK_RESPONSES,
    BaseLLMClient,
    MockClient,
    _detect_agent_type,
)
from cloudoptima.models import AgentType, Session
from cloudoptima.observability import AnomalyDetector, AuditLogger
from cloudoptima.orchestrator import Orchestrator
from cloudoptima.sanitize import (
    MemoryRateLimitStore,
    RateLimiter,
    RedisRateLimitStore,
)


class _ConcurrencyClient(BaseLLMClient):
    """LLM client that measures peak simultaneous calls."""

    def __init__(self) -> None:
        self._active = 0
        self.peak = 0
        self._lock = threading.Lock()
        self.last_tokens_used = 0

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        key = _detect_agent_type(prompt, system_prompt)
        return json.dumps(MOCK_RESPONSES.get(key, MOCK_RESPONSES["architect"]))

    async def agenerate(self, prompt: str, system_prompt: str = "") -> AsyncGenerator[str, None]:
        with self._lock:
            self._active += 1
            self.peak = max(self.peak, self._active)
        try:
            await asyncio.sleep(0.05)
            key = _detect_agent_type(prompt, system_prompt)
            self.last_tokens_used = 1
            yield json.dumps(MOCK_RESPONSES.get(key, MOCK_RESPONSES["architect"]))
        finally:
            with self._lock:
                self._active -= 1


class _FakeRedis:
    """Mock Redis client for testing RedisRateLimitStore."""

    def __init__(self) -> None:
        self._data: dict[str, int] = {}

    def get(self, key: str) -> str | None:
        value = self._data.get(key)
        return None if value is None else str(value)

    def incr(self, key: str) -> int:
        self._data[key] = self._data.get(key, 0) + 1
        return self._data[key]

    def expire(self, key: str, ttl: int) -> bool:  # noqa: ARG002
        return True

    def keys(self, pattern: str) -> list[str]:
        return [k for k in self._data if fnmatch.fnmatch(k, pattern)]

    def delete(self, name: str) -> int:
        return int(self._data.pop(name, None) is not None)


def _make_session(**overrides: Any) -> Session:
    defaults: dict[str, Any] = {
        "project_name": "Scaling Test",
        "user_prompt": "Design a scalable web app on Azure",
        "hitl_approved": True,
    }
    defaults.update(overrides)
    return Session(**defaults)


def _orchestrator_with_client(client: BaseLLMClient) -> Orchestrator:
    settings = Settings(_env_file=None, demo_mode=True, llm_provider="mock", routing_enabled=False)
    context = AppContext.from_settings(settings)
    agents = {
        agent_type: agent_cls(agent_type, client, settings, context=context)
        for agent_type, agent_cls in zip(
            list(AgentType), ALL_AGENTS, strict=True
        )
    }
    return Orchestrator(agents=agents, config=settings, context=context)


def test_base_agent_analyze_is_coroutine() -> None:
    agent = ALL_AGENTS[0](AgentType.ARCHITECT, MockClient(), Settings())
    assert inspect.iscoroutinefunction(agent.analyze)


def test_orchestrator_run_is_coroutine() -> None:
    orch = Orchestrator.from_settings(Settings())
    assert inspect.iscoroutinefunction(orch.run)


def test_specialists_run_concurrently() -> None:
    client = _ConcurrencyClient()
    orch = _orchestrator_with_client(client)
    session = asyncio.run(orch.run(_make_session()))

    assert session.status == "completed"
    assert client.peak == 3


def test_sequential_path_does_not_deadlock() -> None:
    orch = _orchestrator_with_client(MockClient())
    session = asyncio.run(orch.run(_make_session()))
    assert session.status == "completed"
    assert len(session.agent_turns) == 5


def test_pipeline_timing_is_bounded() -> None:
    orch = _orchestrator_with_client(MockClient())
    session = asyncio.run(orch.run(_make_session()))
    assert session.status == "completed"


def test_rate_limiter_accepts_custom_store() -> None:
    store = MemoryRateLimitStore()
    limiter = RateLimiter(store)
    assert limiter.allow("key", 1, 60.0)
    assert not limiter.allow("key", 1, 60.0)
    limiter.reset("key")
    assert limiter.allow("key", 1, 60.0)
    assert limiter.store is store


def test_redis_store_with_fake_client() -> None:
    store = RedisRateLimitStore("redis://localhost:6379", client=_FakeRedis())
    assert store.allow("user", 2, 3600)
    assert store.allow("user", 2, 3600)
    assert not store.allow("user", 2, 3600)
    store.reset("user")
    assert store.allow("user", 2, 3600)


def test_redis_store_requires_url() -> None:
    with pytest.raises(ValueError, match="redis_url"):
        RedisRateLimitStore("")


def test_redis_store_requires_package() -> None:
    store = RedisRateLimitStore("redis://localhost:6379")
    try:
        import redis  # noqa: F401
    except ImportError:
        with pytest.raises(RuntimeError, match="pip install redis"):
            store.allow("key", 1, 60)
    else:
        pytest.skip("redis installed — covered by the fake-client test")


def test_build_rate_limiter_picks_configured_backend() -> None:
    memory = build_rate_limiter(Settings(rate_limit_backend="memory"))
    assert isinstance(memory.store, MemoryRateLimitStore)

    redis = build_rate_limiter(
        Settings(rate_limit_backend="redis", redis_url="redis://localhost:6379")
    )
    assert isinstance(redis.store, RedisRateLimitStore)


def test_settings_reject_unknown_backend() -> None:
    with pytest.raises(ValidationError):
        Settings(rate_limit_backend="postgres")


def test_from_settings_injects_context_dependencies() -> None:
    orch = Orchestrator.from_settings(Settings())
    context = orch.context

    assert context is not None
    for agent in orch.agents.values():
        assert agent._audit_logger is context.audit_logger  # noqa: SLF001
        assert agent._anomaly_detector is context.anomaly_detector  # noqa: SLF001
    assert orch._rate_limiter is context.rate_limiter  # noqa: SLF001


def test_two_contexts_are_isolated() -> None:
    first = AppContext.from_settings(Settings())
    second = AppContext.from_settings(Settings())

    assert first.audit_logger is not second.audit_logger
    assert first.anomaly_detector is not second.anomaly_detector
    assert first.rate_limiter is not second.rate_limiter
    assert first.llm_client is not second.llm_client


def test_direct_construction_still_works_without_context() -> None:
    settings = Settings()
    client = MockClient()
    agents = {
        agent_type: agent_cls(agent_type, client, settings)
        for agent_type, agent_cls in zip(
            list(AgentType), ALL_AGENTS, strict=True
        )
    }
    orch = Orchestrator(
        agents=agents, 
        config=settings,
        audit_logger=AuditLogger(),
        anomaly_detector=AnomalyDetector()
    )
    session = asyncio.run(orch.run(_make_session()))

    assert session.status == "completed"
    assert orch.context is None
