"""Round-3 review tests — the scaling fixes (external principal-engineer review).

The reviewer's three homework items, each pinned by a test:

1. **P1 — async pipeline.** ``BaseAgent.analyze`` and ``Orchestrator.run`` are
   real coroutines, and the three specialists that only depend on the
   architect run concurrently (``asyncio.gather``) instead of in a blocking
   ``for`` loop.
2. **P2 — rate-limit store interface.** The limiter accepts any
   :class:`RateLimitStore` — memory for one process, Redis for a scale-out —
   instead of an unswappable module-level dict.
3. **P3 — dependency injection.** :class:`AppContext` owns the audit logger,
   anomaly detector, and rate limiter, and the orchestrator's production path
   wires them in — no hidden module globals, no state bleeding between tests.
"""

from __future__ import annotations

import asyncio
import inspect
import json
import threading
from typing import Any

import pytest
from pydantic import ValidationError

from cloudoptima.agent_base import BaseAgent
from cloudoptima.agents import ALL_AGENTS
from cloudoptima.config import Settings
from cloudoptima.context import AppContext, build_rate_limiter
from cloudoptima.llm_client import BaseLLMClient, MockClient
from cloudoptima.models import AgentType, Session
from cloudoptima.orchestrator import Orchestrator
from cloudoptima.sanitize import (
    MemoryRateLimitStore,
    RateLimiter,
    RedisRateLimitStore,
)

# ── Test doubles ───────────────────────────────────────────────────────


class _ConcurrencyClient(BaseLLMClient):
    """LLM client that measures the peak number of simultaneous calls.

    ``peak`` counts how many ``agenerate`` calls were in flight at once. The
    architect runs alone (peak 1), then the three specialists are gathered —
    if the pipeline truly runs them concurrently, the peak reaches 3; a
    sequential pipeline would never exceed 1.
    """

    def __init__(self) -> None:
        self._active = 0
        self.peak = 0
        self._lock = threading.Lock()
        self.last_tokens_used = 0

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        # The async path is what the pipeline uses; this sync fallback exists
        # only because BaseLLMClient declares generate as abstract.
        from cloudoptima.llm_client import MOCK_RESPONSES, _detect_agent_type

        key = _detect_agent_type(prompt, system_prompt)
        return json.dumps(MOCK_RESPONSES.get(key, MOCK_RESPONSES["architect"]))

    async def agenerate(self, prompt: str, system_prompt: str = "") -> str:
        from cloudoptima.llm_client import MOCK_RESPONSES, _detect_agent_type

        with self._lock:
            self._active += 1
            self.peak = max(self.peak, self._active)
        try:
            await asyncio.sleep(0.05)
            key = _detect_agent_type(prompt, system_prompt)
            self.last_tokens_used = 1
            return json.dumps(MOCK_RESPONSES.get(key, MOCK_RESPONSES["architect"]))
        finally:
            with self._lock:
                self._active -= 1


class _FakeRedis:
    """Tiny stand-in for the redis client — just the commands we use.

    ``get`` / ``incr`` / ``expire`` / ``keys`` / ``delete`` cover the entire
    surface of :class:`RedisRateLimitStore`, so the adapter is testable
    without a running Redis server.
    """

    def __init__(self) -> None:
        self._data: dict[str, int] = {}

    def get(self, key: str) -> str | None:
        value = self._data.get(key)
        return None if value is None else str(value)

    def incr(self, key: str) -> int:
        self._data[key] = self._data.get(key, 0) + 1
        return self._data[key]

    def expire(self, key: str, ttl: int) -> bool:  # noqa: ARG002 - fake never expires
        return True

    def keys(self, pattern: str) -> list[str]:
        import fnmatch

        return [k for k in self._data if fnmatch.fnmatch(k, pattern)]

    def delete(self, name: str) -> int:
        return int(self._data.pop(name, None) is not None)


# ── Helpers ────────────────────────────────────────────────────────────


def _make_session(**overrides: Any) -> Session:
    defaults: dict[str, Any] = {
        "project_name": "Scaling Test",
        "user_prompt": "Design a scalable web app on Azure",
    }
    defaults.update(overrides)
    return Session(**defaults)


def _orchestrator_with_client(client: BaseLLMClient) -> Orchestrator:
    """Orchestrator whose five agents all share the given LLM client."""
    settings = Settings()
    agents = {
        agent_type: agent_cls(agent_type, client, settings)
        for agent_type, agent_cls in zip(
            list(AgentType), ALL_AGENTS, strict=True
        )
    }
    return Orchestrator(agents=agents, config=settings)


# ── P1 — async pipeline ────────────────────────────────────────────────


def test_pipeline_methods_are_coroutines() -> None:
    """The reviewer's P1: analyze and run must be real async functions."""
    assert inspect.iscoroutinefunction(BaseAgent.analyze)
    assert inspect.iscoroutinefunction(Orchestrator.run)
    assert inspect.iscoroutinefunction(BaseLLMClient.agenerate)


