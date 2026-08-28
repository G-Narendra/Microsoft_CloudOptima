"""Tests for the cost-aware LLM router (Phase 7.5)."""

from __future__ import annotations

import json
from collections.abc import AsyncGenerator
from typing import Any, cast
from unittest.mock import MagicMock

import pytest
from pydantic import SecretStr

from cloudoptima.config import Settings
from cloudoptima.llm_client import BaseLLMClient
from cloudoptima.llm_routing import (
    TIER_FAST,
    TIER_SMART,
    CostAwareRouter,
    create_routed_client,
    estimate_cost,
    estimate_tokens,
    model_pricing,
)

# Fakes & helpers

_OPENAI_MODEL = "gpt-4o"
_OPENAI_FAST_MODEL = "gpt-4o-mini"
_AZURE_MODEL = "gpt-4o-mini"

_OPENAI_SMART = ("openai", TIER_SMART)
_OPENAI_FAST = ("openai", TIER_FAST)
_AZURE_SMART = ("azure", TIER_SMART)
_AZURE_FAST = ("azure", TIER_FAST)
_MOCK_SMART = ("mock", TIER_SMART)
_MOCK_FAST = ("mock", TIER_FAST)

_ARCHITECT_PROMPT = "You are a senior cloud architect with deep Azure expertise."
_JUDGE_PROMPT = "You are an impartial judge overseeing a panel of four cloud expert agents."
_COST_PROMPT = "You are a cloud cost analyst specializing in Azure FinOps."


class _FakeClient(BaseLLMClient):
    """Recording fake client; optionally fails every call."""

    def __init__(self, name: str, fail: bool = False) -> None:
        self.name = name
        self.fail = fail
        self.calls: list[str] = []

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        self.calls.append(system_prompt)
        if self.fail:
            raise ConnectionError(f"{self.name} unavailable")
        return json.dumps({"provider": self.name})


def _build_router(
    clients: dict[tuple[str, str], BaseLLMClient],
    models: dict[tuple[str, str], str],
    max_cost: float = 0.005,
) -> CostAwareRouter:
    settings = Settings(routing_enabled=True, routing_max_cost_per_request=max_cost)
    return CostAwareRouter(settings, clients, models)


def _openai_smart_models() -> dict[tuple[str, str], str]:
    return {_OPENAI_SMART: _OPENAI_MODEL, _AZURE_SMART: _AZURE_MODEL}


# Pricing tests

class TestPricing:
    def test_known_model_pricing(self) -> None:
        assert model_pricing("gpt-4o-mini") == (0.15, 0.60)
        assert model_pricing(_OPENAI_MODEL) == (2.50, 10.00)
        assert model_pricing("mock") == (0.0, 0.0)

    def test_unknown_model_gets_conservative_price(self) -> None:
        assert model_pricing("brand-new-model") == (1.0, 1.0)

    def test_estimate_cost(self) -> None:
        assert estimate_cost(1_000_000, 0, "gpt-4o-mini") == pytest.approx(0.15)
        assert estimate_cost(0, 1_000_000, "gpt-4o-mini") == pytest.approx(0.60)
        assert estimate_cost(1_000_000, 1_000_000, "mock") == 0.0

    def test_estimate_tokens(self) -> None:
        assert estimate_tokens("a" * 40) == 10
        assert estimate_tokens("") == 1


# Routing behavior tests

