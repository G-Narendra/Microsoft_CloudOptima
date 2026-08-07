"""Tests for the pricing module — static catalog (8.3) and live API (8.4)."""

from __future__ import annotations

from typing import Any, cast
from unittest.mock import MagicMock, patch

import httpx
import pytest

from cloudoptima.pricing import (
    STATIC_PRICES,
    azure_api,
    clear_cache,
    estimate,
    estimate_live,
    extract_services,
    get_price,
    get_price_with_unit,
    live_prices,
    lookup,
    render_price_block,
)
from cloudoptima.pricing.azure_api import RETAIL_API_BASE, _cache, _cache_lock

# ── Static catalog (Phase 8.3) ──────────────────────────────────────────


class TestStaticCatalog:
    def test_known_services_have_prices(self) -> None:
        assert lookup("AKS") == 1800.00
        assert lookup("Azure SQL Database") == 920.00
        assert lookup("Blob Storage") == 150.00
        assert STATIC_PRICES["AKS"] == 1800.00

    def test_lookup_case_insensitive(self) -> None:
        assert lookup("aks") == 1800.00
        assert lookup("  blob storage  ") == 150.00

    def test_unknown_service_returns_none(self) -> None:
        assert lookup("Quantum Mainframe") is None
        assert lookup("") is None
        assert lookup(cast(Any, None)) is None

    def test_prices_are_read_only(self) -> None:
        with pytest.raises(TypeError):
            STATIC_PRICES["AKS"] = 1.0  # type: ignore[index]

    def test_estimate_sums_known_services(self) -> None:
        result = estimate({"services": ["AKS", "Blob Storage"]})
        assert result["estimate"] == pytest.approx(1950.00)
        assert result["source"] == "static"
        assert len(result["items"]) == 2

    def test_estimate_with_quantities(self) -> None:
        result = estimate({"services": [{"service": "AKS", "quantity": 2}]})
        assert result["estimate"] == pytest.approx(3600.00)

    def test_estimate_reports_unknown_services(self) -> None:
        result = estimate({"services": ["AKS", "Hover Car DB"]})
        assert result["unknown"] == ["Hover Car DB"]
        assert result["estimate"] == pytest.approx(1800.00)

    def test_estimate_empty_and_malformed(self) -> None:
        assert estimate(None)["estimate"] == 0.0
        assert estimate({"services": "not-a-list"})["estimate"] == 0.0


# ── Live API (Phase 8.4) ────────────────────────────────────────────────


def _mock_retail_response(price: float) -> MagicMock:
    """A mock httpx response carrying one retail-price item."""
    resp = MagicMock()
    resp.json.return_value = {
        "Items": [
            {
                "serviceName": "Virtual Machines",
                "armRegionName": "uaenorth",
                "retailPrice": price,
                "meterId": "meter-1",
            }
        ],
        "NextPageLink": None,
    }
    return resp


