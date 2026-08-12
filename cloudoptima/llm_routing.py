"""Cost-aware LLM provider routing (Phase 7.5 / 7.6).

Instead of pinning the app to one provider, :class:`CostAwareRouter` picks the
cheapest *enabled* provider with credentials for each call and fails over
automatically when one is down or rate-limited (the Nvidia NIM free tier is
famously 429-prone).

Real-world behaviors:

- **Price-ordered selection.** Providers are tried cheapest-first from a
  per-model price table (Nvidia NIM is $0; Azure/OpenAI/Claude/Gemini bill per
  token). "Cheapest adequate, not cheapest imaginable": the Architect and the
  Judge get the ``smart`` tier, the other specialists the cheaper ``fast``
  tier.
- **Rate-limit-aware failover.** A provider that keeps failing is demoted
  behind healthier ones until a call succeeds again, shifting load to the
  next-cheapest.
- **Spend guard.** A request whose estimated input cost would exceed
  ``routing_max_cost_per_request`` skips that provider — belt and suspenders
  on top of price ordering.
- **Spend tracking.** Every call records estimated USD spend per provider
  (:meth:`CostAwareRouter.stats`).
- **Mock safety net.** If routing is on but no real provider has credentials,
  the router falls back to :class:`MockClient` so demos never crash on
  missing keys.

Typical usage:
    >>> settings = Settings(routing_enabled=True)
    >>> client = create_routed_client(settings)
    >>> text = client.generate("...", "You are a senior cloud architect.")
    >>> client.stats()
    {'nvidia': {'calls': 1, 'failures': 0, 'consecutive_failures': 0, 'spend_usd': 0.0}}
"""

from __future__ import annotations

import logging
import threading
from collections import defaultdict
from dataclasses import asdict, dataclass
from typing import Final

from cloudoptima.config import Settings
from cloudoptima.llm_client import (
    AnthropicClient,
    AzureClient,
    BaseLLMClient,
    GoogleClient,
    MockClient,
    NvidiaClient,
    OpenAIClient,
    _detect_agent_type,
)

_logger = logging.getLogger(__name__)

# ── Model price table (USD per 1M tokens: input, output) ────────────────
# Nvidia NIM free tier (build.nvidia.com) is $0 but rate-limited. The rest use
# published 2026 list prices: Azure OpenAI and OpenAI pay-as-you-go, Anthropic
# Claude, Google Gemini. Prices drive cheapest-first selection and spend
# tracking, so they are deliberately conservative where unknown.
MODEL_PRICES: Final[dict[str, tuple[float, float]]] = {
    "mock": (0.0, 0.0),
    "meta/llama-3.3-70b-instruct": (0.0, 0.0),
    "meta/llama-3.1-8b-instruct": (0.0, 0.0),
    "nvidia/llama-3.1-nemotron-70b-instruct": (0.0, 0.0),
    "deepseek-ai/deepseek-r1": (0.0, 0.0),
    "gpt-4o-mini": (0.15, 0.60),
    "gpt-4o": (2.50, 10.00),
    "gpt-4.1": (2.00, 8.00),
    "gpt-4.1-mini": (0.40, 1.60),
    "claude-sonnet-4-20250514": (3.00, 15.00),
    "claude-3-5-haiku-20241022": (0.80, 4.00),
    "claude-3-7-sonnet-20250219": (3.00, 15.00),
    "gemini-2.0-flash": (0.10, 0.40),
    "gemini-2.5-flash": (0.30, 2.50),
    "gemini-2.5-pro": (1.25, 10.00),
}

# Unknown models get a conservative price so they never rank ahead of known
# cheap ones.
_UNKNOWN_PRICE: Final[tuple[float, float]] = (1.0, 1.0)

# Agents that run the "smart" (strongest) tier: the architect designs, the
# judge arbitrates. The remaining specialists run the cheaper tier.
_SMART_AGENTS: Final[frozenset[str]] = frozenset({"architect", "judge"})

# Rough heuristic: ~4 characters per token.
_CHARS_PER_TOKEN: Final[int] = 4

TIER_SMART: Final[str] = "smart"
TIER_FAST: Final[str] = "fast"


