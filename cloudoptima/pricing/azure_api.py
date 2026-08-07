"""Live Azure Retail Prices API lookups (Phase 8.4).

The Azure Retail Prices API (``https://prices.azure.com/api/retail/prices``)
is free, needs no auth, and returns pay-as-you-go prices per region. This
module wraps it with:

- **1-hour caching** — the API is hit at most once per hour per
  ``(service, region)`` key.
- **Graceful degradation** — a network failure or unknown service yields
  ``None``, and :func:`estimate_live` falls back to the static catalog
  (:mod:`cloudoptima.pricing.static_db`), so a flaky network never breaks
  the pipeline.

No API keys are used or logged; requests carry no credentials.
"""

from __future__ import annotations

import logging
import statistics
import threading
import time
from typing import Any, Final

import httpx

from cloudoptima.pricing.static_db import lookup

_logger = logging.getLogger(__name__)

#: Azure Retail Prices API endpoint (free, no auth).
RETAIL_API_BASE: Final[str] = "https://prices.azure.com/api/retail/prices"

#: Cache TTL — the checklist requires results cached for 1 hour.
CACHE_TTL_SECONDS: Final[float] = 3600.0

#: Default HTTP timeout for the free API (fail fast, no auth needed).
_TIMEOUT_SECONDS: Final[float] = 10.0

#: How many API pages to follow before giving up on a search. The default
#: page size is 100 items; big services (Storage, Virtual Machines) need a
#: few pages before the median stabilises.
_MAX_PAGES: Final[int] = 10

# Meters to skip when choosing a representative price. The Retail API returns
# every meter for a service/region — spot VMs, reservations, etc. — and the
# cheapest of those would be a misleading "price" to show a user. A plain
# pay-as-you-go meter is a much better default.
_EXCLUDED_METER_MARKERS: Final[tuple[str, ...]] = (
    "spot",
    "low priority",
    "reservation",
    "savings plan",
    "azure hybrid benefit",
)

# Cache: key -> (fetched_at, (price, unit) | None). A ``None`` value means
# "known unknown" (queried, not found / unreachable) and is cached so callers
# do not hammer the API on every request for an unknown service.
_cache: dict[tuple[str, str], tuple[float, tuple[float, str] | None]] = {}
_cache_lock = threading.Lock()

#: Sentinel returned by :func:`_cache_get` for a genuine miss, so a cached
#: ``None`` result is distinguishable from "not yet cached".
_MISS: Final[object] = object()


def clear_cache() -> None:
    """Clear the in-memory price cache (used between tests)."""
    with _cache_lock:
        _cache.clear()


def _cache_get(key: tuple[str, str]) -> tuple[float, str] | None | object:
    """Return the cached ``(price, unit)`` for ``key``, or ``_MISS``."""
    with _cache_lock:
        entry = _cache.get(key)
    if entry is None:
        return _MISS
    fetched_at, value = entry
    if time.monotonic() - fetched_at > CACHE_TTL_SECONDS:
        return _MISS
    return value


def _cache_put(key: tuple[str, str], value: tuple[float, str] | None) -> None:
    """Store a result for ``key`` (even ``None`` — avoids hammering unknowns)."""
    with _cache_lock:
        _cache[key] = (time.monotonic(), value)


def get_price_with_unit(
    service: str,
    region: str = "uaenorth",
    meter_id: str | None = None,
    timeout: float = _TIMEOUT_SECONDS,
) -> tuple[float, str] | None:
    """Live USD retail price and its unit for ``service`` in ``region``.

    The unit matters: the Retail API prices per meter, so one service is per
    hour ("1 Hour"), another per gigabyte-month ("1 GB-Mo"). Showing a price
    without its unit would silently mislead.

    Args:
        service: Azure service name, e.g. ``"Virtual Machines"`` or
            ``"Azure SQL Database"``.
        region: ARM region name, e.g. ``"uaenorth"``, ``"eastus"``.
        meter_id: Optional specific meter to match; when omitted a
            representative meter is chosen.
        timeout: HTTP timeout in seconds.

    Returns:
        ``(price, unit)`` where ``price`` is the median of the dominant unit
        group's pay-as-you-go meters, or ``None`` when the service is unknown
        in the region, the API is unreachable, or the request fails. Never
        raises — failures are logged and degrade to ``None`` so callers fall
        back to the static catalog.

    Results are cached for 1 hour per ``(service, region)`` key — including
    "known unknown" results, so an unknown service is not re-queried on every
    call.
    """
    if not isinstance(service, str) or not service.strip():
        return None
    key = (service.strip().casefold(), (region or "uaenorth").casefold())

    cached = _cache_get(key)
    if cached is not _MISS:
        return cached  # type: ignore[return-value]

    result = _fetch_price(service.strip(), region or "uaenorth", meter_id, timeout)
    _cache_put(key, result)
    return result


def get_price(
    service: str,
    region: str = "uaenorth",
    meter_id: str | None = None,
    timeout: float = _TIMEOUT_SECONDS,
) -> float | None:
    """Live USD retail price for ``service`` in ``region`` (unit omitted).

    Thin wrapper over :func:`get_price_with_unit` for callers that only need
    the number (e.g. :func:`estimate_live`). See that function for semantics.
    """
    result = get_price_with_unit(service, region, meter_id, timeout)
    return result[0] if result is not None else None


