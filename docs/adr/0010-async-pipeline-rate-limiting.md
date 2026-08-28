# ADR 0010: Async Pipeline & Pluggable Rate Limiting

## Status
Accepted

## Context
Synchronous LLM calls block worker threads, capping enterprise concurrency. In-memory rate limiting fails across multi-worker distributed deployments.

## Decision
- Convert `BaseAgent.analyze()` and `Orchestrator.run()` to native coroutines.
- Execute Cost, Security, and Compliance agents concurrently via `asyncio.gather()`.
- Introduce `RateLimitStore` protocol with `MemoryRateLimitStore` (local default) and `RedisRateLimitStore` (distributed production).
- Introduce `AppContext` dependency container to eliminate singleton state bleed.

## Consequences
- **Positive:** Pipeline execution drops from ~1.5s to ~0.5s for warm queries. Redis integration allows distributed worker scaling on Azure App Service.
- **Negative:** Increases complexity in tracking context and debugging async stack traces.
