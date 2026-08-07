"""Shared test fixtures for the CloudOptima test suite."""

from __future__ import annotations

import pytest


@pytest.fixture(autouse=True)
def _no_live_pricing_network(monkeypatch: pytest.MonkeyPatch) -> None:
    """Keep agent tests hermetic: never call the Azure Retail Prices API.

    The cost analyst grounds its prompt with live prices (Phase 8.4 wiring),
    which would otherwise open a real HTTP connection on every prompt build
    in the test suite. This patches the fetch to return no rows so no test
    depends on the network; pricing tests that exercise the real functions
    patch ``get_price``/``lookup`` themselves.
    """

    def _no_prices(service_names: list[str], region: str) -> list[dict[str, object]]:
        del service_names, region
        return []

    import cloudoptima.agents.cost_analyst as cost_analyst

    monkeypatch.setattr(cost_analyst, "live_prices", _no_prices)
