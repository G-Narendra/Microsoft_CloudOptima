"""Type-safe application settings.

Loads from environment variables and ``.env`` (via pydantic-settings) and
redacts every secret field from ``repr``/``str`` so keys never show up in
logs or error messages.
"""

from __future__ import annotations

from typing import Annotated

from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from .env and environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # ── LLM Provider & API Keys ───────────────────────
    llm_provider: str = Field(
        default="mock",
        description="LLM provider: mock, nvidia, azure, openai, anthropic, google",
    )
    nvidia_api_key: SecretStr = Field(
        default=SecretStr(""), description="Nvidia NIM API key"
    )
    azure_openai_endpoint: str = Field(
        default="", description="Azure OpenAI Endpoint URL"
    )
    azure_openai_api_key: SecretStr = Field(
        default=SecretStr(""), description="Azure OpenAI API key"
    )
    azure_openai_api_version: str = Field(
        default="2024-02-01", description="Azure OpenAI API version"
    )
    # Phase 7.6: direct OpenAI, Anthropic Claude, and Google Gemini.
    openai_api_key: SecretStr = Field(
        default=SecretStr(""), description="OpenAI (direct) API key"
    )
    anthropic_api_key: SecretStr = Field(
        default=SecretStr(""), description="Anthropic Claude API key"
    )
    google_api_key: SecretStr = Field(
        default=SecretStr(""), description="Google Gemini API key"
    )

    # ── Model Settings ───────────────────────────────
    llm_model: str = Field(
        default="gpt-4o-mini", description="Primary model name"
    )
    llm_temperature: float = Field(
        default=0.1, description="Model sampling temperature (0.0 - 2.0)"
    )
    llm_timeout: int = Field(
        default=30, description="Model request timeout in seconds"
    )

    # ── Cost-aware LLM routing (Phase 7.5) ────────────────────────
    routing_enabled: bool = Field(
        default=False,
        description="Route calls across providers cheapest-first with failover",
    )
    # NoDecode: the env var form is a plain comma string ("nvidia,azure"),
    # which pydantic-settings would otherwise try to JSON-decode and fail on.
    routing_providers: Annotated[list[str], NoDecode] = Field(
        default_factory=lambda: ["openai", "azure", "anthropic", "google", "nvidia"],
        description="Providers eligible for routing "
        "(mock, nvidia, azure, openai, anthropic, google)",
    )
    routing_max_cost_per_request: float = Field(
        default=0.005,
        description="Soft USD cap on estimated input cost before a provider is skipped",
    )
    routing_timeout: float = Field(
        default=10.0,
        gt=0.0,
        description="Per-provider timeout in seconds for routed clients (fail fast)",
    )
    llm_nvidia_model: str = Field(
        default="meta/llama-3.3-70b-instruct",
        description="Nvidia NIM smart-tier model (Architect, Judge)",
    )
    llm_nvidia_fast_model: str = Field(
        default="meta/llama-3.1-8b-instruct",
        description="Nvidia NIM fast-tier model (Cost, Security, Compliance)",
    )
    llm_azure_model: str = Field(
        default="gpt-4o-mini", description="Azure OpenAI smart-tier model"
    )
    llm_azure_fast_model: str = Field(
        default="gpt-4o-mini", description="Azure OpenAI fast-tier model"
    )
    # Phase 7.6: smart/fast models per provider.
    llm_openai_model: str = Field(
        default="gpt-4o-mini", description="OpenAI (direct) smart-tier model"
    )
    llm_openai_fast_model: str = Field(
        default="gpt-4o-mini", description="OpenAI (direct) fast-tier model"
    )
    llm_anthropic_model: str = Field(
        default="claude-3-5-sonnet-20241022",
        description="Anthropic Claude smart-tier model",
    )
    llm_anthropic_fast_model: str = Field(
        default="claude-3-5-haiku-20241022",
        description="Anthropic Claude fast-tier model",
    )
    llm_google_model: str = Field(
        default="gemini-2.0-flash", description="Google Gemini smart-tier model"
    )
    llm_google_fast_model: str = Field(
        default="gemini-2.0-flash", description="Google Gemini fast-tier model"
    )

    # ── Debug & Operational Toggles ──────────────────
    debug: bool = Field(
        default=False, description="Enable debug logging and verbose output"
    )
    demo_mode: bool = Field(
        default=True,
        description="Enable demo mode (uses MockClient, no API calls)",
    )

    # ── Rate Limiting ─────────────────────────────────
    rate_limit_per_session: int = Field(
        default=1, description="Max concurrent requests per session"
    )
    rate_limit_global_per_hour: int = Field(
        default=60, description="Max requests globally per hour"
    )
    # Round-3 review P2: the old limiter was an in-memory dict, so a 3-worker
    # scale-out turned the "60/hour" quota into 180/hour. The backend is now
    # pluggable — "memory" for a single process, "redis" for a shared store.
    rate_limit_backend: str = Field(
        default="memory",
        description="Rate-limit store backend: memory or redis",
    )
    redis_url: str = Field(
        default="", description="redis:// URL used when rate_limit_backend=redis"
    )

    # ── Azure Settings ───────────────────────────────
    azure_subscription_id: str = Field(
        default="", description="Target Azure Subscription ID"
    )
    azure_default_region: str = Field(
        default="uaenorth", description="Default Azure region for deployments"
    )

    # ── Cache Settings ───────────────────────────────
    cache_ttl_hours: int = Field(
        default=24, description="Cache time-to-live in hours"
    )
    cache_max_size_mb: int = Field(
        default=200, description="Maximum cache storage size in MB"
    )

    # ── Observability ─────────────────────────────────
    log_level: str = Field(default="INFO", description="Logging level")
    audit_log_dir: str = Field(
        default="logs", description="Directory for audit log output"
    )
    audit_retention_days: int = Field(
        default=90, description="Audit log retention period in days"
    )

    # ── Security & Validation ─────────────────────────
    max_input_length: int = Field(
        default=5000, description="Maximum allowed input length in characters"
    )
    blocked_patterns: list[str] = Field(
        default_factory=lambda: [
            "<script>",
            "DROP TABLE",
            "DELETE FROM",
            "eval(",
            "exec(",
            "__import__",
        ],
        description="List of suspicious/blocked input patterns",
    )

    # ── Azure AI Content Safety (issue #2, OPTIONAL) ───
    # ML-based harm moderation + Prompt Shields. Off by default; when the
    # endpoint+key are set and content_safety_enabled is true, the regex layer
    # in sanitize.py is backed by Azure's detectors. Missing credentials
    # degrade to "no verdict" — the app never breaks without them (same
    # contract as the live pricing module).
    content_safety_endpoint: str = Field(
        default="", description="Azure AI Content Safety endpoint (empty = feature off)"
    )
    content_safety_api_key: SecretStr = Field(
        default=SecretStr(""), description="Azure AI Content Safety API key"
    )
    content_safety_threshold: int = Field(
        default=4,
        ge=0,
        le=6,
        description="Block severity threshold: 0-6 (4 = Medium and above blocks)",
    )
    content_safety_enabled: bool = Field(
        default=False,
        description="Enable Azure ML content moderation + prompt shields",
    )

    # ── Governance (issue #5, OPTIONAL) ────────────────
    # Every tool call is checked against a declarative policy before it runs
    # (allow / deny / require_approval). Delegates to Microsoft's Agent
    # Governance Toolkit when installed; a mirrored built-in policy keeps the
    # contract identical without it.
    governance_enabled: bool = Field(
        default=True,
        description="Enforce the tool-action policy on every tool call",
    )

    # ── Authentication (Phase 15 scaffold) ──────────────
    # Production deployments must not serve the dashboard to anonymous
    # users. When ``auth_enabled`` is true the dashboard requires a signed-in
    # identity (Microsoft Entra ID via Streamlit's native OIDC login, or App
    # Service Easy Auth in front of the app) before rendering anything.
    # Default off so demo mode and the test suite behave exactly as before.
    auth_enabled: bool = Field(
        default=False,
        description="Require login before the dashboard renders (Entra ID / OIDC)",
    )
    auth_provider: str = Field(
        default="entra_id",
        description="Identity provider: entra_id (Microsoft Entra ID via OIDC)",
    )
    auth_client_id: str = Field(
        default="", description="OIDC application (client) ID"
    )
    auth_client_secret: SecretStr = Field(
        default=SecretStr(""), description="OIDC client secret"
    )
    auth_tenant_id: str = Field(
        default="", description="Entra ID tenant id (or 'common')"
    )
    auth_redirect_uri: str = Field(
        default="",
        description="OIDC redirect URI (the deployed dashboard URL)",
    )

    # ── Tool-calling / MCP (issue #7, OPTIONAL) ────────
    # The tool registry (live pricing, compliance lookup) is always available
    # in-process; mcp_enabled additionally routes calls over the Model Context
    # Protocol via the mcp bridge (needs the optional 'mcp' package).
    tools_enabled: bool = Field(
        default=True, description="Expose the built-in tool registry to the pipeline"
    )
    mcp_enabled: bool = Field(
        default=False,
        description="Route tool calls over MCP (requires the optional 'mcp' package)",
    )

    @field_validator("llm_temperature")
    @classmethod
    def validate_temperature(cls, v: float) -> float:
        """Ensure sampling temperature is between 0.0 and 2.0."""
        if not (0.0 <= v <= 2.0):
            raise ValueError(f"llm_temperature must be between 0.0 and 2.0, got {v}")
        return v

    @field_validator("llm_timeout")
    @classmethod
    def validate_timeout(cls, v: int) -> int:
        """Ensure timeout is positive."""
        if v <= 0:
            raise ValueError(f"llm_timeout must be strictly positive (> 0), got {v}")
        return v

    @field_validator("rate_limit_backend")
    @classmethod
    def validate_rate_limit_backend(cls, v: str) -> str:
        """Only memory and redis are valid rate-limit backends."""
        allowed = {"memory", "redis"}
        if v.lower() not in allowed:
            raise ValueError(
                f"rate_limit_backend must be one of {sorted(allowed)}, got '{v}'"
            )
        return v.lower()

    @field_validator("llm_provider")
    @classmethod
    def validate_provider(cls, v: str) -> str:
        """Ensure LLM provider is one of the supported values."""
        allowed = {"mock", "nvidia", "azure", "openai", "anthropic", "google"}
        if v.lower() not in allowed:
            raise ValueError(f"llm_provider must be one of {sorted(allowed)}, got '{v}'")
        return v.lower()

    @field_validator("routing_providers", mode="before")
    @classmethod
    def parse_routing_providers(cls, v: object) -> object:
        """Accept a comma-separated env string ("nvidia,azure") or a list."""
        if isinstance(v, str):
            return [item.strip() for item in v.split(",") if item.strip()]
        return v

    @field_validator("routing_providers")
    @classmethod
    def validate_routing_providers(cls, v: list[str]) -> list[str]:
        """Ensure every routing provider is one of the supported values."""
        allowed = {"mock", "nvidia", "azure", "openai", "anthropic", "google"}
        cleaned = [p.lower() for p in v]
        unknown = [p for p in cleaned if p not in allowed]
        if unknown:
            raise ValueError(f"routing_providers contains unknown provider(s): {unknown}")
        return cleaned

    def get_sensitive_fields(self) -> dict[str, str]:
        """Return dict of sensitive key names mapped to redacted string placeholders."""
        has_nvidia = bool(self.nvidia_api_key.get_secret_value())
        has_azure = bool(self.azure_openai_api_key.get_secret_value())
        return {
            "nvidia_api_key": "***REDACTED***" if has_nvidia else "",
            "azure_openai_api_key": "***REDACTED***" if has_azure else "",
            "openai_api_key": "***REDACTED***" if self.openai_api_key.get_secret_value() else "",
            "anthropic_api_key": "***REDACTED***"
            if self.anthropic_api_key.get_secret_value()
            else "",
            "google_api_key": "***REDACTED***" if self.google_api_key.get_secret_value() else "",
            "auth_client_secret": "***REDACTED***"
            if self.auth_client_secret.get_secret_value()
            else "",
        }

    def __repr__(self) -> str:
        """Custom repr that masks sensitive API keys.

        Every secret renders as the literal placeholder ``***REDACTED***`` —
        not even the first three characters of a real key are shown. A leaked
        prefix narrows the search space for an attacker reading logs or crash
        reports (an external principal-engineer review finding), so masking is
        all-or-nothing.
        """
        fields: list[str] = []
        for name, value in self.__dict__.items():
            if isinstance(value, SecretStr):
                masked = "***REDACTED***" if value.get_secret_value() else ""
                fields.append(f"{name}='{masked}'")
            else:
                fields.append(f"{name}={value!r}")
        return f"Settings({', '.join(fields)})"

    def __str__(self) -> str:
        """Custom str representation that masks sensitive fields."""
        return repr(self)
