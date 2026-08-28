# ADR 0001: Semantic Caching for LLM Responses

## Status
Accepted

## Context
Our multi-agent system uses identical or highly similar prompts for repeated tasks. Initially, we used a traditional SHA-256 hash-based cache. However, users often rephrase questions slightly ("What is the cost?" vs "How much does it cost?"), resulting in cache misses, increased API latency (30+ seconds), and unnecessary API costs. We need a way to serve cached responses for semantically identical prompts.

## Decision
We will transition from a hash-based LLM cache to a **Semantic Cache** backed by a Vector Database (Redis with RediSearch/RedisVL or Pinecone). 
- We will compute an embedding for the incoming user prompt.
- We will perform a cosine similarity search against previously cached prompts.
- If a match is found with a similarity score above a strict threshold (e.g., `0.98`), we will return the cached LLM response.
- If no match is found, we call the LLM and asynchronously insert the prompt embedding and the generated response into the vector store.

## Consequences
- **Positive**: Reduces API costs by 30-40% and cuts latency to ~50ms for repeated/similar queries.
- **Negative**: Adds a latency overhead of ~100-200ms on cache misses to compute the embedding. Requires maintaining a vector store alongside the application.
