"""AppContext — one container that owns every shared dependency (round-3 P3).

Round 3 of the external principal-engineer review called out module-level
singletons (audit logger, anomaly detector, rate limiter) as hidden coupling:
every test had to reset global state, and nothing could run two isolated
pipelines side by side. :class:`AppContext` bundles the shared objects the
pipeline needs so they are created once, owned by one container, and passed
down into agents and the orchestrator instead of fetched from globals.

Typical usage:
    >>> from cloudoptima.config import Settings
    >>> from cloudoptima.context import AppContext
    >>> ctx = AppContext.from_settings(Settings())
    >>> ctx.audit_logger           # one AuditLogger, owned by this container
"""

from __future__ import annotations

from dataclasses import dataclass

from cloudoptima.config import Settings
from cloudoptima.llm_client import BaseLLMClient, create_llm_client
from cloudoptima.llm_routing import create_routed_client
from cloudoptima.observability import AnomalyDetector, AuditLogger
from cloudoptima.sanitize import MemoryRateLimitStore, RateLimiter, RedisRateLimitStore


def build_rate_limiter(settings: Settings) -> RateLimiter:
    """Build the rate limiter for the configured backend (round-3 P2).

    ``memory`` keeps the old single-process sliding window; ``redis`` moves
    the counters to a shared store so a scaled-out deployment enforces one
    global quota instead of one per worker.

    Args:
        settings: The application settings (backend + redis URL).

    Returns:
        A :class:`RateLimiter` backed by the configured store.
    """
    if settings.rate_limit_backend == "redis":
        return RateLimiter(RedisRateLimitStore(settings.redis_url))
    return RateLimiter(MemoryRateLimitStore())


@dataclass
class AppContext:
    """Everything the pipeline needs, owned in one place.

    Attributes:
        settings:        The application settings (model, limits, backend).
        llm_client:      The LLM backend every agent calls (mock/real/router).
        audit_logger:    Append-only audit log for this context.
        anomaly_detector: Per-agent response/token anomaly baselines.
        rate_limiter:    The global quota limiter for pipeline runs.
    """

    settings: Settings
    llm_client: BaseLLMClient
    audit_logger: AuditLogger
    anomaly_detector: AnomalyDetector
    rate_limiter: RateLimiter

    @classmethod
    def from_settings(cls, settings: Settings) -> AppContext:
        """Build a fully-wired context from application settings.

        Creates the LLM client (routed when ``routing_enabled``, else the
        plain provider client) and fresh instances of the logger, detector,
        and rate limiter — no module-global singletons in this path.

        Args:
            settings: The application :class:`Settings`.

        Returns:
            A ready-to-use :class:`AppContext`.
        """
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
        )
