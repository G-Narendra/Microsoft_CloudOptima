"""Live Azure pricing grounding — wires the Retail Prices API into the pipeline.

Before this module, the cost analyst priced line items from the model's
training data and the dashboard showed no authoritative numbers at all. This
closes that gap:

- :func:`extract_services` finds the Azure services mentioned in the
  architect's design and the user's free text.
- :func:`live_prices` looks each one up in the live Azure Retail Prices API
  (free, no auth) with the static catalog as the offline fallback.
- :func:`render_price_block` turns the rows into the factual text block the
  cost analyst's prompt carries.

The static catalog stays the *validation* authority (Phase 10.2) — the LLM may
only name catalog services in its breakdown — while the *numbers* it reasons
over now come from Azure itself.
"""

from __future__ import annotations

from typing import Any, Final

from cloudoptima.pricing.azure_api import get_price_with_unit
from cloudoptima.pricing.static_db import lookup

# Free-text / catalog service names -> catalog display name. The longest
# needle wins (table is sorted by length at import), so "azure kubernetes
# service" matches before the "aks" shorthand in the same sentence. Only
# needles that are unlikely to appear inside an unrelated word are listed.
_SYNONYMS: Final[tuple[tuple[str, str], ...]] = (
    ("azure kubernetes service", "Azure Kubernetes Service"),
    ("azure database for postgresql", "Azure Database for PostgreSQL"),
    ("azure database for mysql", "Azure Database for MySQL"),
    ("azure database for mariadb", "Azure Database for MariaDB"),
    ("azure virtual machine scale sets", "Virtual Machine Scale Sets"),
    ("virtual machine scale sets", "Virtual Machine Scale Sets"),
    ("microsoft defender for cloud", "Microsoft Defender for Cloud"),
    ("azure application gateway", "Application Gateway"),
    ("azure container registry", "Container Registry"),
    ("azure container apps", "Container Apps"),
    ("azure synapse analytics", "Synapse Analytics"),
    ("azure data factory", "Data Factory"),
    ("azure openai service", "Azure OpenAI Service"),
    ("azure ai services", "Cognitive Services"),
    ("cognitive services", "Cognitive Services"),
    ("azure cache for redis", "Azure Cache for Redis"),
    ("azure sql database", "Azure SQL Database"),
    ("application insights", "Application Insights"),
    ("stream analytics", "Stream Analytics"),
    ("content delivery network", "Content Delivery Network"),
    ("application gateway", "Application Gateway"),
    ("virtual machines", "Virtual Machines"),
    ("postgresql", "Azure Database for PostgreSQL"),
    ("azure databricks", "Azure Databricks"),
    ("azure app service", "App Service"),
    ("app service", "App Service"),
    ("azure functions", "Functions"),
    ("api management", "API Management"),
    ("event hubs", "Event Hubs"),
    ("service bus", "Service Bus"),
    ("load balancer", "Load Balancer"),
    ("virtual network", "Virtual Network"),
    ("traffic manager", "Traffic Manager"),
    ("private link", "Private Link"),
    ("azure firewall", "Azure Firewall"),
    ("ddos protection", "DDoS Protection"),
    ("expressroute", "ExpressRoute"),
    ("vpn gateway", "VPN Gateway"),
    ("azure bastion", "Azure Bastion"),
    ("log analytics", "Log Analytics"),
    ("azure monitor", "Azure Monitor"),
    ("azure key vault", "Key Vault"),
    ("key vault", "Key Vault"),
    ("azure dns", "Azure DNS"),
    ("azure files", "Azure Files"),
    ("blob storage", "Blob Storage"),
    ("storage account", "Storage Account"),
    ("azure sql", "Azure SQL Database"),
    ("container registry", "Container Registry"),
    ("container apps", "Container Apps"),
    ("synapse analytics", "Synapse Analytics"),
    ("data factory", "Data Factory"),
    ("redis cache", "Azure Cache for Redis"),
    ("redis", "Azure Cache for Redis"),
    ("cosmos db", "Cosmos DB"),
    ("front door", "Azure Front Door"),
    ("aks", "Azure Kubernetes Service"),
    ("mysql", "Azure Database for MySQL"),
    ("mariadb", "Azure Database for MariaDB"),
    ("postgres", "Azure Database for PostgreSQL"),
    ("databricks", "Azure Databricks"),
)

# Sorted longest-needle-first so overlapping mentions resolve correctly.
_SORTED_SYNONYMS: Final[tuple[tuple[str, str], ...]] = tuple(
    sorted(_SYNONYMS, key=lambda pair: len(pair[0]), reverse=True)
)

