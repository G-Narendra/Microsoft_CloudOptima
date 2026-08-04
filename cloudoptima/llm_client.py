"""LLM client abstraction layer for CloudOptima.

Provides a unified interface for multiple LLM backends (Mock, Nvidia NIM,
Azure OpenAI) with a factory function and retry wrapper for fault tolerance.
"""

from __future__ import annotations

import json
import logging
import re
import time
from abc import ABC, abstractmethod
from typing import Any, cast

import httpx
import openai

from cloudoptima.config import Settings

_logger = logging.getLogger(__name__)


# ── Control Character Sanitization ────────────────────────────────────────────


def _strip_control_chars(text: str) -> str:
    """Remove ANSI escape codes, null bytes, and non-printable control chars.

    Preserves newlines (\\n), carriage returns (\\r), and tabs (\\t).
    """
    # Strip ANSI escape sequences
    text = re.sub(r"\x1b\[[0-9;]*[a-zA-Z]", "", text)
    # Strip null bytes
    text = text.replace("\x00", "")
    # Strip remaining control chars except \\n, \\r, \\t
    text = re.sub(r"[\x01-\x08\x0b\x0c\x0e-\x1f\x7f]", "", text)
    return text


# ── Abstract Base Class ───────────────────────────────────────────────────────


class BaseLLMClient(ABC):
    """Abstract base class for all LLM client implementations."""

    @abstractmethod
    def generate(self, prompt: str, system_prompt: str = "") -> str:
        """Send a prompt to the LLM and return the raw text response.

        Args:
            prompt: The user/agent prompt text.
            system_prompt: Optional system-level instruction prompt.

        Returns:
            Raw string response from the LLM.
        """


# ── Mock Client ───────────────────────────────────────────────────────────────


MOCK_RESPONSES: dict[str, dict[str, Any]] = {
    "architect": {
        "compute": {
            "recommendation": "Azure Kubernetes Service (AKS) with 3 node pools",
            "justification": "AKS provides managed Kubernetes for microservices workloads",
            "alternatives": ["Azure Container Apps", "Azure App Service"],
        },
        "storage": {
            "recommendation": "Azure Blob Storage (Hot tier) + Azure SQL Database",
            "justification": "Blob for unstructured data, SQL for transactional",
            "alternatives": ["Cosmos DB", "Azure Table Storage"],
        },
        "networking": {
            "recommendation": "Azure Virtual Network with NSGs and Azure Front Door",
            "justification": "VNet isolation with global load balancing",
            "alternatives": ["Application Gateway", "Traffic Manager"],
        },
        "data": {
            "recommendation": "Azure SQL Database (General Purpose) + Redis Cache",
            "justification": "Relational DB for OLTP with caching layer",
            "alternatives": ["Cosmos DB", "Azure Database for PostgreSQL"],
        },
    },
    "cost": {
        "estimate": 4250.00,
        "currency": "USD",
        "breakdown": [
            {"service": "AKS", "cost": 1800.00, "notes": "3 nodes, D4s_v3"},
            {"service": "Azure SQL", "cost": 920.00, "notes": "General Purpose, 8 vCores"},
            {"service": "Blob Storage", "cost": 150.00, "notes": "Hot tier, 2TB"},
            {"service": "Front Door", "cost": 380.00, "notes": "Standard tier"},
            {"service": "Redis Cache", "cost": 450.00, "notes": "Premium P1"},
            {"service": "Networking", "cost": 250.00, "notes": "VNet, NSGs, bandwidth"},
            {"service": "Monitoring", "cost": 300.00, "notes": "Log Analytics, alerts"},
        ],
        "budget_status": "UNDER",
        "savings": [
            "Consider reserved instances for AKS nodes (up to 40% savings)",
            "Use Azure Hybrid Benefit if existing Windows Server licenses available",
            "Archive cold data to Cool or Archive tier storage",
        ],
    },
    "security": {
        "findings": [
            {
                "control": "Encryption at Rest",
                "status": "PASS",
                "details": "Azure SQL TDE enabled by default",
                "cvss_score": None,
            },
            {
                "control": "Encryption in Transit",
                "status": "PASS",
                "details": "TLS 1.2+ enforced on all endpoints",
                "cvss_score": None,
            },
            {
                "control": "Network Segmentation",
                "status": "WARNING",
                "details": "NSGs configured but no Azure Firewall for egress filtering",
                "cvss_score": 4.3,
            },
            {
                "control": "Identity & Access",
                "status": "PASS",
                "details": "Managed Identity for AKS, RBAC for Azure SQL",
                "cvss_score": None,
            },
            {
                "control": "Key Management",
                "status": "CONFIG_NEEDED",
                "details": "Customer-managed keys not configured for Blob Storage",
                "cvss_score": 3.1,
            },
        ],
        "overall_risk_rating": "MEDIUM",
        "recommendations": [
            "Add Azure Firewall for egress traffic control",
            "Enable customer-managed keys for Blob Storage",
            "Configure Azure DDoS Protection Standard",
        ],
    },
    "compliance": {
        "framework": "PDPL",
        "rules": [
            {
                "rule_id": "01",
                "rule_name": "Data Residency",
                "status": "PASS",
                "details": "All resources deployed in UAE North region",
            },
            {
                "rule_id": "02",
                "rule_name": "Encryption at Rest",
                "status": "PASS",
                "details": "AES-256 encryption enabled across all storage services",
            },
            {
                "rule_id": "04",
                "rule_name": "Access Control",
                "status": "PASS",
                "details": "RBAC and MFA enforced via Azure AD",
            },
            {
                "rule_id": "05",
                "rule_name": "Audit Logging",
                "status": "CONFIG_NEEDED",
                "details": "Azure Monitor configured but log retention set to 30 days",
            },
        ],
        "overall_status": "NEEDS_WORK",
        "remediation_steps": [
            "Extend audit log retention to minimum 90 days per PDPL requirements",
            "Enable diagnostic settings for all Azure resources",
        ],
    },
    "judge": {
        "arbitration": {
            "conflicts_detected": 2,
            "conflict_summaries": [
                {
                    "dimension": "cost_vs_security",
                    "agents_involved": ["cost_analyst", "security"],
                    "issue": "Security recommends Azure Firewall ($1,200/mo) exceeding budget",
                    "resolution": "Use NSG rules with Azure DDoS Basic (free) as compromise",
                },
                {
                    "dimension": "architect_vs_compliance",
                    "agents_involved": ["architect", "compliance"],
                    "issue": "Audit log retention set to 30 days, compliance requires 90 days",
                    "resolution": "Extend Log Analytics retention to 90 days (+$45/mo)",
                },
            ],
        },
        "final_recommendation": "Proceed with AKS-based architecture with noted adjustments",
        "overridden_agents": ["security"],
        "justification": "Balanced cost and security by using NSG-based controls with DDoS Basic",
    },
}


