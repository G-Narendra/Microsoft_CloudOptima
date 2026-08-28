"""Tests for Compliance RAG."""

import sys
from unittest.mock import MagicMock, patch
import pytest

# Mock optional dependencies
mock_chroma = MagicMock()
sys.modules["chromadb"] = mock_chroma
sys.modules["chromadb.config"] = MagicMock()

import cloudoptima.compliance.rag
# Inject into the already-loaded module namespace if it failed to import initially
cloudoptima.compliance.rag.chromadb = mock_chroma
cloudoptima.compliance.rag.ChromaSettings = MagicMock()

from cloudoptima.compliance.rag import (
    ComplianceRAG,
    _KeywordRetriever,
    _ChromaRetriever,
    AZURE_SEARCH_AVAILABLE,
    CHROMA_AVAILABLE
)
from cloudoptima.config import Settings


def test_keyword_retriever():
    """Test the deterministic offline keyword retriever."""
    docs = [
        ("doc1", "fw1", "This is a compliance rule about passwords."),
        ("doc2", "fw2", "This rule is about data residency and encryption."),
        ("doc3", "fw1", "Another rule covering backups and recovery."),
    ]
    
    retriever = _KeywordRetriever(docs)
    
    # Query matching doc1 (exact word match for BM25)
    results = retriever.query("passwords compliance", top_k=2)
    assert len(results) >= 1
    assert results[0][0] == "doc1"
    
    # Query with framework filter
    results = retriever.query("rule", framework="fw2")
    assert len(results) == 1
    assert results[0][0] == "doc2"
    
    # Empty query
    assert retriever.query("") == []


def test_chroma_retriever():
    """Test the ChromaDB retriever logic."""
    docs = [
        ("doc1", "fw1", "Data residency in KSA"),
        ("doc2", "fw1", "Consent must be explicit"),
    ]
    
    # The mocked chromadb will be used inside _ChromaRetriever
    retriever = _ChromaRetriever(docs)
    
    # Verify client and collection created
    assert mock_chroma.PersistentClient.called
    
    # Mock the query response
    mock_collection = retriever.collection
    mock_collection.query.return_value = {
        "ids": [["doc1"]],
        "documents": [["Data residency in KSA"]]
    }
    
    results = retriever.query("KSA residency", top_k=1)
    assert len(results) == 1
    assert results[0][0] == "doc1"
    assert results[0][1] == "Data residency in KSA"
    
    mock_collection.query.assert_called_with(
        query_texts=["KSA residency"],
        n_results=1,
        where=None
    )


def test_compliance_rag_semantic_chunking():
    """Test the semantic chunking functionality of ComplianceRAG."""
    settings = Settings()
    rag = ComplianceRAG(settings)
    
    docs = [
        ("doc1", "fw1", "Paragraph 1\n\nParagraph 2\n\nParagraph 3")
    ]
    
    # Small max_len to force splitting on every paragraph
    chunked = rag._semantic_chunk(docs, max_len=10)
    
    assert len(chunked) == 3
    assert chunked[0][0] == "doc1-0"
    assert chunked[1][0] == "doc1-1"
    assert chunked[2][0] == "doc1-2"
    
    # Check text
    assert chunked[0][2] == "Paragraph 1"
    assert chunked[1][2] == "Paragraph 2"


def test_compliance_rag_query():
    """Test the main query_rag method using keyword fallback."""
    settings = Settings()
    rag = ComplianceRAG(settings)
    
    # Force keyword backend for testing the query_rag flow
    rag.backend = "keyword"
    rag.seed_docs([("doc1", "hipaa", "HIPAA BAA agreement required")])
    
    results = rag.query_rag("HIPAA BAA", top_k=1)
    assert len(results) == 1
    assert "BAA" in results[0]


def test_compliance_rag_query_invalid():
    """Test query_rag with invalid inputs."""
    settings = Settings()
    rag = ComplianceRAG(settings)
    
    with pytest.raises(ValueError):
        rag.query_rag("test", top_k=0)
        
    assert rag.query_rag("   ") == []

@patch("cloudoptima.compliance.rag.VectorizedQuery", MagicMock())
def test_azure_search_seed_and_query():
    """Test Azure Search backend logic."""
    settings = Settings()
    rag = ComplianceRAG(settings)
    rag.backend = "azure-search"
    
    # Mock clients
    mock_search = MagicMock()
    mock_oai = MagicMock()
    rag._search_client = mock_search
    rag._oai_client = mock_oai
    
    # Mock embeddings
    mock_response = MagicMock()
    mock_response.data = [MagicMock(embedding=[0.1, 0.2, 0.3])]
    mock_oai.embeddings.create.return_value = mock_response
    
    # Seed
    docs = [("azure-1", "fw1", "azure text")]
    count = rag.seed_docs(docs)
    assert count == 1 # 1 extra

    assert mock_search.upload_documents.called
    
    # Query
    mock_search.search.return_value = [{"text": "azure text"}]
    results = rag.query_rag("test query")
    assert len(results) == 1
    assert results[0] == "azure text"
    
    # Query exception fallback
    mock_search.search.side_effect = Exception("azure error")
    assert rag.query_rag("test") == []

def test_hybrid_query():
    """Test Hybrid backend logic."""
    settings = Settings()
    rag = ComplianceRAG(settings)
    rag.backend = "hybrid"
    
    mock_chroma = MagicMock()
    mock_chroma.query.return_value = [("doc2", "chroma text")]
    rag._chroma = mock_chroma
    
    mock_keyword = MagicMock()
    mock_keyword.query.return_value = [("doc1", "keyword text")]
    rag._keyword = mock_keyword
    
    results = rag.query_rag("hybrid test", top_k=2)
    assert len(results) == 2
    assert "keyword text" in results
    assert "chroma text" in results