class TestAzureApi:
    @pytest.fixture(autouse=True)
    def _clean_cache(self) -> Any:
        clear_cache()
        yield
        clear_cache()

    def test_get_price_uses_median_and_skips_spot_meters(self) -> None:
        """Spot/reservation meters are excluded; the median PAYG price wins."""
        with patch("cloudoptima.pricing.azure_api.httpx.Client") as mock_cls:
            mock_http = MagicMock()
            mock_cls.return_value.__enter__ = MagicMock(return_value=mock_http)
            mock_cls.return_value.__exit__ = MagicMock(return_value=False)
            resp = MagicMock()
            resp.json.return_value = {
                "Items": [
                    {
                        "serviceName": "Virtual Machines",
                        "meterName": "D2 v3 Spot",
                        "retailPrice": 6.0,
                    },
                    {
                        "serviceName": "Virtual Machines",
                        "meterName": "D2 v3",
                        "retailPrice": 72.14,
                    },
                    {
                        "serviceName": "Virtual Machines",
                        "meterName": "D4 v3",
                        "retailPrice": 144.28,
                    },
                    {
                        "serviceName": "Virtual Machines",
                        "meterName": "D8 v3",
                        "retailPrice": 288.56,
                    },
                ],
                "NextPageLink": None,
            }
            mock_http.get.return_value = resp

            price = get_price("Virtual Machines", "uaenorth")

        # Median of the three pay-as-you-go meters, not the spot SKU's 6.0.
        assert price == pytest.approx(144.28)

    def test_get_price_falls_back_to_all_meters_when_all_excluded(self) -> None:
        """If every meter is spot, use them rather than returning nothing."""
        with patch("cloudoptima.pricing.azure_api.httpx.Client") as mock_cls:
            mock_http = MagicMock()
            mock_cls.return_value.__enter__ = MagicMock(return_value=mock_http)
            mock_cls.return_value.__exit__ = MagicMock(return_value=False)
            resp = MagicMock()
            resp.json.return_value = {
                "Items": [
                    {
                        "serviceName": "Virtual Machines",
                        "meterName": "D2 v3 Spot",
                        "retailPrice": 6.0,
                    },
                    {
                        "serviceName": "Virtual Machines",
                        "meterName": "D4 v3 Spot",
                        "retailPrice": 12.0,
                    },
                ],
                "NextPageLink": None,
            }
            mock_http.get.return_value = resp

            price = get_price("Virtual Machines", "uaenorth")

        assert price == pytest.approx(9.0)  # median of all spot meters

    def test_get_price_with_unit_median_of_dominant_unit_group(self) -> None:
        """Prices group by unit; the most common unit's median wins."""
        with patch("cloudoptima.pricing.azure_api.httpx.Client") as mock_cls:
            mock_http = MagicMock()
            mock_cls.return_value.__enter__ = MagicMock(return_value=mock_http)
            mock_cls.return_value.__exit__ = MagicMock(return_value=False)
            resp = MagicMock()
            resp.json.return_value = {
                "Items": [
                    {
                        "serviceName": "Azure Kubernetes Service",
                        "meterName": "Standard vCPU",
                        "retailPrice": 0.02,
                        "unitOfMeasure": "1 Hour",
                    },
                    {
                        "serviceName": "Azure Kubernetes Service",
                        "meterName": "Standard vCPU",
                        "retailPrice": 0.04,
                        "unitOfMeasure": "1 Hour",
                    },
                    {
                        "serviceName": "Azure Kubernetes Service",
                        "meterName": "Monthly pricing",
                        "retailPrice": 100.0,
                        "unitOfMeasure": "1 Month",
                    },
                ],
                "NextPageLink": None,
            }
            mock_http.get.return_value = resp

            result = get_price_with_unit("Azure Kubernetes Service", "uaenorth")

        # Median of the two per-hour meters, with the hourly unit attached.
        assert result == (0.03, "1 Hour")
        assert get_price("Azure Kubernetes Service", "uaenorth") == pytest.approx(0.03)

    def test_get_price_returns_retail_price(self) -> None:
        with patch("cloudoptima.pricing.azure_api.httpx.Client") as mock_cls:
            mock_http = MagicMock()
            mock_cls.return_value.__enter__ = MagicMock(return_value=mock_http)
            mock_cls.return_value.__exit__ = MagicMock(return_value=False)
            mock_http.get.return_value = _mock_retail_response(72.14)

            price = get_price("Virtual Machines", "uaenorth")

        assert price == pytest.approx(72.14)
        # The request went to the documented no-auth endpoint.
        called_url = mock_http.get.call_args[0][0]
        assert RETAIL_API_BASE in called_url

    def test_get_price_caches_for_one_hour(self) -> None:
        with patch("cloudoptima.pricing.azure_api.httpx.Client") as mock_cls:
            mock_http = MagicMock()
            mock_cls.return_value.__enter__ = MagicMock(return_value=mock_http)
            mock_cls.return_value.__exit__ = MagicMock(return_value=False)
            mock_http.get.return_value = _mock_retail_response(72.14)

            first = get_price("Virtual Machines", "uaenorth")
            second = get_price("Virtual Machines", "uaenorth")

        assert first == second == pytest.approx(72.14)
        # Second call served from cache — the HTTP layer was hit exactly once.
        assert mock_http.get.call_count == 1

    def test_cache_expires_after_ttl(self) -> None:
        with patch("cloudoptima.pricing.azure_api.httpx.Client") as mock_cls:
            mock_http = MagicMock()
            mock_cls.return_value.__enter__ = MagicMock(return_value=mock_http)
            mock_cls.return_value.__exit__ = MagicMock(return_value=False)
            mock_http.get.return_value = _mock_retail_response(72.14)

            get_price("Virtual Machines", "uaenorth")
            # Simulate the TTL elapsing.
            with _cache_lock:
                key = ("virtual machines", "uaenorth")
                fetched_at, price = _cache[key]
                _cache[key] = (fetched_at - azure_api.CACHE_TTL_SECONDS - 1, price)
            get_price("Virtual Machines", "uaenorth")

        assert mock_http.get.call_count == 2

    def test_get_price_unreachable_returns_none(self) -> None:
        with patch("cloudoptima.pricing.azure_api.httpx.Client") as mock_cls:
            mock_http = MagicMock()
            mock_cls.return_value.__enter__ = MagicMock(return_value=mock_http)
            mock_cls.return_value.__exit__ = MagicMock(return_value=False)
            mock_http.get.side_effect = httpx.ConnectError("no network")

            price = get_price("Virtual Machines", "uaenorth")

        assert price is None

    def test_get_price_unknown_service_returns_none(self) -> None:
        with patch("cloudoptima.pricing.azure_api.httpx.Client") as mock_cls:
            mock_http = MagicMock()
            mock_cls.return_value.__enter__ = MagicMock(return_value=mock_http)
            mock_cls.return_value.__exit__ = MagicMock(return_value=False)
            resp = MagicMock()
            resp.json.return_value = {"Items": [], "NextPageLink": None}
            mock_http.get.return_value = resp

            price = get_price("Hover Car DB", "uaenorth")

        assert price is None

    def test_unknown_service_not_requeried_due_to_negative_cache(self) -> None:
        """A 'known unknown' (None price) is cached, so the API is not re-hit."""
        with patch("cloudoptima.pricing.azure_api.httpx.Client") as mock_cls:
            mock_http = MagicMock()
            mock_cls.return_value.__enter__ = MagicMock(return_value=mock_http)
            mock_cls.return_value.__exit__ = MagicMock(return_value=False)
            resp = MagicMock()
            resp.json.return_value = {"Items": [], "NextPageLink": None}
            mock_http.get.return_value = resp

            assert get_price("Hover Car DB", "uaenorth") is None
            assert get_price("Hover Car DB", "uaenorth") is None

        # Both calls served without re-hitting the HTTP layer.
        assert mock_http.get.call_count == 1

    def test_estimate_live_uses_api_and_reports_source(self) -> None:
        with patch.object(azure_api, "get_price", return_value=72.14) as mock_get:
            result = estimate_live({"services": ["Virtual Machines"]})

        assert result["estimate"] == pytest.approx(72.14)
        assert result["source"] == "azure_retail_api"
        mock_get.assert_called_once()

    def test_estimate_live_falls_back_to_static(self) -> None:
        with patch.object(azure_api, "get_price", return_value=None):
            result = estimate_live({"services": ["AKS", "Blob Storage"]})

        assert result["estimate"] == pytest.approx(1950.00)
        assert result["source"] == "static"
        assert all(item["source"] == "static" for item in result["items"])

    def test_estimate_live_mixed_sources(self) -> None:
        with patch.object(
            azure_api,
            "get_price",
            side_effect=lambda name, *a, **k: 72.14 if name == "Virtual Machines" else None,
        ):
            result = estimate_live({"services": ["Virtual Machines", "AKS"]})

        assert result["source"] == "static_fallback"
        sources = {item["source"] for item in result["items"]}
        assert sources == {"live", "static"}

    def test_estimate_live_unknown_reported(self) -> None:
        with patch.object(azure_api, "get_price", return_value=None):
            result = estimate_live({"services": ["Hover Car DB"]})

        assert result["unknown"] == ["Hover Car DB"]
        assert result["estimate"] == 0.0


