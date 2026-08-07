"""Tests for the cost-aware LLM router (Phase 7.5)."""

from __future__ import annotations

import json
from typing import Any, cast

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

# ── Fakes & helpers ─────────────────────────────────────────────────────

_NVIDIA_MODEL = "meta/llama-3.3-70b-instruct"
_NVIDIA_FAST_MODEL = "meta/llama-3.1-8b-instruct"
_AZURE_MODEL = "gpt-4o-mini"

_NVIDIA_SMART = ("nvidia", TIER_SMART)
_NVIDIA_FAST = ("nvidia", TIER_FAST)
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


def _nvidia_smart_models() -> dict[tuple[str, str], str]:
    return {_NVIDIA_SMART: _NVIDIA_MODEL, _AZURE_SMART: _AZURE_MODEL}


# ── Pricing ─────────────────────────────────────────────────────────────


class TestPricing:
    def test_known_model_pricing(self) -> None:
        assert model_pricing("gpt-4o-mini") == (0.15, 0.60)
        assert model_pricing(_NVIDIA_MODEL) == (0.0, 0.0)
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


# ── Routing behaviour ───────────────────────────────────────────────────


class TestRouting:
    def test_cheapest_provider_tried_first(self) -> None:
        nvidia = _FakeClient("nvidia")
        azure = _FakeClient("azure")
        router = _build_router(
            {_NVIDIA_SMART: nvidia, _AZURE_SMART: azure},
            _nvidia_smart_models(),
        )
        result = router.generate("design a system", _ARCHITECT_PROMPT)
        assert json.loads(result)["provider"] == "nvidia"
        assert nvidia.calls and not azure.calls

    def test_failover_to_next_cheapest(self) -> None:
        nvidia = _FakeClient("nvidia", fail=True)
        azure = _FakeClient("azure")
        router = _build_router(
            {_NVIDIA_SMART: nvidia, _AZURE_SMART: azure},
            _nvidia_smart_models(),
        )
        result = router.generate("design a system", _ARCHITECT_PROMPT)
        assert json.loads(result)["provider"] == "azure"
        assert azure.calls

    def test_all_providers_fail_raises_last_error(self) -> None:
        nvidia = _FakeClient("nvidia", fail=True)
        azure = _FakeClient("azure", fail=True)
        router = _build_router(
            {_NVIDIA_SMART: nvidia, _AZURE_SMART: azure},
            _nvidia_smart_models(),
        )
        with pytest.raises(ConnectionError):
            router.generate("design a system", _ARCHITECT_PROMPT)
        assert nvidia.calls and azure.calls

    def test_health_demotion_after_repeated_failures(self) -> None:
        nvidia = _FakeClient("nvidia", fail=True)
        azure = _FakeClient("azure")
        router = _build_router(
            {_NVIDIA_SMART: nvidia, _AZURE_SMART: azure},
            _nvidia_smart_models(),
        )
        for _ in range(3):
            router.generate("design a system", _ARCHITECT_PROMPT)
        # Nvidia failed twice consecutively -> demoted on the third call.
        assert len(nvidia.calls) == 2
        assert len(azure.calls) == 3

    def test_tier_selection_by_agent_role(self) -> None:
        smart = _FakeClient("nvidia-smart")
        fast = _FakeClient("nvidia-fast")
        router = _build_router(
            {_NVIDIA_SMART: smart, _NVIDIA_FAST: fast},
            {_NVIDIA_SMART: _NVIDIA_MODEL, _NVIDIA_FAST: _NVIDIA_FAST_MODEL},
        )
        router.generate("arbitrate", _JUDGE_PROMPT)
        router.generate("estimate", _COST_PROMPT)
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
        router.generate("z" * 500, _ARCHITECT_PROMPT)
        assert azure.calls == []
        assert mock.calls

    def test_spend_tracking(self) -> None:
        azure = _FakeClient("azure")
        router = _build_router(
            {_AZURE_SMART: azure},
            {_AZURE_SMART: _AZURE_MODEL},
        )
        router.generate("hello world", _ARCHITECT_PROMPT)
        stats = router.stats()
        assert stats["azure"]["calls"] == 1
        assert stats["azure"]["spend_usd"] > 0
        assert stats["azure"]["consecutive_failures"] == 0


# ── Factory ─────────────────────────────────────────────────────────────


class TestCreateRoutedClient:
    def test_mock_fallback_when_no_real_credentials(self) -> None:
        settings = Settings(
            routing_enabled=True,
            routing_providers=["nvidia", "azure"],
            # Explicitly clear credentials so this test is hermetic even on
            # machines that have a populated .env (e.g. the dev machine).
            nvidia_api_key=SecretStr(""),
            azure_openai_api_key=SecretStr(""),
            azure_openai_endpoint="",
        )
        router = create_routed_client(settings)
        result = router.generate("design a system", _ARCHITECT_PROMPT)
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
            routing_providers=cast(Any, "openai,azure,anthropic,google,nvidia"),
        )
        assert settings.routing_providers == [
            "openai",
            "azure",
            "anthropic",
            "google",
            "nvidia",
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
            ("nvidia", TIER_SMART): _FakeClient("nvidia", fail=True),
            ("openai", TIER_SMART): _FakeClient("openai", fail=True),
            ("azure", TIER_SMART): _FakeClient("azure", fail=True),
            ("anthropic", TIER_SMART): _FakeClient("anthropic"),
        }
        models: dict[tuple[str, str], str] = {
            ("nvidia", TIER_SMART): "meta/llama-3.3-70b-instruct",
            ("openai", TIER_SMART): "gpt-4o-mini",
            ("azure", TIER_SMART): "gpt-4o-mini",
            ("anthropic", TIER_SMART): "claude-sonnet-4-20250514",
        }
        router = _build_router(clients, models)
        result = router.generate("design a system", _ARCHITECT_PROMPT)
        assert json.loads(result)["provider"] == "anthropic"

    def test_spend_guard_with_real_prices(self) -> None:
        """Phase 7.6: a tiny cap skips every paid provider and hits free Nvidia."""
        nvidia = _FakeClient("nvidia")
        azure = _FakeClient("azure")
        openai = _FakeClient("openai")
        clients: dict[tuple[str, str], BaseLLMClient] = {
            ("nvidia", TIER_SMART): nvidia,
            ("azure", TIER_SMART): azure,
            ("openai", TIER_SMART): openai,
        }
        models: dict[tuple[str, str], str] = {
            ("nvidia", TIER_SMART): "meta/llama-3.3-70b-instruct",
            ("azure", TIER_SMART): "gpt-4o-mini",
            ("openai", TIER_SMART): "gpt-4o-mini",
        }
        router = _build_router(
            clients,
            models,
            max_cost=0.00001,  # below any paid input cost, above the free $0
        )
        router.generate("z" * 500, _ARCHITECT_PROMPT)
        assert azure.calls == []
        assert openai.calls == []
        assert nvidia.calls
