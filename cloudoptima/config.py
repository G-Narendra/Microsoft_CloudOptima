"""Configuration module for CloudOptima.

Provides type-safe application settings loaded from environment variables
and .env files with security redaction for sensitive fields.
"""

from __future__ import annotations

from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


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
        default="mock", description="LLM provider: mock, nvidia, azure"
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

    @field_validator("llm_provider")
    @classmethod
    def validate_provider(cls, v: str) -> str:
        """Ensure LLM provider is one of the supported values."""
        allowed = {"mock", "nvidia", "azure"}
        if v.lower() not in allowed:
            raise ValueError(f"llm_provider must be one of {allowed}, got '{v}'")
        return v.lower()

    def get_sensitive_fields(self) -> dict[str, str]:
        """Return dict of sensitive key names mapped to redacted string placeholders."""
        has_nvidia = bool(self.nvidia_api_key.get_secret_value())
        has_azure = bool(self.azure_openai_api_key.get_secret_value())
        return {
            "nvidia_api_key": "***REDACTED***" if has_nvidia else "",
            "azure_openai_api_key": "***REDACTED***" if has_azure else "",
        }

    def __repr__(self) -> str:
        """Custom repr that masks sensitive API keys."""
        fields: list[str] = []
        for name, value in self.__dict__.items():
            if isinstance(value, SecretStr):
                secret = value.get_secret_value()
                masked = f"{secret[:3]}***" if len(secret) > 3 else "***"
                fields.append(f"{name}='{masked}'")
            else:
                fields.append(f"{name}={value!r}")
        return f"Settings({', '.join(fields)})"

    def __str__(self) -> str:
        """Custom str representation that masks sensitive fields."""
        return repr(self)
