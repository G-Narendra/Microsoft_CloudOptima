"""Tests for Redis LLM caches."""

import gzip
import json
import sys
from unittest.mock import MagicMock, patch

# Mock redis module before importing anything that might use it
mock_redis_module = MagicMock()
sys.modules["redis"] = mock_redis_module

from cloudoptima.llm_cache import RedisLLMCache, SemanticRedisLLMCache


@patch("redis.from_url")
def test_redis_llm_cache_put_and_get(mock_from_url):
    """Test standard Redis cache putting and getting."""
    mock_redis = MagicMock()
    mock_from_url.return_value = mock_redis
    
    cache = RedisLLMCache("redis://localhost:6379", ttl_hours=1)
    
    # Put
    response = '{"message": "success"}'
    cache.put("prompt", "system", "model", 0.1, response)
    
    # Assert Redis SET was called with compressed data
    assert mock_redis.set.called
    args, kwargs = mock_redis.set.call_args
    assert kwargs.get("ex") == 3600
    assert gzip.decompress(args[1]).decode("utf-8") == response

    # Get
    mock_redis.get.return_value = gzip.compress(response.encode("utf-8"))
    result = cache.get("prompt", "system", "model", 0.1)
    assert result == response
    assert cache.stats()["hits"] == 1


@patch("redis.from_url")
def test_redis_llm_cache_miss_and_error(mock_from_url):
    """Test cache miss and fault tolerance in Redis cache."""
    mock_redis = MagicMock()
    mock_from_url.return_value = mock_redis
    
    cache = RedisLLMCache("redis://localhost:6379")
    
    # Get miss
    mock_redis.get.return_value = None
    assert cache.get("prompt", "sys", "mod", 0.0) is None
    assert cache.stats()["misses"] == 1
    
    # Exception handling
    mock_redis.get.side_effect = Exception("Connection lost")
    assert cache.get("prompt", "sys", "mod", 0.0) is None
    assert cache.stats()["errors"] == 1


@patch("redis.from_url")
def test_redis_llm_cache_clear(mock_from_url):
    """Test clearing the Redis cache."""
    mock_redis = MagicMock()
    mock_from_url.return_value = mock_redis
    
    mock_redis.scan_iter.return_value = ["llmcache:1", "llmcache:2"]
    
    cache = RedisLLMCache("redis://localhost")
    cache.clear()
    
    assert mock_redis.delete.call_count == 2


@patch("redis.from_url")
def test_semantic_redis_cache_exact_hit(mock_from_url):
    """Test exact hit in semantic redis cache."""
    mock_redis = MagicMock()
    mock_from_url.return_value = mock_redis
    
    cache = SemanticRedisLLMCache("redis://localhost")
    response = '{"exact": "match"}'
    mock_redis.get.return_value = gzip.compress(response.encode("utf-8"))
    
    result = cache.get("prompt", "sys", "mod", 0.1)
    assert result == response
    assert cache.stats()["hits"] == 1


@patch("redis.from_url")
def test_semantic_redis_cache_semantic_hit(mock_from_url):
    """Test semantic fallback hit in semantic redis cache."""
    mock_redis = MagicMock()
    mock_from_url.return_value = mock_redis
    
    cache = SemanticRedisLLMCache("redis://localhost")
    
    # Force exact cache to miss
    mock_redis.get.return_value = None
    
    # Mock FT.SEARCH result
    response = '{"semantic": "match"}'
    compressed_resp = gzip.compress(response.encode("utf-8"))
    
    # FT.SEARCH returns [num_results, key1, [field1, val1, ...]]
    mock_redis.execute_command.return_value = [
        1,
        "key1",
        [b"score", b"0.01", b"response", compressed_resp]
    ]
    
    result = cache.get("prompt", "sys", "mod", 0.1)
    assert result == response
    assert cache.stats()["hits"] == 1


@patch("redis.from_url")
def test_semantic_redis_cache_put(mock_from_url):
    """Test putting semantic data in redis."""
    mock_redis = MagicMock()
    mock_from_url.return_value = mock_redis
    
    cache = SemanticRedisLLMCache("redis://localhost")
    cache.put("prompt", "sys", "mod", 0.1, '{"answer": "yes"}')
    
    assert mock_redis.set.called
    assert mock_redis.hset.called
    assert mock_redis.expire.called