class TestRouting:
    def test_cheapest_provider_tried_first(self) -> None:
        openai = _FakeClient("openai")
        azure = _FakeClient("azure")
        router = _build_router(
            {_OPENAI_SMART: openai, _AZURE_SMART: azure},
            _openai_smart_models(),
        )
        result = ''.join(router.generate("design a system", _ARCHITECT_PROMPT))
        assert json.loads(result)["provider"] == "azure"
        assert azure.calls and not openai.calls

    def test_failover_to_next_cheapest(self) -> None:
        azure = _FakeClient("azure", fail=True)
        openai = _FakeClient("openai")
        router = _build_router(
            {_OPENAI_SMART: openai, _AZURE_SMART: azure},
            _openai_smart_models(),
        )
        result = ''.join(router.generate("design a system", _ARCHITECT_PROMPT))
        assert json.loads(result)["provider"] == "openai"
        assert openai.calls

    def test_all_providers_fail_raises_last_error(self) -> None:
        openai = _FakeClient("openai", fail=True)
        azure = _FakeClient("azure", fail=True)
        router = _build_router(
            {_OPENAI_SMART: openai, _AZURE_SMART: azure},
            _openai_smart_models(),
        )
        with pytest.raises(ConnectionError):
            ''.join(router.generate("design a system", _ARCHITECT_PROMPT))
        assert openai.calls and azure.calls

    def test_health_demotion_after_repeated_failures(self) -> None:
        azure = _FakeClient("azure", fail=True)
        openai = _FakeClient("openai")
        router = _build_router(
            {_OPENAI_SMART: openai, _AZURE_SMART: azure},
            _openai_smart_models(),
        )
        for _ in range(3):
            ''.join(router.generate("design a system", _ARCHITECT_PROMPT))
        # Azure failed twice consecutively -> demoted on the third call.
        assert len(azure.calls) == 2
        assert len(openai.calls) == 3

    def test_tier_selection_by_agent_role(self) -> None:
        smart = _FakeClient("openai-smart")
        fast = _FakeClient("openai-fast")
        router = _build_router(
            {_OPENAI_SMART: smart, _OPENAI_FAST: fast},
            {_OPENAI_SMART: _OPENAI_MODEL, _OPENAI_FAST: _OPENAI_FAST_MODEL},
        )
        ''.join(router.generate("arbitrate", _JUDGE_PROMPT))
        ''.join(router.generate("estimate", _COST_PROMPT))
        assert len(smart.calls) == 1
        assert len(fast.calls) == 1

    def test_spend_guard_skips_expensive_provider(self) -> None:
        azure = _FakeClient("azure")
        mock = _FakeClient("mock")
        router = _build_router(
            {_AZURE_SMART: azure, _MOCK_SMART: mock},
            {_AZURE_SMART: _AZURE_MODEL, _MOCK_SMART: "mock"},
            max_cost=0.00001,  # below any paid input cost, above the free $0
        )
        ''.join(router.generate("z" * 500, _ARCHITECT_PROMPT))
        assert azure.calls == []
        assert mock.calls

    def test_spend_guard_skips_all_providers(self) -> None:
        azure = _FakeClient("azure")
        router = _build_router(
            {_AZURE_SMART: azure},
            {_AZURE_SMART: _AZURE_MODEL},
            max_cost=0.00001,  # below any paid input cost
        )
        with pytest.raises(Exception) as exc_info:
            ''.join(router.generate("z" * 500, _ARCHITECT_PROMPT))
        assert azure.calls == []
        assert "all candidates were skipped" in str(exc_info.value)

@pytest.mark.asyncio
async def test_routed_agenerate():
    """Test the async generation path (agenerate)."""
    settings = Settings(llm_provider="mock", routing_enabled=True)
    router = create_routed_client(settings)
    class SucceedingAsyncClient:
        def __init__(self):
            self.last_tokens_used = 10
        async def agenerate(self, p, s):
            yield "async"
            yield "_"
            yield "chunk"
            
    router._clients[("mock", "fast")] = SucceedingAsyncClient()
    
    chunks = []
    async for chunk in router.agenerate("test", "sys"):
        chunks.append(chunk)
        
    assert chunks == ["async", "_", "chunk"]

@pytest.mark.asyncio
async def test_routed_agenerate_failover():
    """Test the async failover path."""
    settings = Settings(llm_provider="mock", routing_enabled=True)
    router = create_routed_client(settings)
    
    class FailingAsyncClient:
        def __init__(self):
            self.last_tokens_used = 0
        async def agenerate(self, p, s):
            raise ValueError("async fail")
            yield "never"
            
    class SucceedingAsyncClient:
        def __init__(self):
            self.last_tokens_used = 10
        async def agenerate(self, p, s):
            yield "success"
            
    router._clients = {
        ("prov1", "smart"): FailingAsyncClient(),
        ("prov2", "smart"): SucceedingAsyncClient()
    }
    
    chunks = []
    async for chunk in router.agenerate("test", "You are an architect"):
        chunks.append(chunk)
        
    assert chunks == ["success"]
    assert router.last_tokens_used == 10

@pytest.mark.asyncio
async def test_routed_agenerate_all_fail():
    """Test agenerate when all providers fail."""
    settings = Settings(llm_provider="mock", routing_enabled=True)
    router = create_routed_client(settings)
    
    class FailingAsyncClient:
        def __init__(self):
            self.last_tokens_used = 0
        async def agenerate(self, p, s):
            raise ValueError("async fail")
            yield "never"
            
    router._clients = {
        ("prov1", "smart"): FailingAsyncClient(),
    }
    
    with pytest.raises(ValueError, match="async fail"):
        async for _ in router.agenerate("test", "You are an architect"):
            pass

    def test_spend_tracking(self) -> None:
        azure = _FakeClient("azure")
        router = _build_router(
            {_AZURE_SMART: azure},
            {_AZURE_SMART: _AZURE_MODEL},
        )
        ''.join(router.generate("hello world", _ARCHITECT_PROMPT))
        stats = router.stats()
        assert stats["azure"]["calls"] == 1
        assert stats["azure"]["spend_usd"] > 0
        assert stats["azure"]["consecutive_failures"] == 0


