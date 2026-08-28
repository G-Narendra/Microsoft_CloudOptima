"""Type-safe application settings with automatic secret redaction."""

from __future__ import annotations

from typing import Annotated

from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict

try:
    from azure.identity import DefaultAzureCredential
    from azure.keyvault.secrets import SecretClient
    HAS_AZURE_IDENTITY = True
except ImportError:
    HAS_AZURE_IDENTITY = False


class Settings(BaseSettings):
    """Application settings loaded from environment and .env files."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # LLM Provider & API Keys
    llm_provider: str = Field(
        default="mock",
        description="LLM provider: mock, azure, openai, anthropic, google, nvidia",
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
    openai_api_key: SecretStr = Field(
        default=SecretStr(""), description="OpenAI API key"
    )
    anthropic_api_key: SecretStr = Field(
        default=SecretStr(""), description="Anthropic Claude API key"
    )
    google_api_key: SecretStr = Field(
        default=SecretStr(""), description="Google Gemini API key"
    )
    nvidia_api_key: SecretStr = Field(
        default=SecretStr(""), description="Nvidia NIM API key"
    )

    # Model Settings
    llm_model: str = Field(
        default="gpt-4o-mini", description="Primary model name"
    )
    llm_temperature: float = Field(
        default=0.1, description="Model sampling temperature (0.0 - 2.0)"
    )
    llm_timeout: int = Field(
        default=30, description="Model request timeout in seconds"
    )

    # Cost-aware LLM routing
    routing_enabled: bool = Field(
        default=False,
        description="Route calls across providers cheapest-first with failover",
    )
    routing_providers: Annotated[list[str], NoDecode] = Field(
        default_factory=lambda: ["openai", "azure", "anthropic", "google"],
        description="Providers eligible for routing",
    )
    routing_max_cost_per_request: float = Field(
        default=0.005,
        description="Soft USD cap on estimated input cost before a provider is skipped",
    )
    routing_timeout: float = Field(
        default=10.0,
        gt=0.0,
        description="Per-provider timeout in seconds for routed clients",
    )
    llm_azure_model: str = Field(
        default="gpt-4o-mini", description="Azure OpenAI smart-tier model"
    )
    llm_azure_fast_model: str = Field(
        default="gpt-4o-mini", description="Azure OpenAI fast-tier model"
    )
    llm_openai_model: str = Field(
        default="gpt-4o-mini", description="OpenAI smart-tier model"
    )
    llm_openai_fast_model: str = Field(
        default="gpt-4o-mini", description="OpenAI fast-tier model"
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
    llm_nvidia_model: str = Field(
        default="meta/llama-3.3-70b-instruct", description="Nvidia NIM smart-tier model"
    )
    llm_nvidia_fast_model: str = Field(
        default="meta/llama-3.1-8b-instruct", description="Nvidia NIM fast-tier model"
    )

    # Operational toggles
    debug: bool = Field(
        default=False, description="Enable debug logging"
    )
    demo_mode: bool = Field(
        default=True,
        description="Enable demo mode (uses MockClient)",
    )

    # Rate Limiting
    rate_limit_per_session: int = Field(
        default=1, description="Max concurrent requests per session"
    )
    rate_limit_global_per_hour: int = Field(
        default=60, description="Max requests globally per hour"
    )
    rate_limit_backend: str = Field(
        default="memory",
        description="Rate-limit store backend: memory or redis",
    )
    redis_url: str = Field(
        default="", description="redis:// URL used when rate_limit_backend=redis"
    )

    # Azure Settings
    azure_subscription_id: str = Field(
        default="", description="Target Azure Subscription ID"
    )
    azure_default_region: str = Field(
        default="uaenorth", description="Default Azure region for deployments"
    )
    azure_keyvault_url: str = Field(
        default="", description="Azure Key Vault URL for secret resolution"
    )
    azure_search_endpoint: str = Field(
        default="", description="Azure AI Search endpoint URL"
    )
    azure_search_api_key: SecretStr = Field(
        default=SecretStr(""), description="Azure AI Search API key"
    )
    azure_search_index_name: str = Field(
        default="compliance-docs", description="Azure AI Search index name"
    )
    azure_openai_embedding_deployment: str = Field(
        default="text-embedding-3-large", description="Azure OpenAI embedding deployment name"
    )

    # Cache Settings
    cache_ttl_hours: int = Field(
        default=24, description="Cache time-to-live in hours"
    )
    cache_max_size_mb: int = Field(
        default=200, description="Maximum cache storage size in MB"
    )

    # Observability
    log_level: str = Field(default="INFO", description="Logging level")
    audit_log_dir: str = Field(
        default="logs", description="Directory for audit log output"
    )
    audit_retention_days: int = Field(
        default=90, description="Audit log retention period in days"
    )

    # Security & Validation
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

    # Azure AI Content Safety
    content_safety_endpoint: str = Field(
        default="", description="Azure AI Content Safety endpoint"
    )
    content_safety_api_key: SecretStr = Field(
        default=SecretStr(""), description="Azure AI Content Safety API key"
    )
    content_safety_threshold: int = Field(
        default=4,
        ge=0,
        le=6,
        description="Block severity threshold: 0-6",
    )
    content_safety_enabled: bool = Field(
        default=False,
        description="Enable Azure ML content moderation and prompt shields",
    )

    # Governance
    governance_enabled: bool = Field(
        default=True,
        description="Enforce tool action policy on tool execution",
    )

    # Authentication
    auth_enabled: bool = Field(
        default=False,
        description="Require login before dashboard renders",
    )
    auth_provider: str = Field(
        default="entra_id",
        description="Identity provider name",
    )
    auth_client_id: str = Field(
        default="", description="OIDC application client ID"
    )
    auth_client_secret: SecretStr = Field(
        default=SecretStr(""), description="OIDC client secret"
    )
    auth_tenant_id: str = Field(
        default="", description="Entra ID tenant ID"
    )
    auth_redirect_uri: str = Field(
        default="",
        description="OIDC redirect URI",
    )

    # Tools and MCP
    tools_enabled: bool = Field(
        default=True, description="Expose built-in tool registry to pipeline"
    )
    mcp_enabled: bool = Field(
        default=False,
        description="Route tool calls over MCP",
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
        """Validate rate-limit store backend name."""
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
        """Accept comma-separated string or list."""
        if isinstance(v, str):
            return [item.strip() for item in v.split(",") if item.strip()]
        return v

    @field_validator("routing_providers")
    @classmethod
    def validate_routing_providers(cls, v: list[str]) -> list[str]:
        """Ensure all routing providers are supported."""
        allowed = {"mock", "nvidia", "azure", "openai", "anthropic", "google"}
        cleaned = [p.lower() for p in v]
        unknown = [p for p in cleaned if p not in allowed]
        if unknown:
            raise ValueError(f"routing_providers contains unknown provider(s): {unknown}")
        return cleaned

    def model_post_init(self, __context: object) -> None:
        """Resolve missing secrets from Azure Key Vault if configured."""
        if not self.azure_keyvault_url or not HAS_AZURE_IDENTITY:
            return

        try:
            credential = DefaultAzureCredential()
            client = SecretClient(vault_url=self.azure_keyvault_url, credential=credential)
        except Exception:
            return

        secret_fields = [
            "nvidia_api_key",
            "azure_openai_api_key",
            "openai_api_key",
            "anthropic_api_key",
            "google_api_key",
            "content_safety_api_key",
            "auth_client_secret",
            "azure_search_api_key",
        ]

        for field_name in secret_fields:
            val = getattr(self, field_name)
            if not val or not val.get_secret_value():
                kv_secret_name = field_name.replace("_", "-")
                try:
                    secret_val = client.get_secret(kv_secret_name).value
                    if secret_val:
                        setattr(self, field_name, SecretStr(secret_val))
                except Exception:
                    pass

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
            "azure_search_api_key": "***REDACTED***"
            if self.azure_search_api_key.get_secret_value()
            else "",
        }

    def __repr__(self) -> str:
        """Mask sensitive API keys in repr."""
        fields: list[str] = []
        for name, value in self.__dict__.items():
            if isinstance(value, SecretStr):
                masked = "***REDACTED***" if value.get_secret_value() else ""
                fields.append(f"{name}='{masked}'")
            else:
                fields.append(f"{name}={value!r}")
        return f"Settings({', '.join(fields)})"

    def __str__(self) -> str:
        """Mask sensitive fields in str."""
        return repr(self)