# Role markers that name the agent in its system prompt. More specific markers
# come first, so "cost analyst" beats a bare "cost" mention in user text.
_ROLE_MARKERS: tuple[tuple[str, str], ...] = (
    ("cost analyst", "cost"),
    ("security engineer", "security"),
    ("compliance officer", "compliance"),
    ("judge", "judge"),
    ("architect", "architect"),
)


def _detect_agent_type(prompt: str, system_prompt: str = "") -> str:
    """Detect which agent type a prompt is intended for.

    The system prompt is authoritative because it names the role, so it is
    checked first. This matters in the real pipeline: downstream agents carry
    earlier outputs in their prompt (the architect's design mentions "compute"
    and "design"), which would otherwise misroute the mock response. The
    combined-text keyword scan remains as a fallback for callers that do not
    pass a system prompt.
    """
    system_lower = system_prompt.lower()
    for marker, agent_key in _ROLE_MARKERS:
        if marker in system_lower:
            return agent_key

    combined = f"{system_prompt} {prompt}".lower()
    if "architect" in combined or "compute" in combined or "design" in combined:
        return "architect"
    if "cost" in combined or "budget" in combined or "estimate" in combined:
        return "cost"
    if "security" in combined or "vulnerability" in combined or "risk" in combined:
        return "security"
    if "compliance" in combined or "regulation" in combined or "pdpl" in combined:
        return "compliance"
    if "judge" in combined or "conflict" in combined or "arbitrat" in combined:
        return "judge"
    return "architect"


class MockClient(BaseLLMClient):
    """Mock LLM client returning canned responses per agent type.

    Used for development, testing, and demo mode. No API keys required.
    """

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        """Return a canned JSON response based on detected agent type."""
        agent_key = _detect_agent_type(prompt, system_prompt)
        response = MOCK_RESPONSES.get(agent_key, MOCK_RESPONSES["architect"])
        time.sleep(0.05)  # Simulate minimal latency
        return json.dumps(response)


# ── Nvidia NIM Client ─────────────────────────────────────────────────────────


