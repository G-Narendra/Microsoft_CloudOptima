"""Tests for LLM client implementations and retry logic."""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

import httpx
import pytest
from pydantic import SecretStr

from cloudoptima.config import Settings
from cloudoptima.llm_client import (
    AzureClient,
    BaseLLMClient,
    MockClient,
    NvidiaClient,
    _strip_control_chars,
    create_llm_client,
    generate_with_retry,
)


# ── MockClient Tests ─────────────────────────────────────────────────────────


def test_mock_client_architect() -> None:
    """MockClient returns valid architect JSON with expected keys."""
    client = MockClient()
    response = client.generate("Design a compute architecture", "You are an architect")
    data = json.loads(response)
    assert "compute" in data
    assert "storage" in data
    assert "networking" in data
    assert "data" in data
    assert "recommendation" in data["compute"]


def test_mock_client_cost() -> None:
    """MockClient returns valid cost analyst JSON with expected keys."""
    client = MockClient()
    response = client.generate("Estimate the monthly cost and budget")
    data = json.loads(response)
    assert "estimate" in data
    assert "breakdown" in data
    assert "budget_status" in data
    assert isinstance(data["estimate"], (int, float))


def test_mock_client_security() -> None:
    """MockClient returns valid security JSON with expected keys."""
    client = MockClient()
    response = client.generate("Analyze security vulnerabilities and risk")
    data = json.loads(response)
    assert "findings" in data
    assert "overall_risk_rating" in data
    assert "recommendations" in data
    assert isinstance(data["findings"], list)


def test_mock_client_compliance() -> None:
    """MockClient returns valid compliance JSON with expected keys."""
    client = MockClient()
    response = client.generate("Check compliance with PDPL regulations")
    data = json.loads(response)
    assert "rules" in data
    assert "overall_status" in data
    assert isinstance(data["rules"], list)


def test_mock_client_judge() -> None:
    """MockClient returns valid judge JSON with expected keys."""
    client = MockClient()
    response = client.generate("Judge the conflicts and arbitrate between agents")
    data = json.loads(response)
    assert "arbitration" in data
    assert "final_recommendation" in data
    assert "overridden_agents" in data


# ── Factory Tests ─────────────────────────────────────────────────────────────


def test_factory_mock() -> None:
    """Factory creates MockClient when provider is 'mock'."""
    settings = Settings(llm_provider="mock")
    client = create_llm_client(settings)
    assert isinstance(client, MockClient)


def test_factory_invalid() -> None:
    """Factory raises ValueError for unknown provider."""
    # Provider validation happens at Settings level, so we patch around it
    settings = Settings(llm_provider="mock")
    object.__setattr__(settings, "llm_provider", "unknown_provider")
    with pytest.raises(ValueError, match="Unknown LLM provider"):
        create_llm_client(settings)


# ── Control Character Stripping ───────────────────────────────────────────────


def test_control_chars_stripped() -> None:
    """Control characters, ANSI codes, and null bytes are stripped."""
    dirty = "Hello\x1b[31m World\x00!\x07\x08End"
    clean = _strip_control_chars(dirty)
    assert clean == "Hello World!End"
    assert "\x1b" not in clean
    assert "\x00" not in clean
    assert "\x07" not in clean


# ── Retry Wrapper Tests ───────────────────────────────────────────────────────


def test_retry_success_on_second_attempt() -> None:
    """Retry wrapper recovers after first failure."""
    mock_client = MagicMock(spec=BaseLLMClient)
    mock_client.generate.side_effect = [
        httpx.TimeoutException("timeout"),
        '{"result": "success"}',
    ]

    result = generate_with_retry(
        mock_client, "test prompt", max_retries=3, base_delay=0.01
    )
    assert result == '{"result": "success"}'
    assert mock_client.generate.call_count == 2


def test_retry_exhausted() -> None:
    """Retry wrapper raises after all attempts fail."""
    mock_client = MagicMock(spec=BaseLLMClient)
    mock_client.generate.side_effect = httpx.TimeoutException("timeout")

    with pytest.raises(httpx.TimeoutException):
        generate_with_retry(
            mock_client, "test prompt", max_retries=3, base_delay=0.01
        )
    assert mock_client.generate.call_count == 3


# ── NvidiaClient Tests ────────────────────────────────────────────────────────


def test_nvidia_client_missing_key() -> None:
    """NvidiaClient raises ValueError when API key is empty."""
    settings = Settings(llm_provider="mock", nvidia_api_key=SecretStr(""))
    with pytest.raises(ValueError, match="nvidia_api_key is required"):
        NvidiaClient(settings)


def test_nvidia_client_generate() -> None:
    """NvidiaClient.generate() sends correct request and returns content."""
    settings = Settings(llm_provider="mock", nvidia_api_key=SecretStr("nvapi-test-key-123"))
    client = NvidiaClient(settings)

    mock_response_data = {
        "choices": [{"message": {"content": '{"result": "nvidia_ok"}'}}]
    }

    with patch("cloudoptima.llm_client.httpx.Client") as mock_httpx:
        mock_http_client = MagicMock()
        mock_httpx.return_value.__enter__ = MagicMock(return_value=mock_http_client)
        mock_httpx.return_value.__exit__ = MagicMock(return_value=False)

        mock_resp = MagicMock()
        mock_resp.json.return_value = mock_response_data
        mock_http_client.post.return_value = mock_resp

        result = client.generate("test prompt", "system prompt")

    assert result == '{"result": "nvidia_ok"}'


