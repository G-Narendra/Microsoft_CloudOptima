"""In-memory LLM response cache.

Keys are SHA-256 hashes of the request, bodies are gzip-compressed, entries
expire on a TTL, and the oldest 20% get evicted when we pass the size cap.
The one rule that matters: it never crashes. Every error path is caught and
logged, and a miss returns None so callers just fall through to the LLM.
"""

from __future__ import annotations

import gzip
import hashlib
import json
import logging
import threading
import time
from dataclasses import dataclass
from typing import Any

_logger = logging.getLogger(__name__)


@dataclass
class CacheEntry:
    """A single cached LLM response with metadata."""

    compressed_data: bytes
    timestamp: float
    size_bytes: int


@dataclass
class CacheStats:
    """Running statistics for the cache."""

    hits: int = 0
    misses: int = 0
    evictions: int = 0
    errors: int = 0


class LLMCache:
    """Thread-safe response cache with compression, TTL, and size caps.

    Two security rules are baked in: we never store API keys (keys are hashes
    of the request, never the payload), and we refuse to cache anything that
    looks like an error response.
    """

    def __init__(self, ttl_hours: int = 24, max_size_mb: int = 200) -> None:
        self._ttl_seconds = ttl_hours * 3600
        self._max_size_bytes = max_size_mb * 1024 * 1024
        self._store: dict[str, CacheEntry] = {}
        self._lock = threading.Lock()
        self._stats = CacheStats()

    @staticmethod
    def _make_key(
        prompt: str, system_prompt: str, model: str, temperature: float
    ) -> str:
        """Generate a SHA-256 cache key from the request parameters."""
        raw = f"{prompt}|{system_prompt}|{model}|{temperature}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    @staticmethod
    def _is_error_response(response: str) -> bool:
        """True when the response is an error payload — those are never cached."""
        try:
            data = json.loads(response)
            if isinstance(data, dict) and "error" in data:
                return True
        except (json.JSONDecodeError, TypeError):
            pass
        return False

    def _total_size(self) -> int:
        """Sum of every entry's stored size in bytes."""
        return sum(entry.size_bytes for entry in self._store.values())

    def _evict_oldest(self) -> None:
        """Drop the oldest 20% (at least one entry) once we're over the cap."""
        if not self._store:
            return

        count_to_remove = max(1, len(self._store) // 5)
        sorted_keys = sorted(
            self._store.keys(),
            key=lambda k: self._store[k].timestamp,
        )

        for key in sorted_keys[:count_to_remove]:
            del self._store[key]
            self._stats.evictions += 1

        _logger.info(
            "Cache eviction: removed %d entries, %d remaining",
            count_to_remove,
            len(self._store),
        )

    def get(
        self,
        prompt: str,
        system_prompt: str,
        model: str,
        temperature: float,
    ) -> str | None:
        """Return the cached response for a request, or None on miss/expiry/error."""
        try:
            key = self._make_key(prompt, system_prompt, model, temperature)
            with self._lock:
                entry = self._store.get(key)
                if entry is None:
                    self._stats.misses += 1
                    return None

                # Check TTL expiry
                age = time.time() - entry.timestamp
                if age > self._ttl_seconds:
                    del self._store[key]
                    self._stats.misses += 1
                    _logger.debug("Cache entry expired (age=%.0fs)", age)
                    return None

                # Decompress and return
                raw = gzip.decompress(entry.compressed_data)
                self._stats.hits += 1
                return raw.decode("utf-8")

        except Exception:
            _logger.warning("Cache get error", exc_info=True)
            self._stats.errors += 1
            return None

    def put(
        self,
        prompt: str,
        system_prompt: str,
        model: str,
        temperature: float,
        response: str,
    ) -> None:
        """Store a response, skipping error payloads and evicting if over the cap."""
        try:
            # Security: don't cache error responses
            if self._is_error_response(response):
                _logger.debug("Skipping cache for error response")
                return

            key = self._make_key(prompt, system_prompt, model, temperature)
            compressed = gzip.compress(response.encode("utf-8"))

            with self._lock:
                self._store[key] = CacheEntry(
                    compressed_data=compressed,
                    timestamp=time.time(),
                    size_bytes=len(compressed),
                )

                # Evict if over size limit
                if self._total_size() > self._max_size_bytes:
                    self._evict_oldest()

        except Exception:
            _logger.warning("Cache put error", exc_info=True)
            self._stats.errors += 1

    def clear(self) -> None:
        """Remove all entries from the cache."""
        with self._lock:
            self._store.clear()
            _logger.info("Cache cleared")

    def stats(self) -> dict[str, Any]:
        """Return hit/miss/eviction counters and current size for monitoring."""
        with self._lock:
            return {
                "entries": len(self._store),
                "total_size_bytes": self._total_size(),
                "hits": self._stats.hits,
                "misses": self._stats.misses,
                "evictions": self._stats.evictions,
                "errors": self._stats.errors,
            }
