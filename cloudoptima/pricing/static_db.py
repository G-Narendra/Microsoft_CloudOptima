"""Static Azure service price catalog (Phase 8.3).

The read-only authority on Azure service prices. Numbers are indicative
monthly USD per the listed unit; the live Retail Prices API
(:mod:`cloudoptima.pricing.azure_api`) supplies authoritative figures when
reachable, and this table remains the offline fallback plus the validation
authority.

Prices are read-only: rows are a tuple and the public views are
:class:`types.MappingProxyType` — nothing can mutate them at runtime. That's
also the Phase 10.2 AI-poisoning defense: the cost analyst may only name
services present in :data:`KNOWN_AZURE_SERVICES`.
"""

from __future__ import annotations

from types import MappingProxyType
from typing import Any, Final

# (service display name, monthly USD, notes). Name variants are listed
# deliberately ("Azure SQL" / "Azure SQL Database") so a real LLM's natural
# wording is not rejected by the strict catalog check.
_STATIC_ROWS: Final[tuple[tuple[str, float, str], ...]] = (
    ("AKS", 1800.00, "per 3-node D4s_v3 pool"),
    ("Azure Kubernetes Service", 1800.00, "managed control plane included"),
    ("Azure SQL", 920.00, "General Purpose, 8 vCores"),
    ("Azure SQL Database", 920.00, "General Purpose, 8 vCores"),
    ("Azure Database for PostgreSQL", 550.00, "General Purpose"),
    ("PostgreSQL", 550.00, "General Purpose"),
    ("Azure Database for MySQL", 350.00, "General Purpose"),
    ("Azure Database for MariaDB", 250.00, "General Purpose"),
    ("Blob Storage", 150.00, "Hot tier, 2TB"),
    ("Storage Account", 150.00, "Blob hot tier, 2TB"),
    ("Azure Files", 120.00, "Premium, 1TB"),
    ("Cosmos DB", 600.00, "Serverless, 1M RU/s tier"),
    ("Azure Cache for Redis", 450.00, "Premium P1"),
    ("Redis Cache", 450.00, "Premium P1"),
    ("Front Door", 380.00, "Standard tier"),
    ("Azure Front Door", 380.00, "Standard tier"),
    ("Application Gateway", 300.00, "Standard v2"),
    ("Load Balancer", 25.00, "Standard, 1 rule"),
    ("Traffic Manager", 5.00, "1 endpoint profile"),
    ("Virtual Network", 40.00, "regional VNet"),
    ("Networking", 250.00, "VNet, NSGs, bandwidth"),
    ("Azure Firewall", 1200.00, "Standard, 1 instance"),
    ("DDoS Protection", 3000.00, "Standard, per-resource"),
    ("Key Vault", 0.50, "Standard, 10k transactions"),
    ("Azure Key Vault", 0.50, "Standard, 10k transactions"),
    ("Managed Identity", 0.00, "per identity"),
    ("Microsoft Entra ID", 0.00, "free tier"),
    ("Azure Active Directory", 0.00, "free tier"),
    ("Log Analytics", 300.00, "Monitoring & alerts"),
    ("Monitoring", 300.00, "Log Analytics, alerts"),
    ("Application Insights", 50.00, "pay-as-you-go, 5GB"),
    ("Azure Monitor", 300.00, "Log Analytics, alerts"),
    ("App Service", 150.00, "P1v3, 1 instance"),
    ("Container Apps", 200.00, "consumption, 1 replica"),
    ("Functions", 30.00, "serverless, 1M executions"),
    ("Azure Functions", 30.00, "serverless, 1M executions"),
    ("Container Registry", 20.00, "Basic, 1 registry"),
    ("Azure Container Registry", 20.00, "Basic, 1 registry"),
    ("Virtual Machines", 70.00, "Standard_D2s_v3, 1 instance"),
    ("Virtual Machine Scale Sets", 70.00, "Standard_D2s_v3, 1 instance"),
    ("Azure Bastion", 150.00, "Basic, 1 instance"),
    ("VPN Gateway", 30.00, "Basic, 1 connection"),
    ("ExpressRoute", 120.00, "1 Gbps, 1 circuit"),
    ("Private Link", 15.00, "1 private endpoint"),
    ("API Management", 700.00, "Developer tier"),
    ("Event Hubs", 20.00, "Standard, 1 TU"),
    ("Service Bus", 15.00, "Standard, 1 messaging unit"),
    ("IoT Hub", 60.00, "S1, 1 unit"),
    ("Stream Analytics", 120.00, "1 streaming unit"),
    ("SignalR", 60.00, "Free, 20 connections"),
    ("Azure Databricks", 200.00, "premium, light usage"),
    ("Synapse Analytics", 400.00, "dedicated SQL pool, DW100c"),
    ("Azure Synapse Analytics", 400.00, "dedicated SQL pool, DW100c"),
    ("Data Factory", 100.00, "orchestration, 50 activities"),
    ("Azure Data Factory", 100.00, "orchestration, 50 activities"),
    ("Cognitive Services", 60.00, "S0, mixed usage"),
    ("Azure AI Services", 60.00, "S0, mixed usage"),
    ("Azure OpenAI Service", 100.00, "gpt-4o-mini, mixed usage"),
    ("OpenAI", 100.00, "gpt-4o-mini, mixed usage"),
    ("Backup", 80.00, "VMs + files, 1TB"),
    ("Azure Site Recovery", 40.00, "1 VM replicated"),
    ("Microsoft Defender for Cloud", 150.00, "pay-as-you-go, 10 resources"),
    ("Defender for Cloud", 150.00, "pay-as-you-go, 10 resources"),
    ("Content Delivery Network", 60.00, "standard, 1TB egress"),
    ("Azure DNS", 0.50, "1 hosted zone"),
)

