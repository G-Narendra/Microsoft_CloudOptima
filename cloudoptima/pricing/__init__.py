"""CloudOptima pricing — static catalog + live Azure Retail Prices lookups.

Public API (see each submodule for details):

- :data:`STATIC_PRICES` / :data:`KNOWN_AZURE_SERVICES` — the immutable,
  read-only price catalog (Phase 10.2 AI-poisoning defense and Phase 8.3).
- :func:`lookup` — price a single service from the static catalog.
- :func:`estimate` — estimate a monthly cost from a config, offline.
- :func:`get_price` / :func:`estimate_live` — live Azure Retail Prices API
  lookups with a 1-hour cache and automatic static fallback (Phase 8.4).
"""

from __future__ import annotations

from cloudoptima.pricing.azure_api import (
    CACHE_TTL_SECONDS,
    RETAIL_API_BASE,
    clear_cache,
    estimate_live,
    get_price,
    get_price_with_unit,
)
from cloudoptima.pricing.grounding import (
    SOURCE_LABELS,
    extract_services,
    live_prices,
    render_price_block,
)
from cloudoptima.pricing.static_db import (
    KNOWN_AZURE_SERVICES,
    STATIC_PRICES,
    estimate,
    lookup,
)

__all__ = [
    "CACHE_TTL_SECONDS",
    "KNOWN_AZURE_SERVICES",
    "RETAIL_API_BASE",
    "SOURCE_LABELS",
    "STATIC_PRICES",
    "clear_cache",
    "estimate",
    "estimate_live",
    "extract_services",
    "get_price",
    "get_price_with_unit",
    "live_prices",
    "lookup",
    "render_price_block",
]