# Factory tests

class TestCreateRoutedClient:
    def test_mock_fallback_when_no_real_credentials(self) -> None:
        settings = Settings(
            routing_enabled=True,
            routing_providers=["openai", "azure"],
            # Explicitly clear credentials so this test is hermetic even on
            # machines that have a populated .env (e.g. the dev machine).
            openai_api_key=SecretStr(""),
            azure_openai_api_key=SecretStr(""),
            azure_openai_endpoint="",
        )
        router = create_routed_client(settings)
        result = ''.join(router.generate("design a system", _ARCHITECT_PROMPT))
        assert json.loads(result)  # mock returns valid JSON
        assert router.stats()["mock"]["calls"] == 1

    def test_azure_client_built_when_credentials_present(self) -> None:
        settings = Settings(
            routing_enabled=True,
            routing_providers=["azure"],
            azure_openai_api_key=SecretStr("test-key"),
            azure_openai_endpoint="https://example.openai.azure.com/",
        )
        router = create_routed_client(settings)
        assert "azure" in router.chosen_providers()

    def test_unknown_routing_provider_rejected_by_settings(self) -> None:
        with pytest.raises(Exception):
            Settings(routing_enabled=True, routing_providers=["bogus"])

    def test_comma_separated_providers_string_parsed(self) -> None:
        settings = Settings(
            routing_enabled=True,
            # cast: the comma string exercises the NoDecode parsing path, which
            # the annotated list[str] type cannot express statically.
            routing_providers=cast(Any, "openai,azure,anthropic,google"),
        )
        assert settings.routing_providers == [
            "openai",
            "azure",
            "anthropic",
            "google",
        ]

    def test_all_phase76_providers_registered_when_credentials_present(self) -> None:
        settings = Settings(
            routing_enabled=True,
            routing_providers=["openai", "anthropic", "google"],
            openai_api_key=SecretStr("sk-openai"),
            anthropic_api_key=SecretStr("sk-ant"),
            google_api_key=SecretStr("AI-google"),
        )
        router = create_routed_client(settings)
        providers = set(router.chosen_providers())
        assert {"openai", "anthropic", "google"} <= providers

    def test_failover_across_four_providers(self) -> None:
        """Phase 7.6: kill the three cheapest providers, load lands on the 4th."""
        clients: dict[tuple[str, str], BaseLLMClient] = {
            ("openai", TIER_SMART): _FakeClient("openai", fail=True),
            ("google", TIER_SMART): _FakeClient("google", fail=True),
            ("azure", TIER_SMART): _FakeClient("azure", fail=True),
            ("anthropic", TIER_SMART): _FakeClient("anthropic"),
        }
        models: dict[tuple[str, str], str] = {
            ("openai", TIER_SMART): "gpt-4o-mini",
            ("azure", TIER_SMART): "gpt-4o-mini",
            ("anthropic", TIER_SMART): "claude-3-5-sonnet-20241022",
        }
        router = _build_router(clients, models)
        result = ''.join(router.generate("design a system", _ARCHITECT_PROMPT))
        assert json.loads(result)["provider"] == "anthropic"

    def test_spend_guard_with_real_prices(self) -> None:
        """Phase 7.6: a tiny cap skips every paid provider and hits free mock."""
        mock = _FakeClient("mock")
        azure = _FakeClient("azure")
        openai = _FakeClient("openai")
        clients: dict[tuple[str, str], BaseLLMClient] = {
            ("mock", TIER_SMART): mock,
            ("azure", TIER_SMART): azure,
            ("openai", TIER_SMART): openai,
        }
        models: dict[tuple[str, str], str] = {
            ("mock", TIER_SMART): "mock",
            ("azure", TIER_SMART): "gpt-4o-mini",
            ("openai", TIER_SMART): "gpt-4o-mini",
        }
        router = _build_router(
            clients,
            models,
            max_cost=0.00001,  # below any paid input cost, above the free $0
        )
        ''.join(router.generate("z" * 500, _ARCHITECT_PROMPT))
        assert azure.calls == []
        assert openai.calls == []
        assert mock.calls
