# ADR 0004: RAG Hybrid Search with Cross-Encoder

## Status
Accepted

## Context
Our compliance agent relies on RAG to fetch accurate regulatory clauses (GDPR, SOC2, etc.). The current implementation uses a naive implementation of either purely dense (cosine similarity) or purely sparse (keyword overlap) search, leading to poor recall on exact phrasing and entity names. 

## Decision
We will implement **Hybrid Search** with a **Cross-Encoder Re-ranker**.
- We will retrieve `N` candidates using dense vector search (via an optimized embedding model like `text-embedding-3-small` or domain-specific models).
- We will retrieve `N` candidates using a sparse BM25 index to capture exact keyword matches (e.g., "Article 17").
- We will merge and deduplicate the candidates to form a candidate pool.
- A Cross-Encoder model (e.g., Cohere Rerank or MS-MARCO) will score the candidate pool against the query and re-rank the final `top_k` results for prompt injection.

## Consequences
- **Positive**: Substantially improves recall and precision, especially for legal clauses requiring exact keyword hits along with semantic context.
- **Negative**: Increases search latency and compute cost due to the Cross-Encoder step. Requires maintaining dual indices (Vector and BM25).
