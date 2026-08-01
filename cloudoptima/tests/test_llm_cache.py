"""Tests for LLM response cache."""

from __future__ import annotations

import json
import threading
import time
from unittest.mock import patch

from cloudoptima.llm_cache import LLMCache

# ── Cache Hit / Miss ──────────────────────────────────────────────────────────


def test_cache_hit() -> None:
    """Cached response is returned on subsequent get with same key."""
    cache = LLMCache(ttl_hours=1, max_size_mb=10)
    response = '{"compute": "AKS", "storage": "Blob"}'

    cache.put("prompt1", "system1", "gpt-4o-mini", 0.1, response)
    result = cache.get("prompt1", "system1", "gpt-4o-mini", 0.1)

    assert result == response


def test_cache_miss() -> None:
    """Unknown key returns None."""
    cache = LLMCache(ttl_hours=1, max_size_mb=10)
    result = cache.get("never_seen", "system", "model", 0.1)

    assert result is None


# ── TTL Expiry ────────────────────────────────────────────────────────────────


def test_cache_expiry() -> None:
    """Entry older than TTL returns None and is evicted."""
    cache = LLMCache(ttl_hours=1, max_size_mb=10)
    response = '{"data": "test"}'

    cache.put("prompt", "system", "model", 0.1, response)

    # Mock time to be 2 hours in the future
    with patch("cloudoptima.llm_cache.time") as mock_time:
        mock_time.time.return_value = time.time() + 7200  # 2 hours later
        result = cache.get("prompt", "system", "model", 0.1)

    assert result is None


# ── Size-Based Eviction ──────────────────────────────────────────────────────


def test_cache_eviction() -> None:
    """When size limit exceeded, oldest 20% of entries are removed."""
    # Create a tiny cache (1 byte max to force eviction on every put)
    cache = LLMCache(ttl_hours=24, max_size_mb=1)
    # Override to a very small size limit
    cache._max_size_bytes = 100  # 100 bytes — will fill up fast

    # Add entries with increasing timestamps
    for i in range(10):
        cache.put(
            f"prompt_{i}", "system", "model", 0.1,
            json.dumps({"index": i, "padding": "x" * 20}),
        )

    stats = cache.stats()
    # Some entries should have been evicted
    assert stats["entries"] < 10
    assert stats["evictions"] > 0


# ── Error Response Not Cached ─────────────────────────────────────────────────


def test_cache_error_not_stored() -> None:
    """Responses with 'error' key in top-level JSON are not cached."""
    cache = LLMCache(ttl_hours=1, max_size_mb=10)
    error_response = '{"error": "rate_limit_exceeded", "message": "Too many requests"}'

    cache.put("prompt", "system", "model", 0.1, error_response)
    result = cache.get("prompt", "system", "model", 0.1)

    assert result is None


# ── Thread Safety ─────────────────────────────────────────────────────────────


def test_cache_thread_safety() -> None:
    """Concurrent reads and writes don't corrupt state or raise exceptions."""
    cache = LLMCache(ttl_hours=1, max_size_mb=10)
    errors: list[Exception] = []

    def writer(thread_id: int) -> None:
        try:
            for i in range(20):
                cache.put(
                    f"prompt_{thread_id}_{i}", "system", "model", 0.1,
                    json.dumps({"thread": thread_id, "iteration": i}),
                )
        except Exception as exc:
            errors.append(exc)

    def reader(thread_id: int) -> None:
        try:
            for i in range(20):
                cache.get(f"prompt_{thread_id}_{i}", "system", "model", 0.1)
        except Exception as exc:
            errors.append(exc)

    threads = []
    for t_id in range(5):
        threads.append(threading.Thread(target=writer, args=(t_id,)))
        threads.append(threading.Thread(target=reader, args=(t_id,)))

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert len(errors) == 0, f"Thread safety errors: {errors}"


# ── Fault Tolerance ───────────────────────────────────────────────────────────


def test_cache_fault_tolerance() -> None:
    """Corrupted internal state returns None instead of crashing."""
    cache = LLMCache(ttl_hours=1, max_size_mb=10)

    # Store a valid entry
    cache.put("prompt", "system", "model", 0.1, '{"valid": true}')

    # Corrupt the internal store by replacing compressed data with garbage
    key = list(cache._store.keys())[0]
    cache._store[key].compressed_data = b"not-gzip-data"

    # Should return None, not crash
    result = cache.get("prompt", "system", "model", 0.1)
    assert result is None

    stats = cache.stats()
    assert stats["errors"] >= 1


# ── Stats ─────────────────────────────────────────────────────────────────────


def test_cache_stats() -> None:
    """Stats correctly track hits, misses, and entries."""
    cache = LLMCache(ttl_hours=1, max_size_mb=10)

    # Miss
    cache.get("unknown", "sys", "model", 0.1)

    # Put + hit
    cache.put("p1", "sys", "model", 0.1, '{"data": 1}')
    cache.get("p1", "sys", "model", 0.1)

    stats = cache.stats()
    assert stats["entries"] == 1
    assert stats["hits"] == 1
    assert stats["misses"] == 1
    assert stats["total_size_bytes"] > 0