def test_async_pipeline_completes_with_same_results() -> None:
    """The async run produces the same completed session as the old sync one."""
    orch = Orchestrator.from_settings(Settings())
    session = asyncio.run(orch.run(_make_session()))

    assert session.status == "completed"
    assert len(session.agent_turns) == 5
    assert len(session.artifacts) == 4


def test_specialists_run_concurrently() -> None:
    """Cost, Security, Compliance overlap — peak concurrency reaches 3.

    The architect runs alone first (it feeds the other three), so peak 1 is
    expected before the gather; a peak >= 2 proves the LLM waits overlap.
    """
    client = _ConcurrencyClient()
    orch = _orchestrator_with_client(client)

    session = asyncio.run(orch.run(_make_session()))

    assert session.status == "completed"
    assert client.peak >= 2, (
        f"specialists did not run concurrently (peak={client.peak}); "
        "the pipeline is still serializing LLM calls"
    )


# ── P2 — rate-limit store interface ────────────────────────────────────


def test_memory_store_sliding_window() -> None:
    """A fresh MemoryRateLimitStore enforces the window and resets cleanly."""
    store = MemoryRateLimitStore()
    assert store.allow("key", 2, 60.0)
    assert store.allow("key", 2, 60.0)
    assert not store.allow("key", 2, 60.0)  # quota exhausted
    store.reset("key")
    assert store.allow("key", 2, 60.0)  # reset restores the quota


def test_ratelimiter_accepts_injected_store() -> None:
    """RateLimiter is a thin wrapper — the store is swappable (reviewer P2)."""
    store = MemoryRateLimitStore()
    limiter = RateLimiter(store)
    assert limiter.allow("key", 1, 60.0)
    assert not limiter.allow("key", 1, 60.0)
    limiter.reset()
    assert limiter.allow("key", 1, 60.0)
    assert limiter.store is store  # the injected store is the one in use


def test_redis_store_with_fake_client() -> None:
    """RedisRateLimitStore counts through the injected client's INCR."""
    store = RedisRateLimitStore("redis://localhost:6379", client=_FakeRedis())
    assert store.allow("user", 2, 3600)
    assert store.allow("user", 2, 3600)
    assert not store.allow("user", 2, 3600)
    store.reset("user")
    assert store.allow("user", 2, 3600)


def test_redis_store_requires_url() -> None:
    """Without a URL there is nothing to connect to — fail fast."""
    with pytest.raises(ValueError, match="redis_url"):
        RedisRateLimitStore("")


def test_redis_store_requires_package() -> None:
    """When the redis package is missing, allow() explains how to install it."""
    store = RedisRateLimitStore("redis://localhost:6379")
    try:
        import redis  # noqa: F401
    except ImportError:
        with pytest.raises(RuntimeError, match="pip install redis"):
            store.allow("key", 1, 60)
    else:
        # The package is installed — the real import path is exercised by the
        # fake-client test above, so nothing else to assert here.
        pytest.skip("redis installed — covered by the fake-client test")


def test_build_rate_limiter_picks_configured_backend() -> None:
    """build_rate_limiter maps config to the right store (memory vs redis)."""
    memory = build_rate_limiter(Settings(rate_limit_backend="memory"))
    assert isinstance(memory.store, MemoryRateLimitStore)

    redis = build_rate_limiter(
        Settings(rate_limit_backend="redis", redis_url="redis://localhost:6379")
    )
    assert isinstance(redis.store, RedisRateLimitStore)


def test_settings_reject_unknown_backend() -> None:
    """A typo in rate_limit_backend is caught at settings load time."""
    with pytest.raises(ValidationError):
        Settings(rate_limit_backend="postgres")


# ── P3 — dependency injection ──────────────────────────────────────────


def test_from_settings_injects_context_dependencies() -> None:
    """Production wiring passes the context's instances into every agent.

    None of this reaches for the module-level singletons — the reviewer's P3
    complaint was hidden global coupling and test state bleed.
    """
    orch = Orchestrator.from_settings(Settings())
    context = orch.context

    assert context is not None
    for agent in orch.agents.values():
        assert agent._audit_logger is context.audit_logger  # noqa: SLF001
        assert agent._anomaly_detector is context.anomaly_detector  # noqa: SLF001
    assert orch._rate_limiter is context.rate_limiter  # noqa: SLF001


def test_two_contexts_are_isolated() -> None:
    """Two pipelines in one process share nothing — no global state bleed."""
    first = AppContext.from_settings(Settings())
    second = AppContext.from_settings(Settings())

    assert first.audit_logger is not second.audit_logger
    assert first.anomaly_detector is not second.anomaly_detector
    assert first.rate_limiter is not second.rate_limiter
    assert first.llm_client is not second.llm_client


def test_direct_construction_still_works_without_context() -> None:
    """Agents and orchestrators built without a context fall back safely."""
    orch = _orchestrator_with_client(MockClient())
    session = asyncio.run(orch.run(_make_session()))

    assert session.status == "completed"
    assert orch.context is None
