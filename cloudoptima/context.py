"""Application context container managing shared dependencies."""

from __future__ import annotations

from dataclasses import dataclass

from cloudoptima.compliance.rag import ComplianceRAG
from cloudoptima.config import Settings
from cloudoptima.llm_cache import BaseLLMCache, LLMCache, RedisLLMCache
from cloudoptima.llm_client import BaseLLMClient, create_llm_client
from cloudoptima.llm_routing import create_routed_client
from cloudoptima.observability import AnomalyDetector, AuditLogger
from cloudoptima.sanitize import MemoryRateLimitStore, RateLimiter, RedisRateLimitStore


def build_cache(settings: Settings) -> BaseLLMCache:
    """Build the LLM cache backed by Redis or memory depending on settings."""
    if settings.redis_url:
        return RedisLLMCache(
            url=settings.redis_url,
            ttl_hours=settings.cache_ttl_hours,
            max_size_mb=settings.cache_max_size_mb,
        )
    return LLMCache(
        ttl_hours=settings.cache_ttl_hours,
        max_size_mb=settings.cache_max_size_mb,
    )


def build_rate_limiter(settings: Settings) -> RateLimiter:
    """Build the rate limiter for the configured backend (memory or redis)."""
    if settings.rate_limit_backend == "redis":
        return RateLimiter(RedisRateLimitStore(settings.redis_url))
    return RateLimiter(MemoryRateLimitStore())


@dataclass
class AppContext:
    """Dependency container for pipeline execution."""

    settings: Settings
    llm_client: BaseLLMClient
    audit_logger: AuditLogger
    anomaly_detector: AnomalyDetector
    rate_limiter: RateLimiter
    rag: ComplianceRAG
    cache: BaseLLMCache

    @classmethod
    def from_settings(cls, settings: Settings) -> AppContext:
        """Build a fully-wired context from application settings."""
        llm_client: BaseLLMClient = (
            create_routed_client(settings)
            if settings.routing_enabled
            else create_llm_client(settings)
        )
        return cls(
            settings=settings,
            llm_client=llm_client,
            audit_logger=AuditLogger(settings.audit_log_dir),
            anomaly_detector=AnomalyDetector(),
            rate_limiter=build_rate_limiter(settings),
            rag=ComplianceRAG(settings),
            cache=build_cache(settings),
        )