def test_nvidia_client_empty_response() -> None:
    """NvidiaClient returns empty string when response content is empty."""
    settings = Settings(llm_provider="mock", nvidia_api_key=SecretStr("nvapi-test-key-123"))
    client = NvidiaClient(settings)

    mock_response_data = {
        "choices": [{"message": {"content": ""}}]
    }

    with patch("cloudoptima.llm_client.httpx.Client") as mock_httpx:
        mock_http_client = MagicMock()
        mock_httpx.return_value.__enter__ = MagicMock(return_value=mock_http_client)
        mock_httpx.return_value.__exit__ = MagicMock(return_value=False)

        mock_resp = MagicMock()
        mock_resp.json.return_value = mock_response_data
        mock_http_client.post.return_value = mock_resp

        result = client.generate("test prompt")

    assert result == ""


# ── AzureClient Tests ─────────────────────────────────────────────────────────


def test_azure_client_missing_key() -> None:
    """AzureClient raises ValueError when API key is empty."""
    settings = Settings(
        llm_provider="mock",
        azure_openai_api_key=SecretStr(""),
        azure_openai_endpoint="https://test.openai.azure.com/",
    )
    with pytest.raises(ValueError, match="azure_openai_api_key is required"):
        AzureClient(settings)


def test_azure_client_missing_endpoint() -> None:
    """AzureClient raises ValueError when endpoint is empty."""
    settings = Settings(
        llm_provider="mock",
        azure_openai_api_key=SecretStr("sk-test-key"),
        azure_openai_endpoint="",
    )
    with pytest.raises(ValueError, match="azure_openai_endpoint is required"):
        AzureClient(settings)


def test_azure_client_generate() -> None:
    """AzureClient.generate() calls openai SDK and returns content."""
    settings = Settings(
        llm_provider="mock",
        azure_openai_api_key=SecretStr("sk-test-key"),
        azure_openai_endpoint="https://test.openai.azure.com/",
    )

    with patch("cloudoptima.llm_client.openai.AzureOpenAI") as mock_openai_cls:
        mock_openai_instance = MagicMock()
        mock_openai_cls.return_value = mock_openai_instance

        # Build mock response
        mock_message = MagicMock()
        mock_message.content = '{"result": "azure_ok"}'
        mock_choice = MagicMock()
        mock_choice.message = mock_message
        mock_completion = MagicMock()
        mock_completion.choices = [mock_choice]
        mock_openai_instance.chat.completions.create.return_value = mock_completion

        client = AzureClient(settings)
        result = client.generate("test prompt", "system prompt")

    assert result == '{"result": "azure_ok"}'


def test_azure_client_empty_response() -> None:
    """AzureClient returns empty string when response content is None."""
    settings = Settings(
        llm_provider="mock",
        azure_openai_api_key=SecretStr("sk-test-key"),
        azure_openai_endpoint="https://test.openai.azure.com/",
    )

    with patch("cloudoptima.llm_client.openai.AzureOpenAI") as mock_openai_cls:
        mock_openai_instance = MagicMock()
        mock_openai_cls.return_value = mock_openai_instance

        mock_message = MagicMock()
        mock_message.content = None
        mock_choice = MagicMock()
        mock_choice.message = mock_message
        mock_completion = MagicMock()
        mock_completion.choices = [mock_choice]
        mock_openai_instance.chat.completions.create.return_value = mock_completion

        client = AzureClient(settings)
        result = client.generate("test prompt")

    assert result == ""


def test_azure_client_no_system_prompt() -> None:
    """AzureClient adds default JSON system prompt when none provided."""
    settings = Settings(
        llm_provider="mock",
        azure_openai_api_key=SecretStr("sk-test-key"),
        azure_openai_endpoint="https://test.openai.azure.com/",
    )

    with patch("cloudoptima.llm_client.openai.AzureOpenAI") as mock_openai_cls:
        mock_openai_instance = MagicMock()
        mock_openai_cls.return_value = mock_openai_instance

        mock_message = MagicMock()
        mock_message.content = '{"result": "default_sys"}'
        mock_choice = MagicMock()
        mock_choice.message = mock_message
        mock_completion = MagicMock()
        mock_completion.choices = [mock_choice]
        mock_openai_instance.chat.completions.create.return_value = mock_completion

        client = AzureClient(settings)
        result = client.generate("test prompt")  # no system_prompt

        # Verify the default system prompt was used
        call_args = mock_openai_instance.chat.completions.create.call_args
        messages = call_args.kwargs.get("messages", call_args[1].get("messages", []))
        system_msgs = [m for m in messages if m["role"] == "system"]
        assert len(system_msgs) == 1
        assert "JSON" in system_msgs[0]["content"]

    assert result == '{"result": "default_sys"}'