# Catalog display name -> Retail API serviceName, only where they differ.
# The values below were verified against the live API (Aug 2026) — several
# serviceName values carry no "Azure " prefix ("SQL Database", "Redis
# Cache"), so sending the wrong casing/prefix means a static fallback instead
# of a live hit. Names absent here are queried as-is.
_API_NAMES: Final[dict[str, str]] = {
    "AKS": "Azure Kubernetes Service",
    "Azure SQL": "SQL Database",
    "Azure SQL Database": "SQL Database",
    "PostgreSQL": "Azure Database for PostgreSQL",
    "MySQL": "Azure Database for MySQL",
    "MariaDB": "Azure Database for MariaDB",
    "Blob Storage": "Storage",
    "Storage Account": "Storage",
    "Cosmos DB": "Azure Cosmos DB",
    "Azure Cache for Redis": "Redis Cache",
    "App Service": "Azure App Service",
    "Container Apps": "Azure Container Apps",
    "Synapse Analytics": "Azure Synapse Analytics",
}

#: Human-readable source labels used in prompts and the dashboard.
SOURCE_LABELS: Final[dict[str, str]] = {
    "live": "azure_retail_api",
    "static": "static_catalog",
}


def extract_services(*texts: str | None) -> list[str]:
    """Return the catalog service names mentioned across ``texts``.

    Matching is a case-insensitive substring scan of the aliases in
    :data:`_SYNONYMS`, longest needle first, deduplicated and in first-mention
    order. Unknown services are ignored — only catalog names come back, so a
    downstream :func:`live_prices` call can always fall back to a static price.

    Args:
        texts: Free text to scan, e.g. the user's services line and the
            architect's JSON design.

    Returns:
        Catalog service names (e.g. ``"Azure SQL Database"``), in order of
        first mention, with duplicates removed.
    """
    haystack = " ".join((text or "") for text in texts).casefold()
    found: list[str] = []
    seen: set[str] = set()
    for needle, name in _SORTED_SYNONYMS:
        if needle in haystack and name not in seen:
            seen.add(name)
            found.append(name)
    return found


def live_prices(service_names: list[str], region: str) -> list[dict[str, Any]]:
    """Fetch live retail prices for ``service_names`` in ``region``.

    Each service is queried against the Azure Retail Prices API; a service the
    API cannot price (wrong name variant, offline, unknown in the region) falls
    back to the static catalog, and the per-row ``source`` says which one was
    used. Rows never raise — pricing is advisory, the pipeline must not crash
    on a network blip.

    Args:
        service_names: Catalog service names (from :func:`extract_services`).
        region: ARM region name, e.g. ``"uaenorth"``.

    Returns:
        A list of ``{"service", "price", "unit", "source"}`` dicts — price in
        USD for the given unit (median of the region's dominant pay-as-you-go
        meter group, e.g. ``"1 Hour"`` or ``"1 GB-Mo"``), source either
        ``"live"`` (Azure Retail API) or ``"static"`` (catalog, unit
        ``"month"``).
    """
    rows: list[dict[str, Any]] = []
    for name in service_names:
        api_name = _API_NAMES.get(name, name)
        result = get_price_with_unit(api_name, region)
        source = "live"
        if result is None:
            price = lookup(name)
            unit = "month"
            source = "static"
        else:
            price, unit = result
        if price is None:
            continue
        rows.append(
            {
                "service": name,
                "price": round(float(price), 6),
                "unit": unit,
                "source": source,
            }
        )
    return rows


def render_price_block(rows: list[dict[str, Any]], region: str) -> str:
    """Render live pricing rows as the factual block the cost analyst sees.

    The wording is deliberately neutral (no imperatives): the assembled prompt
    is scanned by ``detect_injection``, and instruction-like phrases would trip
    a false positive. The system prompt carries the actual guidance.

    Args:
        rows: Rows from :func:`live_prices`.
        region: ARM region name for the header.

    Returns:
        A multi-line text block listing each service, its per-unit USD price,
        and the data source.
    """
    if not rows:
        return (
            "LIVE AZURE RETAIL PRICES: no Azure services matched in the "
            "design, so no live prices were fetched for this region."
        )
    lines = [
        f"LIVE AZURE RETAIL PRICES (region: {region}, source: Azure Retail "
        "Prices API, free no-auth endpoint)",
        "Per-unit list prices in USD (unit varies by service).",
        "",
    ]
    for row in rows:
        label = SOURCE_LABELS.get(str(row.get("source", "static")), "static")
        unit = row.get("unit", "unit")
        lines.append(f"- {row['service']}: ${row['price']:,.2f} per {unit} [{label}]")
    return "\n".join(lines)
