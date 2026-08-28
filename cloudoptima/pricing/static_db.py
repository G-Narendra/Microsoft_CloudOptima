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

# (service display name, monthly USD, notes). Name variants are listed deliberately
# so a real LLM's natural wording is never rejected by the strict catalog check.
# Each Azure service has its "with Azure prefix" and "without prefix" variant.
_STATIC_ROWS: Final[tuple[tuple[str, float, str], ...]] = (
    # Compute
    ("AKS", 1800.00, "per 3-node D4s_v3 pool"),
    ("Azure Kubernetes Service", 1800.00, "managed control plane included"),
    ("Azure Kubernetes Service (AKS)", 1800.00, "managed control plane included"),
    ("Azure App Service", 150.00, "P1v3, 1 instance"),
    ("App Service", 150.00, "P1v3, 1 instance"),
    ("Azure Container Apps", 200.00, "consumption, 1 replica"),
    ("Container Apps", 200.00, "consumption, 1 replica"),
    ("Azure Functions", 30.00, "serverless, 1M executions"),
    ("Functions", 30.00, "serverless, 1M executions"),
    ("Azure Container Registry", 20.00, "Basic, 1 registry"),
    ("Container Registry", 20.00, "Basic, 1 registry"),
    ("Azure Virtual Machines", 70.00, "Standard_D2s_v3, 1 instance"),
    ("Virtual Machines", 70.00, "Standard_D2s_v3, 1 instance"),
    ("Virtual Machine Scale Sets", 70.00, "Standard_D2s_v3, 1 instance"),
    ("Azure Batch", 0.00, "pay-per-compute-second"),
    ("Azure Service Fabric", 0.00, "open-source; only VM costs"),
    # Database
    ("Azure SQL", 920.00, "General Purpose, 8 vCores"),
    ("Azure SQL Database", 920.00, "General Purpose, 8 vCores"),
    ("Azure SQL Managed Instance", 1200.00, "General Purpose, 8 vCores"),
    ("Azure Database for PostgreSQL", 550.00, "General Purpose"),
    ("PostgreSQL", 550.00, "General Purpose"),
    ("Azure Database for MySQL", 350.00, "General Purpose"),
    ("MySQL", 350.00, "General Purpose"),
    ("Azure Database for MariaDB", 250.00, "General Purpose"),
    ("Azure Cosmos DB", 600.00, "Serverless, 1M RU/s tier"),
    ("Cosmos DB", 600.00, "Serverless, 1M RU/s tier"),
    # Storage
    ("Azure Blob Storage", 150.00, "Hot tier, 2TB"),
    ("Blob Storage", 150.00, "Hot tier, 2TB"),
    ("Storage Account", 150.00, "Blob hot tier, 2TB"),
    ("Azure Files", 120.00, "Premium, 1TB"),
    ("Azure Data Lake Storage", 200.00, "Gen2, 2TB"),
    ("Data Lake Storage", 200.00, "Gen2, 2TB"),
    # Cache
    ("Azure Cache for Redis", 450.00, "Premium P1"),
    ("Redis Cache", 450.00, "Premium P1"),
    ("Redis", 450.00, "Premium P1"),
    # Networking
    ("Azure Front Door", 380.00, "Standard tier"),
    ("Front Door", 380.00, "Standard tier"),
    ("Azure Application Gateway", 300.00, "Standard v2"),
    ("Application Gateway", 300.00, "Standard v2"),
    ("Azure Load Balancer", 25.00, "Standard, 1 rule"),
    ("Load Balancer", 25.00, "Standard, 1 rule"),
    ("Azure Traffic Manager", 5.00, "1 endpoint profile"),
    ("Traffic Manager", 5.00, "1 endpoint profile"),
    ("Azure Virtual Network", 40.00, "regional VNet"),
    ("Virtual Network", 40.00, "regional VNet"),
    ("Networking", 250.00, "VNet, NSGs, bandwidth"),
    ("Azure Firewall", 1200.00, "Standard, 1 instance"),
    ("Azure DDoS Protection", 3000.00, "Standard, per-resource"),
    ("DDoS Protection", 3000.00, "Standard, per-resource"),
    ("Azure Private Link", 15.00, "1 private endpoint"),
    ("Private Link", 15.00, "1 private endpoint"),
    ("Azure VPN Gateway", 30.00, "Basic, 1 connection"),
    ("VPN Gateway", 30.00, "Basic, 1 connection"),
    ("Azure ExpressRoute", 120.00, "1 Gbps, 1 circuit"),
    ("ExpressRoute", 120.00, "1 Gbps, 1 circuit"),
    ("Azure Bastion", 150.00, "Basic, 1 instance"),
    ("Azure DNS", 0.50, "1 hosted zone"),
    ("Azure Content Delivery Network", 60.00, "standard, 1TB egress"),
    ("Content Delivery Network", 60.00, "standard, 1TB egress"),
    ("Azure CDN", 60.00, "standard, 1TB egress"),
    # Security
    ("Azure Key Vault", 0.50, "Standard, 10k transactions"),
    ("Key Vault", 0.50, "Standard, 10k transactions"),
    ("Azure Managed Identity", 0.00, "per identity"),
    ("Managed Identity", 0.00, "per identity"),
    ("Microsoft Entra ID", 0.00, "free tier"),
    ("Azure Active Directory", 0.00, "free tier"),
    ("Microsoft Defender for Cloud", 150.00, "pay-as-you-go, 10 resources"),
    ("Defender for Cloud", 150.00, "pay-as-you-go, 10 resources"),
    ("Microsoft Sentinel", 200.00, "pay-as-you-go, 10GB/day"),
    ("Azure Sentinel", 200.00, "pay-as-you-go, 10GB/day"),
    # Monitoring & Observability
    ("Azure Log Analytics", 300.00, "Monitoring & alerts"),
    ("Log Analytics", 300.00, "Monitoring & alerts"),
    ("Azure Monitor", 300.00, "Log Analytics, alerts"),
    ("Monitoring", 300.00, "Log Analytics, alerts"),
    ("Azure Application Insights", 50.00, "pay-as-you-go, 5GB"),
    ("Application Insights", 50.00, "pay-as-you-go, 5GB"),
    # Integration & Messaging
    ("Azure API Management", 700.00, "Developer tier"),
    ("API Management", 700.00, "Developer tier"),
    ("Azure Event Hubs", 20.00, "Standard, 1 TU"),
    ("Event Hubs", 20.00, "Standard, 1 TU"),
    ("Azure Service Bus", 15.00, "Standard, 1 messaging unit"),
    ("Service Bus", 15.00, "Standard, 1 messaging unit"),
    ("Azure SignalR", 60.00, "Free, 20 connections"),
    ("SignalR", 60.00, "Free, 20 connections"),
    ("Azure IoT Hub", 60.00, "S1, 1 unit"),
    ("IoT Hub", 60.00, "S1, 1 unit"),
    ("Azure Stream Analytics", 120.00, "1 streaming unit"),
    ("Stream Analytics", 120.00, "1 streaming unit"),
    # Analytics & AI
    ("Azure Databricks", 200.00, "premium, light usage"),
    ("Azure Synapse Analytics", 400.00, "dedicated SQL pool, DW100c"),
    ("Synapse Analytics", 400.00, "dedicated SQL pool, DW100c"),
    ("Azure Data Factory", 100.00, "orchestration, 50 activities"),
    ("Data Factory", 100.00, "orchestration, 50 activities"),
    ("Azure Cognitive Services", 60.00, "S0, mixed usage"),
    ("Cognitive Services", 60.00, "S0, mixed usage"),
    ("Azure AI Services", 60.00, "S0, mixed usage"),
    ("Azure OpenAI Service", 100.00, "gpt-4o-mini, mixed usage"),
    ("OpenAI", 100.00, "gpt-4o-mini, mixed usage"),
    # Backup & DR
    ("Azure Backup", 80.00, "VMs + files, 1TB"),
    ("Backup", 80.00, "VMs + files, 1TB"),
    ("Azure Site Recovery", 40.00, "1 VM replicated"),
    ("Site Recovery", 40.00, "1 VM replicated"),
    # Dev Tools
    ("Azure DevOps", 30.00, "Basic plan, 5 users"),
    ("Azure Availability Zones", 0.00, "no direct cost"),
    ("Availability Zones", 0.00, "no direct cost"),
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
