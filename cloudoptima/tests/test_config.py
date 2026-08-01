"""Tests for Settings configuration module."""

from __future__ import annotations

import pytest
from pydantic import ValidationError, SecretStr

from cloudoptima.config import Settings


def test_defaults_load() -> None:
    """Test that Settings loads with expected default values."""
    settings = Settings()
    assert settings.demo_mode is True
    assert settings.llm_provider == "mock"
    assert settings.llm_model == "gpt-4o-mini"
    assert settings.llm_temperature == 0.1
    assert settings.llm_timeout == 30
    assert settings.rate_limit_per_session == 1
    assert settings.cache_ttl_hours == 24
    assert settings.max_input_length == 5000


def test_env_override(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that env vars override default values."""
    monkeypatch.setenv("LLM_MODEL", "gpt-4-turbo")
    monkeypatch.setenv("LLM_TEMPERATURE", "0.7")
    monkeypatch.setenv("DEMO_MODE", "false")

    settings = Settings()
    assert settings.llm_model == "gpt-4-turbo"
    assert settings.llm_temperature == 0.7
    assert settings.demo_mode is False


def test_api_key_masked_in_repr() -> None:
    """Test that secret API keys are never leaked in repr()."""
    raw_key = "sk-nvidia-secret-key-12345"
    settings = Settings(nvidia_api_key=SecretStr(raw_key))
    repr_str = repr(settings)

    assert raw_key not in repr_str
    assert "nvidia_api_key=" in repr_str
    assert "sk-***" in repr_str or "***" in repr_str


def test_api_key_masked_in_str() -> None:
    """Test that secret API keys are never leaked in str()."""
    raw_key = "sk-azure-secret-key-67890"
    settings = Settings(azure_openai_api_key=SecretStr(raw_key))
    str_out = str(settings)

    assert raw_key not in str_out
    assert "azure_openai_api_key=" in str_out


def test_temperature_bounds() -> None:
    """Test that temperature outside [0.0, 2.0] raises ValidationError."""
    with pytest.raises(ValidationError):
        Settings(llm_temperature=2.5)

    with pytest.raises(ValidationError):
        Settings(llm_temperature=-0.5)


def test_timeout_positive() -> None:
    """Test that timeout <= 0 raises ValidationError."""
    with pytest.raises(ValidationError):
        Settings(llm_timeout=0)

    with pytest.raises(ValidationError):
        Settings(llm_timeout=-10)


def test_invalid_provider() -> None:
    """Test that invalid provider raises ValidationError."""
    with pytest.raises(ValidationError):
        Settings(llm_provider="unsupported_provider")
