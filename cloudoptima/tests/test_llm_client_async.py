"""Async tests for LLM clients."""

import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from cloudoptima.config import Settings
from cloudoptima.llm_client import (
    AzureClient, OpenAIClient, AnthropicClient, GoogleClient, MockClient
)
from pydantic import SecretStr

@pytest.mark.asyncio
async def test_mock_agenerate():
    client = MockClient()
    result = ""
    async for chunk in client.agenerate("prompt", "system"):
        result += chunk
    assert len(result) > 0

@pytest.mark.asyncio
async def test_azure_agenerate():
    settings = Settings(llm_provider="mock", azure_openai_api_key=SecretStr("sk-test"), azure_openai_endpoint="https://test.openai.azure.com/")
    with patch("cloudoptima.llm_client.openai.AsyncAzureOpenAI") as mock_openai_cls:
        mock_instance = MagicMock()
        mock_openai_cls.return_value = mock_instance
        
        async def mock_stream():
            mock_delta = MagicMock()
            mock_delta.content = '{"result": "async_azure"}'
            mock_choice = MagicMock()
            mock_choice.delta = mock_delta
            mock_chunk = MagicMock()
            mock_chunk.choices = [mock_choice]
            yield mock_chunk
            
        mock_instance.chat.completions.create = AsyncMock(return_value=mock_stream())
        
        client = AzureClient(settings)
        result = ""
        async for chunk in client.agenerate("prompt", "system"):
            result += chunk
        assert result == '{"result": "async_azure"}'

@pytest.mark.asyncio
async def test_openai_agenerate():
    settings = Settings(llm_provider="mock", openai_api_key=SecretStr("sk-test"))
    with patch("cloudoptima.llm_client.openai.AsyncOpenAI") as mock_openai_cls:
        mock_instance = MagicMock()
        mock_openai_cls.return_value = mock_instance
        
        async def mock_stream():
            mock_delta = MagicMock()
            mock_delta.content = '{"result": "async_openai"}'
            mock_choice = MagicMock()
            mock_choice.delta = mock_delta
            mock_chunk = MagicMock()
            mock_chunk.choices = [mock_choice]
            yield mock_chunk
            
        mock_instance.chat.completions.create = AsyncMock(return_value=mock_stream())
        
        client = OpenAIClient(settings)
        result = ""
        async for chunk in client.agenerate("prompt", "system"):
            result += chunk
        assert result == '{"result": "async_openai"}'

@pytest.mark.asyncio
async def test_anthropic_agenerate():
    settings = Settings(llm_provider="mock", anthropic_api_key=SecretStr("sk-ant"))
    with patch("cloudoptima.llm_client.httpx.AsyncClient") as mock_httpx:
        mock_client = MagicMock()
        mock_httpx.return_value.__aenter__.return_value = mock_client
        
        mock_resp = MagicMock()
        mock_resp.json.return_value = {
            "content": [{"type": "text", "text": '{"result": "async_ant"}'}],
            "usage": {"input_tokens": 10, "output_tokens": 10}
        }
        
        async def mock_post(*args, **kwargs):
            return mock_resp
            
        mock_client.post = mock_post
        
        client = AnthropicClient(settings)
        result = ""
        async for chunk in client.agenerate("prompt", "system"):
            result += chunk
        assert result == '{"result": "async_ant"}'

@pytest.mark.asyncio
async def test_google_agenerate():
    settings = Settings(llm_provider="mock", google_api_key=SecretStr("AI-google"))
    with patch("cloudoptima.llm_client.httpx.AsyncClient") as mock_httpx:
        mock_client = MagicMock()
        mock_httpx.return_value.__aenter__.return_value = mock_client
        
        mock_resp = MagicMock()
        mock_resp.json.return_value = {
            "candidates": [{"content": {"parts": [{"text": '{"result": "async_google"}'}]}}],
            "usageMetadata": {"totalTokenCount": 20}
        }
        
        async def mock_post(*args, **kwargs):
            return mock_resp
            
        mock_client.post = mock_post
        
        client = GoogleClient(settings)
        result = ""
        async for chunk in client.agenerate("prompt", "system"):
            result += chunk
        assert result == '{"result": "async_google"}'

def test_anthropic_extract_empty():
    settings = Settings(llm_provider="mock", anthropic_api_key=SecretStr("sk-ant"))
    client = AnthropicClient(settings)
    assert client._extract_content({}) == ""
    assert client._extract_content({"content": []}) == ""
    assert client._extract_content({"content": [{"text": ""}]}) == ""

def test_google_extract_empty():
    settings = Settings(llm_provider="mock", google_api_key=SecretStr("AI-google"))
    client = GoogleClient(settings)
    assert client._extract_text({}) == ""
    assert client._extract_text({"candidates": []}) == ""
    assert client._extract_text({"candidates": [{"content": {}}]}) == ""