def _fetch_price(
    service: str, region: str, meter_id: str | None, timeout: float
) -> tuple[float, str] | None:
    """Query the Retail Prices API for ``service``/``region`` (uncached).

    Returns the median price within the dominant unit group, or ``None`` on
    failure. The query deliberately omits ``$top``: the API's ``NextPageLink``
    is corrupt when ``$top`` is set (it emits ``$top=-900`` on later pages,
    which 400s), so pagination is driven by the link as returned.
    """
    # serviceName filter values use the API's canonical casing; a plain
    # equality filter is the documented, no-auth way to search.
    filter_expr = (
        f"serviceName eq '{_escape_odata(service)}'"
        f" and armRegionName eq '{_escape_odata(region)}'"
    )
    url = f"{RETAIL_API_BASE}?$filter={filter_expr}"
    preferred: list[tuple[float, str]] = []
    all_prices: list[tuple[float, str]] = []

    try:
        with httpx.Client(timeout=timeout) as client:
            for _ in range(_MAX_PAGES):
                response = client.get(url)
                response.raise_for_status()
                data = response.json()
                for item in data.get("Items", []):
                    if not isinstance(item, dict):
                        continue
                    if meter_id and item.get("meterId") != meter_id:
                        continue
                    price = item.get("retailPrice")
                    if not isinstance(price, (int, float)) or isinstance(price, bool):
                        continue
                    unit = str(item.get("unitOfMeasure") or "unit")
                    entry = (float(price), unit)
                    all_prices.append(entry)
                    meter_name = str(item.get("meterName", "")).casefold()
                    if any(marker in meter_name for marker in _EXCLUDED_METER_MARKERS):
                        continue
                    preferred.append(entry)
                next_link = data.get("NextPageLink")
                if not next_link:
                    break
                url = next_link
    except (httpx.HTTPError, ValueError, OSError) as exc:
        _logger.warning(
            "Azure Retail Prices API unreachable for %r/%r: %s", service, region, exc
        )
        return None

    # Prefer pay-as-you-go meters; if every meter was excluded (unusual), fall
    # back to everything rather than returning nothing.
    chosen = preferred or all_prices
    if not chosen:
        return None
    return _representative_price(chosen)


def _representative_price(entries: list[tuple[float, str]]) -> tuple[float, str]:
    """Median price within the dominant unit group of ``entries``.

    A service's meters are priced in different units (hours, GB-months,
    months). Medians across mixed units are meaningless, so prices are grouped
    by unit first and the group with the most meters wins — the unit a user
    is most likely to encounter. The min would be a cheapest-spot SKU, which
    is why the median is used instead.
    """
    by_unit: dict[str, list[float]] = {}
    for price, unit in entries:
        by_unit.setdefault(unit, []).append(price)
    dominant_unit, prices = max(by_unit.items(), key=lambda pair: len(pair[1]))
    return statistics.median(prices), dominant_unit


def _escape_odata(value: str) -> str:
    """Escape a value for an OData ``eq`` filter (single quotes doubled)."""
    return value.replace("'", "''")


def estimate_live(config: dict[str, Any] | None = None) -> dict[str, Any]:
    """Estimate monthly cost from a config using live Retail Prices.

    Args:
        config: Same shape as :func:`cloudoptima.pricing.static_db.estimate` —
            a dict with an optional ``"services"`` list of names or
            ``{"service": ..., "quantity": ...}`` dicts.

    Returns:
        A dict with ``estimate``, ``items``, ``unknown``, and ``source``.
        ``source`` is ``"azure_retail_api"`` when every known service came
        from the live API, ``"static_fallback"`` when at least one service
        was priced from the static catalog (offline / unknown in region), and
        ``"static"`` when the live API was entirely unavailable. Unknown
        services contribute $0 and are reported in ``unknown``.

    Note:
        Live prices are per-unit (per hour, per GB-Mo, ...), so the total is
        only a true monthly figure when every ``quantity`` is expressed per
        month; for hourly services multiply by hours used.
    """
    services = (config or {}).get("services", [])
    items: list[dict[str, Any]] = []
    unknown: list[str] = []
    total = 0.0
    used_live = False
    used_static = False

    for entry in services if isinstance(services, list) else []:
        if isinstance(entry, str):
            name, quantity = entry, 1.0
        elif isinstance(entry, dict):
            raw_name = entry.get("service", entry.get("name"))
            if not isinstance(raw_name, str):
                continue
            name, quantity = raw_name, float(entry.get("quantity", 1.0) or 1.0)
        else:
            continue

        region = (
            str(entry.get("region", "uaenorth")) if isinstance(entry, dict) else "uaenorth"
        )
        price = get_price(name, region)
        source = "live"
        if price is None:
            # Not in the region / offline — fall back to the static catalog.
            price = lookup(name)
            source = "static"
        if price is None:
            unknown.append(name)
            continue

        if source == "live":
            used_live = True
        else:
            used_static = True
        line_total = round(price * quantity, 2)
        total += line_total
        items.append(
            {
                "service": name,
                "quantity": quantity,
                "price": price,
                "total": line_total,
                "source": source,
            }
        )

    if used_live and not used_static:
        source_label = "azure_retail_api"
    elif used_live:
        source_label = "static_fallback"
    else:
        source_label = "static"

    return {
        "estimate": round(total, 2),
        "items": items,
        "unknown": unknown,
        "source": source_label,
    }