# ── Live-pricing grounding (Phase 8.4 -> pipeline wiring) ────────────────


class TestGrounding:
    def test_extract_services_finds_aliases(self) -> None:
        names = extract_services(
            "Use AKS with Redis and Azure SQL Database for the data tier"
        )
        assert "Azure Kubernetes Service" in names
        assert "Azure Cache for Redis" in names
        assert "Azure SQL Database" in names

    def test_extract_services_longest_needle_wins(self) -> None:
        names = extract_services("azure kubernetes service (aks) cluster")
        assert names.count("Azure Kubernetes Service") == 1

    def test_extract_services_dedupes_in_first_mention_order(self) -> None:
        names = extract_services("Redis first, then AKS and redis cache again")
        assert names == ["Azure Cache for Redis", "Azure Kubernetes Service"]

    def test_extract_services_empty_and_clean(self) -> None:
        assert extract_services() == []
        assert extract_services("", None, "no azure services mentioned") == []

    def test_live_prices_uses_api_then_static_fallback(self) -> None:
        with patch("cloudoptima.pricing.grounding.get_price_with_unit") as mock_get, patch(
            "cloudoptima.pricing.grounding.lookup"
        ) as mock_lookup:
            mock_get.side_effect = lambda name, *a, **k: (
                (72.14, "1 Hour") if name == "Virtual Machines" else None
            )
            mock_lookup.side_effect = lambda name, *a, **k: (
                1800.0 if name == "AKS" else None
            )

            rows = live_prices(["Virtual Machines", "AKS"], "uaenorth")

        assert rows == [
            {
                "service": "Virtual Machines",
                "price": 72.14,
                "unit": "1 Hour",
                "source": "live",
            },
            {"service": "AKS", "price": 1800.0, "unit": "month", "source": "static"},
        ]

    def test_live_prices_queries_api_canonical_name(self) -> None:
        """AKS is canonicalized to the Retail API's serviceName for a live hit."""
        with patch("cloudoptima.pricing.grounding.get_price_with_unit") as mock_get, patch(
            "cloudoptima.pricing.grounding.lookup", return_value=None
        ):
            mock_get.return_value = (193.44, "1 Hour")

            live_prices(["AKS"], "uaenorth")

        assert mock_get.call_args[0][0] == "Azure Kubernetes Service"

    def test_live_prices_skips_unpriceable_services(self) -> None:
        with patch("cloudoptima.pricing.grounding.get_price_with_unit", return_value=None), patch(
            "cloudoptima.pricing.grounding.lookup", return_value=None
        ):
            assert live_prices(["Hover Car DB"], "uaenorth") == []

    def test_render_price_block_lists_rows_and_sources(self) -> None:
        block = render_price_block(
            [
                {"service": "AKS", "price": 0.0231, "unit": "1 Hour", "source": "live"},
                {
                    "service": "Blob Storage",
                    "price": 150.0,
                    "unit": "month",
                    "source": "static",
                },
            ],
            "uaenorth",
        )
        assert "Azure Retail" in block
        assert "AKS: $0.02 per 1 Hour [azure_retail_api]" in block
        assert "Blob Storage: $150.00 per month [static_catalog]" in block

    def test_render_price_block_empty_is_factual(self) -> None:
        block = render_price_block([], "uaenorth")
        assert "no Azure services matched" in block