def model_pricing(model: str) -> tuple[float, float]:
    """Return ``(input, output)`` USD price per 1M tokens for a model."""
    return MODEL_PRICES.get(model, _UNKNOWN_PRICE)


def estimate_cost(tokens_in: int, tokens_out: int, model: str) -> float:
    """Estimate the USD cost of a call for a given model."""
    input_price, output_price = model_pricing(model)
    return (tokens_in / 1_000_000) * input_price + (tokens_out / 1_000_000) * output_price


def estimate_tokens(text: str) -> int:
    """Rough token estimate (~4 chars per token)."""
    return max(1, len(text) // _CHARS_PER_TOKEN)


@dataclass
class ProviderStats:
    """Per-provider routing statistics."""

    calls: int = 0
    failures: int = 0
    consecutive_failures: int = 0
    spend_usd: float = 0.0


class CostAwareRouter(BaseLLMClient):
    """Route each call to the cheapest healthy provider, failing over as needed.

    Args:
        settings: Application settings (routing config, spend cap).
        clients:  Mapping of ``(provider, tier)`` to a concrete client.
        models:   Mapping of ``(provider, tier)`` to the model name used, for
            pricing and spend tracking.
    """

    _DEMOTE_AFTER_FAILURES: Final[int] = 2
    _MOCK_RANK: Final[int] = 10  # mock is always tried last (safety net)

    def __init__(
        self,
        settings: Settings,
        clients: dict[tuple[str, str], BaseLLMClient],
        models: dict[tuple[str, str], str],
    ) -> None:
        self._settings = settings
        self._clients = dict(clients)
        self._models = dict(models)
        self._stats: dict[str, ProviderStats] = defaultdict(ProviderStats)
        for provider, _tier in self._clients:
            self._stats.setdefault(provider, ProviderStats())
        # NOTE: the pipeline runs agents sequentially, so the stats dict needs
        # no lock. If generate() is ever called concurrently, guard it.
        self._lock = threading.Lock()

    # ── BaseLLMClient ──────────────────────────────────────────────────

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        """Route one call: cheapest healthy provider first, failover on error.

        Raises:
            The last provider exception when every candidate fails, or
            ``RuntimeError`` when no provider is available for the tier.
        """
        tier = self._tier_for(system_prompt)
        candidates = self._ordered_candidates(tier)
        if not candidates:
            raise RuntimeError(f"no LLM provider available for tier {tier!r}")

        last_exception: Exception | None = None
        for provider, key in candidates:
            if not self._within_spend_cap(provider, key, prompt):
                _logger.debug("Routing: skipping %s — estimated input cost exceeds cap", provider)
                continue
            client = self._clients[key]
            try:
                response = client.generate(prompt, system_prompt)
                # Surface the winning provider's usage so agents can record
                # per-turn token counts (Phase 10.2).
                self.last_tokens_used = client.last_tokens_used
                self._record_success(provider, key, prompt, response)
                return response
            except Exception as exc:  # failover to the next provider
                self._record_failure(provider, exc)
                last_exception = exc

        if last_exception is not None:
            raise last_exception
        raise RuntimeError(
            f"no LLM provider could handle the request for tier {tier!r} "
            "(all candidates were skipped by the spend cap)"
        )  # pragma: no cover

    async def agenerate(self, prompt: str, system_prompt: str = "") -> str:
        """Async routing — same cheapest-healthy-first order, awaited calls.

        Round-3 review P1: the old ``generate`` blocked on every provider's
        HTTP call. This awaits each candidate's ``agenerate`` instead, so the
        router participates in the parallel specialist run instead of pinning
        the event loop. Failover, spend-cap skipping, and health tracking are
        identical to the sync path.

        Raises:
            The last provider exception when every candidate fails, or
            ``RuntimeError`` when no provider is available for the tier.
        """
        tier = self._tier_for(system_prompt)
        candidates = self._ordered_candidates(tier)
        if not candidates:
            raise RuntimeError(f"no LLM provider available for tier {tier!r}")

        last_exception: Exception | None = None
        for provider, key in candidates:
            if not self._within_spend_cap(provider, key, prompt):
                _logger.debug("Routing: skipping %s — estimated input cost exceeds cap", provider)
                continue
            client = self._clients[key]
            try:
                response = await client.agenerate(prompt, system_prompt)
                # Surface the winning provider's usage so agents can record
                # per-turn token counts (Phase 10.2).
                self.last_tokens_used = client.last_tokens_used
                self._record_success(provider, key, prompt, response)
                return response
            except Exception as exc:  # failover to the next provider
                self._record_failure(provider, exc)
                last_exception = exc

        if last_exception is not None:
            raise last_exception
        raise RuntimeError(
            f"no LLM provider could handle the request for tier {tier!r} "
            "(all candidates were skipped by the spend cap)"
        )  # pragma: no cover

    # ── Routing internals ──────────────────────────────────────────────

    def _tier_for(self, system_prompt: str) -> str:
        """Pick the quality tier from the agent's system prompt role."""
        agent = _detect_agent_type("", system_prompt)
        return TIER_SMART if agent in _SMART_AGENTS else TIER_FAST

    def _ordered_candidates(self, tier: str) -> list[tuple[str, tuple[str, str]]]:
        """Candidates for ``tier`` ordered by (health, role, price)."""
        keys = [k for k in self._clients if k[1] == tier]

        def sort_key(key: tuple[str, str]) -> tuple[int, int, float]:
            provider = key[0]
            unhealthy = (
                1
                if self._stats[provider].consecutive_failures >= self._DEMOTE_AFTER_FAILURES
                else 0
            )
            rank = self._MOCK_RANK if provider == "mock" else 0
            price_in, _ = model_pricing(self._models.get(key, ""))
            return (unhealthy, rank, price_in)

        return [(k[0], k) for k in sorted(keys, key=sort_key)]

    def _within_spend_cap(self, provider: str, key: tuple[str, str], prompt: str) -> bool:
        """True when the estimated input cost fits the configured spend cap."""
        cap = self._settings.routing_max_cost_per_request
        price_in, _ = model_pricing(self._models.get(key, ""))
        estimated = (estimate_tokens(prompt) / 1_000_000) * price_in
        return estimated <= cap

    def _record_success(
        self, provider: str, key: tuple[str, str], prompt: str, response: str
    ) -> None:
        """Track a successful call and its estimated spend."""
        model = self._models.get(key, "")
        with self._lock:
            stats = self._stats[provider]
            stats.calls += 1
            stats.consecutive_failures = 0
            stats.spend_usd += estimate_cost(
                estimate_tokens(prompt), estimate_tokens(response), model
            )

    def _record_failure(self, provider: str, exc: Exception) -> None:
        """Track a failed call and log the provider's health."""
        with self._lock:
            stats = self._stats[provider]
            stats.failures += 1
            stats.consecutive_failures += 1
        _logger.warning(
            "Routing: provider %s failed (%d consecutive): %s",
            provider,
            stats.consecutive_failures,
            exc,
        )

    # ── Introspection ──────────────────────────────────────────────────

    def stats(self) -> dict[str, dict[str, int | float]]:
        """Per-provider routing statistics (calls, failures, spend)."""
        with self._lock:
            snapshot = {p: asdict(s) for p, s in self._stats.items()}
        return snapshot

    def chosen_providers(self) -> list[str]:
        """Provider names currently wired into the router (per tier, may repeat)."""
        return [p for p, _ in self._clients]


def create_routed_client(settings: Settings) -> CostAwareRouter:
    """Build a :class:`CostAwareRouter` from settings.

    Constructs smart/fast clients for every enabled provider that has
    credentials. If no real provider is configured, the router falls back to
    :class:`MockClient` so development and demos keep working.
    """
    clients: dict[tuple[str, str], BaseLLMClient] = {}
    models: dict[tuple[str, str], str] = {}
    has_real = False

    def add(provider: str, tier: str, client: BaseLLMClient, model: str) -> None:
        nonlocal has_real
        clients[(provider, tier)] = client
        models[(provider, tier)] = model
        if provider != "mock":
            has_real = True

    for provider in settings.routing_providers:
        if provider == "mock":
            add("mock", TIER_SMART, MockClient(), "mock")
            add("mock", TIER_FAST, MockClient(), "mock")
        elif provider == "nvidia":
            try:
                add(
                    "nvidia",
                    TIER_SMART,
                    NvidiaClient(
                        settings,
                        model=settings.llm_nvidia_model,
                        timeout=settings.routing_timeout,
                    ),
                    settings.llm_nvidia_model,
                )
                add(
                    "nvidia",
                    TIER_FAST,
                    NvidiaClient(
                        settings,
                        model=settings.llm_nvidia_fast_model,
                        timeout=settings.routing_timeout,
                    ),
                    settings.llm_nvidia_fast_model,
                )
            except (ValueError, TypeError) as exc:
                _logger.info("Routing: Nvidia NIM unavailable — %s", exc)
        elif provider == "azure":
            try:
                add(
                    "azure",
                    TIER_SMART,
                    AzureClient(
                        settings,
                        model=settings.llm_azure_model,
                        timeout=settings.routing_timeout,
                    ),
                    settings.llm_azure_model,
                )
                add(
                    "azure",
                    TIER_FAST,
                    AzureClient(
                        settings,
                        model=settings.llm_azure_fast_model,
                        timeout=settings.routing_timeout,
                    ),
                    settings.llm_azure_fast_model,
                )
            except (ValueError, TypeError) as exc:
                _logger.info("Routing: Azure OpenAI unavailable — %s", exc)
        elif provider == "openai":  # Phase 7.6
            try:
                add(
                    "openai",
                    TIER_SMART,
                    OpenAIClient(
                        settings,
                        model=settings.llm_openai_model,
                        timeout=settings.routing_timeout,
                    ),
                    settings.llm_openai_model,
                )
                add(
                    "openai",
                    TIER_FAST,
                    OpenAIClient(
                        settings,
                        model=settings.llm_openai_fast_model,
                        timeout=settings.routing_timeout,
                    ),
                    settings.llm_openai_fast_model,
                )
            except (ValueError, TypeError) as exc:
                _logger.info("Routing: OpenAI unavailable — %s", exc)
        elif provider == "anthropic":  # Phase 7.6
            try:
                add(
                    "anthropic",
                    TIER_SMART,
                    AnthropicClient(
                        settings,
                        model=settings.llm_anthropic_model,
                        timeout=settings.routing_timeout,
                    ),
                    settings.llm_anthropic_model,
                )
                add(
                    "anthropic",
                    TIER_FAST,
                    AnthropicClient(
                        settings,
                        model=settings.llm_anthropic_fast_model,
                        timeout=settings.routing_timeout,
                    ),
                    settings.llm_anthropic_fast_model,
                )
            except (ValueError, TypeError) as exc:
                _logger.info("Routing: Anthropic unavailable — %s", exc)
        elif provider == "google":  # Phase 7.6
            try:
                add(
                    "google",
                    TIER_SMART,
                    GoogleClient(
                        settings,
                        model=settings.llm_google_model,
                        timeout=settings.routing_timeout,
                    ),
                    settings.llm_google_model,
                )
                add(
                    "google",
                    TIER_FAST,
                    GoogleClient(
                        settings,
                        model=settings.llm_google_fast_model,
                        timeout=settings.routing_timeout,
                    ),
                    settings.llm_google_fast_model,
                )
            except (ValueError, TypeError) as exc:
                _logger.info("Routing: Google Gemini unavailable — %s", exc)
        else:  # pragma: no cover - guarded by Settings validation
            _logger.warning("Routing: unknown provider %r ignored", provider)

    # Safety net: no real credentials -> fall back to mock so the app never
    # crashes on missing keys.
    if not has_real:
        clients.setdefault(("mock", TIER_SMART), MockClient())
        clients.setdefault(("mock", TIER_FAST), MockClient())
        models.setdefault(("mock", TIER_SMART), "mock")
        models.setdefault(("mock", TIER_FAST), "mock")
        _logger.warning("Routing: no real provider configured — using MockClient")

    return CostAwareRouter(settings=settings, clients=clients, models=models)