# Read-only mapping of service name -> indicative monthly USD.
STATIC_PRICES: Final[MappingProxyType[str, float]] = MappingProxyType(
    {name: price for name, price, _notes in _STATIC_ROWS}
)

#: The set of services agents are allowed to reference.
KNOWN_AZURE_SERVICES: Final[frozenset[str]] = frozenset(STATIC_PRICES)


def lookup(
    service: str, region: str | None = None, tier: str | None = None
) -> float | None:
    """Return the monthly USD price for ``service``, or ``None`` if unknown.

    Args:
        service: A catalog service name, e.g. ``"AKS"`` or
            ``"Azure SQL Database"`` — matching is case-insensitive and
            whitespace-tolerant.
        region: Ignored (accepted for API parity with
            :func:`cloudoptima.pricing.azure_api.get_price`).
        tier: Ignored (accepted for API parity).

    Returns:
        The monthly price in USD, or ``None`` when the service isn't in the
        catalog.
    """
    del region, tier  # static catalog is region/tier-agnostic (Phase 8.4 adds live tiers)
    if not isinstance(service, str):
        return None
    normalized = service.strip()
    if not normalized:
        return None
    exact = STATIC_PRICES.get(normalized)
    if exact is not None:
        return exact
    folded = normalized.casefold()
    for name, price in STATIC_PRICES.items():
        if name.casefold() == folded:
            return price
    return None


def estimate(config: dict[str, Any] | None = None) -> dict[str, Any]:
    """Estimate a monthly cost from a service configuration.

    Args:
        config: A dict with an optional ``"services"`` list, each item either
            a string service name or a dict with ``"service"`` and an optional
            ``"quantity"`` multiplier. Any other top-level keys are ignored.

    Returns:
        A dict with ``estimate`` (float, sum of known services), ``items``
        (per-service detail), ``source`` (``"static"``), and ``unknown`` (the
        services that could not be priced). Unknown services contribute $0
        and are reported, never silently dropped.
    """
    services = (config or {}).get("services", [])
    items: list[dict[str, Any]] = []
    unknown: list[str] = []
    total = 0.0

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
        price = lookup(name)
        if price is None:
            unknown.append(name)
            continue
        line_total = round(price * quantity, 2)
        total += line_total
        items.append({"service": name, "quantity": quantity, "price": price, "total": line_total})

    return {
        "estimate": round(total, 2),
        "items": items,
        "unknown": unknown,
        "source": "static",
    }