class NvidiaClient(BaseLLMClient):
    """LLM client for Nvidia NIM API via httpx.

    Calls the OpenAI-compatible chat/completions endpoint at
    https://integrate.api.nvidia.com/v1.
    """

    BASE_URL = "https://integrate.api.nvidia.com/v1"

    def __init__(
        self, settings: Settings, model: str | None = None, timeout: float | None = None
    ) -> None:
        self._api_key = settings.nvidia_api_key.get_secret_value()
        self._model = model or settings.llm_model
        self._temperature = settings.llm_temperature
        self._timeout = timeout if timeout is not None else settings.llm_timeout

        if not self._api_key:
            raise ValueError(
                "nvidia_api_key is required for NvidiaClient. "
                "Set NVIDIA_API_KEY in .env or use DEMO_MODE=true."
            )

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        """Send a chat completion request to Nvidia NIM API."""
        messages: list[dict[str, str]] = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        payload = {
            "model": self._model,
            "messages": messages,
            "temperature": self._temperature,
            "max_tokens": 4096,
        }

        with httpx.Client(
            base_url=self.BASE_URL,
            headers=headers,
            timeout=float(self._timeout),
        ) as client:
            response = client.post("/chat/completions", json=payload)
            response.raise_for_status()
            data = response.json()

        content: str = data["choices"][0]["message"]["content"]
        if not content:
            _logger.warning("NvidiaClient received empty response")
            return ""
        return _strip_control_chars(content)


# ── Azure OpenAI Client ──────────────────────────────────────────────────────


class AzureClient(BaseLLMClient):
    """LLM client for Azure OpenAI via the openai Python SDK.

    Supports JSON mode via response_format parameter.
    """

    def __init__(
        self, settings: Settings, model: str | None = None, timeout: float | None = None
    ) -> None:
        api_key = settings.azure_openai_api_key.get_secret_value()
        if not api_key:
            raise ValueError(
                "azure_openai_api_key is required for AzureClient. "
                "Set AZURE_OPENAI_API_KEY in .env or use DEMO_MODE=true."
            )
        if not settings.azure_openai_endpoint:
            raise ValueError(
                "azure_openai_endpoint is required for AzureClient. "
                "Set AZURE_OPENAI_ENDPOINT in .env."
            )

        self._client = openai.AzureOpenAI(
            api_key=api_key,
            api_version=settings.azure_openai_api_version,
            azure_endpoint=settings.azure_openai_endpoint,
        )
        self._model = model or settings.llm_model
        self._temperature = settings.llm_temperature
        self._timeout = timeout if timeout is not None else settings.llm_timeout

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        """Send a chat completion request to Azure OpenAI with JSON mode."""
        messages: list[dict[str, str]] = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        else:
            messages.append(
                {"role": "system", "content": "Respond with valid JSON."}
            )
        messages.append({"role": "user", "content": prompt})

        response = self._client.chat.completions.create(
            messages=cast(Any, messages),
            model=self._model,
            temperature=self._temperature,
            response_format={"type": "json_object"},
            timeout=float(self._timeout),
        )

        content = response.choices[0].message.content
        if not content:
            _logger.warning("AzureClient received empty response")
            return ""
        return _strip_control_chars(content)


# ── Factory Function ─────────────────────────────────────────────────────────


def create_llm_client(settings: Settings) -> BaseLLMClient:
    """Create an LLM client based on the configured provider.

    Args:
        settings: Application settings with provider and API key config.

    Returns:
        A concrete BaseLLMClient implementation.

    Raises:
        ValueError: If the provider is not recognized.
    """
    provider = settings.llm_provider
    if provider == "mock":
        return MockClient()
    elif provider == "nvidia":
        return NvidiaClient(settings)
    elif provider == "azure":
        return AzureClient(settings)
    else:
        raise ValueError(
            f"Unknown LLM provider '{provider}'. "
            f"Expected one of: mock, nvidia, azure."
        )


# ── Retry Wrapper ─────────────────────────────────────────────────────────────


def generate_with_retry(
    client: BaseLLMClient,
    prompt: str,
    system_prompt: str = "",
    max_retries: int = 3,
    base_delay: float = 1.0,
) -> str:
    """Call client.generate() with exponential backoff retry logic.

    Args:
        client: The LLM client to use.
        prompt: The user/agent prompt.
        system_prompt: Optional system prompt.
        max_retries: Maximum number of attempts (default 3).
        base_delay: Base delay in seconds for exponential backoff.

    Returns:
        The LLM response string.

    Raises:
        The last exception if all retries are exhausted.
    """
    last_exception: Exception | None = None

    for attempt in range(max_retries):
        try:
            return client.generate(prompt, system_prompt)
        except (  # noqa: PERF203
            httpx.HTTPStatusError,
            httpx.TimeoutException,
            openai.APIError,
            TimeoutError,
            ConnectionError,
        ) as exc:
            last_exception = exc
            if attempt < max_retries - 1:
                delay = base_delay * (2**attempt)
                _logger.warning(
                    "LLM request failed (attempt %d/%d): %s. "
                    "Retrying in %.1fs...",
                    attempt + 1,
                    max_retries,
                    str(exc),
                    delay,
                )
                time.sleep(delay)
            else:
                _logger.error(
                    "LLM request failed after %d attempts: %s",
                    max_retries,
                    str(exc),
                )

    if last_exception is not None:
        raise last_exception
    raise RuntimeError("generate_with_retry: unexpected state")  # pragma: no cover
