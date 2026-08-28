# ADR 0009: Hybrid Compliance RAG with Full Legal Corpus Ingestion

## Status
Accepted

## Context
Compliance verification requires grounded legal citations across GDPR, HIPAA, ISO-27001, NIST, PCI-DSS, PDPL, and SOC 2, rather than generic LLM memory which is prone to hallucination.

## Decision
- Build a RAG engine (`cloudoptima/compliance/rag.py`) supporting Azure AI Search with vector search (`text-embedding-3-large`) and keyword fallbacks.
- Automate paragraph-based semantic chunking across the entire `corpus/` directory.
- Implement LLM query rewriting before vector retrieval to focus search queries on compliance concepts.
- Strict metadata filtering on framework identifiers to isolate search domains.

## Consequences
- **Positive:** Accurate, verifiable compliance checks anchored in actual regulatory text. 
- **Negative:** Requires vector database infrastructure and embedding generation overhead.
