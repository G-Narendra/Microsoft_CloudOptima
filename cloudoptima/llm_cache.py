"""LLM response caching with in-memory and Redis backends."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
import gzip
import hashlib
import json
import logging
import threading
import time
from typing import Any

_logger = logging.getLogger(__name__)

try:
    import redis
    _REDIS_AVAILABLE = True
except ImportError:
    _REDIS_AVAILABLE = False

try:
    import numpy as np
    _NUMPY_AVAILABLE = True
except ImportError:
    _NUMPY_AVAILABLE = False

try:
    import openai
    _OPENAI_AVAILABLE = True
except ImportError:
    _OPENAI_AVAILABLE = False


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


class BaseLLMCache(ABC):
    """Abstract base class for LLM response caching."""
    
    @abstractmethod
    def get(self, prompt: str, system_prompt: str, model: str, temperature: float) -> str | None: ...
    
    @abstractmethod
    def put(self, prompt: str, system_prompt: str, model: str, temperature: float, response: str) -> None: ...
    
    @abstractmethod
    def clear(self) -> None: ...
    
    @abstractmethod
    def stats(self) -> dict[str, Any]: ...


class LLMCache(BaseLLMCache):
    """Thread-safe in-memory cache with compression, TTL, and size eviction."""

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
        """Generate SHA-256 cache key from request parameters."""
        raw = f"{prompt}|{system_prompt}|{model}|{temperature}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    @staticmethod
    def _is_error_response(response: str) -> bool:
        """Check if response contains an error structure."""
        try:
            data = json.loads(response)
            if isinstance(data, dict) and "error" in data:
                return True
        except (json.JSONDecodeError, TypeError):
            pass
        return False

    def _total_size(self) -> int:
        """Sum of stored entry sizes in bytes."""
        return sum(entry.size_bytes for entry in self._store.values())

    def _evict_oldest(self) -> None:
        """Drop oldest 20% of entries when over capacity."""
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
        """Return cached response, or None on miss/expiry/error."""
        try:
            key = self._make_key(prompt, system_prompt, model, temperature)
            with self._lock:
                entry = self._store.get(key)
                if entry is None:
                    self._stats.misses += 1
                    return None

                age = time.time() - entry.timestamp
                if age > self._ttl_seconds:
                    del self._store[key]
                    self._stats.misses += 1
                    _logger.debug("Cache entry expired (age=%.0fs)", age)
                    return None

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
        """Store response in cache, skipping errors and evicting if needed."""
        try:
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
        """Return cache hit/miss statistics."""
        with self._lock:
            return {
                "entries": len(self._store),
                "total_size_bytes": self._total_size(),
                "hits": self._stats.hits,
                "misses": self._stats.misses,
                "evictions": self._stats.evictions,
                "errors": self._stats.errors,
            }


class RedisLLMCache(BaseLLMCache):
    """Distributed Redis-backed LLM response cache."""
    
    def __init__(self, url: str, ttl_hours: int = 24, max_size_mb: int = 200) -> None:
        if not url:
            raise ValueError("redis_url is required for RedisLLMCache")
        self._url = url
        self._ttl_seconds = ttl_hours * 3600
        self._client: Any = None
        self._stats = CacheStats()
        self._prefix = "llmcache:"

    def _get_client(self) -> Any:
        if self._client is None:
            if not _REDIS_AVAILABLE:
                raise RuntimeError("redis package is required for RedisLLMCache")
            self._client = redis.from_url(self._url)
        return self._client
    
    def get(self, prompt: str, system_prompt: str, model: str, temperature: float) -> str | None:
        try:
            key = self._prefix + LLMCache._make_key(prompt, system_prompt, model, temperature)
            client = self._get_client()
            compressed = client.get(key)
            if compressed is None:
                self._stats.misses += 1
                return None
            
            raw = gzip.decompress(compressed)
            self._stats.hits += 1
            return raw.decode("utf-8")
        except Exception:
            _logger.warning("Redis cache get error", exc_info=True)
            self._stats.errors += 1
            return None

    def put(self, prompt: str, system_prompt: str, model: str, temperature: float, response: str) -> None:
        try:
            if LLMCache._is_error_response(response):
                _logger.debug("Skipping cache for error response")
                return
            
            key = self._prefix + LLMCache._make_key(prompt, system_prompt, model, temperature)
            compressed = gzip.compress(response.encode("utf-8"))
            client = self._get_client()
            client.set(key, compressed, ex=self._ttl_seconds)
        except Exception:
            _logger.warning("Redis cache put error", exc_info=True)
            self._stats.errors += 1

    def clear(self) -> None:
        try:
            client = self._get_client()
            for key in client.scan_iter(f"{self._prefix}*"):
                client.delete(key)
            _logger.info("Redis cache cleared")
        except Exception:
            _logger.warning("Redis cache clear error", exc_info=True)
            self._stats.errors += 1

    def stats(self) -> dict[str, Any]:
        return {
            "entries": -1,
            "total_size_bytes": -1,
            "hits": self._stats.hits,
            "misses": self._stats.misses,
            "evictions": self._stats.evictions,
            "errors": self._stats.errors,
        }


class SemanticRedisLLMCache(BaseLLMCache):
    """Distributed Redis-backed Semantic LLM response cache."""
    
    def __init__(self, url: str, ttl_hours: int = 24, similarity_threshold: float = 0.98) -> None:
        if not url:
            raise ValueError("redis_url is required for SemanticRedisLLMCache")
        self._url = url
        self._ttl_seconds = ttl_hours * 3600
        self._similarity_threshold = similarity_threshold
        self._client: Any = None
        self._stats = CacheStats()
        self._prefix = "semcache:"

    def _get_client(self) -> Any:
        if self._client is None:
            if not _REDIS_AVAILABLE:
                raise RuntimeError("redis package is required for SemanticRedisLLMCache")
            self._client = redis.from_url(self._url)
        return self._client

    def _get_embedding(self, text: str) -> list[float]:
        if _OPENAI_AVAILABLE:
            try:
                client = openai.Client()
                response = client.embeddings.create(input=text, model="text-embedding-3-small")
                return response.data[0].embedding
            except Exception:
                pass

        _logger.debug("Falling back to deterministic embedding generation")
        h = hashlib.sha256(text.encode("utf-8")).digest()
        vec = [(float(b) / 255.0) - 0.5 for b in h]
        vec = vec * (1536 // len(vec))
        length = sum(v * v for v in vec) ** 0.5
        return [v / length for v in vec]
    
    def get(self, prompt: str, system_prompt: str, model: str, temperature: float) -> str | None:
        try:
            client = self._get_client()
            
            exact_key = f"{self._prefix}exact:{LLMCache._make_key(prompt, system_prompt, model, temperature)}"
            compressed = client.get(exact_key)
            if compressed is not None:
                self._stats.hits += 1
                return gzip.decompress(compressed).decode("utf-8")
            
            if _NUMPY_AVAILABLE:
                query_emb = np.array(self._get_embedding(prompt), dtype=np.float32).tobytes()
                try:
                    q = (
                        f"(@system_prompt:{{{system_prompt}}} @model:{{{model}}}) "
                        f"=>[KNN 1 @prompt_vector $vec AS score]"
                    )
                    res = client.execute_command(
                        "FT.SEARCH", "idx:semcache", q, 
                        "PARAMS", "2", "vec", query_emb,
                        "DIALECT", "2",
                        "RETURN", "2", "score", "response"
                    )
                    if res and len(res) > 2 and isinstance(res[2], list):
                        fields = res[2]
                        score_idx = fields.index(b"score") + 1
                        resp_idx = fields.index(b"response") + 1
                        score = float(fields[score_idx])
                        similarity = 1.0 - score
                        
                        if similarity >= self._similarity_threshold:
                            compressed_resp = fields[resp_idx]
                            self._stats.hits += 1
                            return gzip.decompress(compressed_resp).decode("utf-8")
                except Exception:
                    pass

            self._stats.misses += 1
            return None
        except Exception:
            _logger.warning("Semantic Redis cache get error", exc_info=True)
            self._stats.errors += 1
            return None

    def put(self, prompt: str, system_prompt: str, model: str, temperature: float, response: str) -> None:
        try:
            if LLMCache._is_error_response(response):
                return
                
            client = self._get_client()
            
            exact_key = f"{self._prefix}exact:{LLMCache._make_key(prompt, system_prompt, model, temperature)}"
            compressed = gzip.compress(response.encode("utf-8"))
            client.set(exact_key, compressed, ex=self._ttl_seconds)
            
            if _NUMPY_AVAILABLE:
                emb_bytes = np.array(self._get_embedding(prompt), dtype=np.float32).tobytes()
                semantic_key = f"{self._prefix}hash:{hashlib.sha256(prompt.encode('utf-8')).hexdigest()}"
                client.hset(semantic_key, mapping={
                    "prompt": prompt,
                    "system_prompt": system_prompt,
                    "model": model,
                    "prompt_vector": emb_bytes,
                    "response": compressed
                })
                client.expire(semantic_key, self._ttl_seconds)
            
        except Exception:
            _logger.warning("Semantic Redis cache put error", exc_info=True)
            self._stats.errors += 1

    def clear(self) -> None:
        try:
            client = self._get_client()
            for key in client.scan_iter(f"{self._prefix}*"):
                client.delete(key)
        except Exception:
            self._stats.errors += 1

    def stats(self) -> dict[str, Any]:
        return {
            "entries": -1,
            "total_size_bytes": -1,
            "hits": self._stats.hits,
            "misses": self._stats.misses,
            "evictions": self._stats.evictions,
            "errors": self._stats.errors,
        }
