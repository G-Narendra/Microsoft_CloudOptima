# ADR 0007: Multi-Provider LLM Router with Cost-Aware Failover

## Status
Accepted

## Context
Relying on a single LLM vendor creates single-point-of-failure risks, vendor lock-in, and unpredictable API cost spikes.

## Decision
Implement a provider-agnostic router (`cloudoptima/llm_routing.py`) supporting:
- Azure OpenAI, OpenAI (direct), Anthropic Claude, Google Gemini, and Nvidia NIM.
- Price-tier routing: assigning high-reasoning models (GPT-4o, Claude 3.5 Sonnet) to Architect/Judge, and fast models (GPT-4o-mini, Gemini Flash) to Cost/Security/Compliance.
- Automated health demotion and failover on HTTP 429 (rate limits) or 5xx errors.
- Budget spend guard and token usage tracking per session.

## Consequences
- **Positive:** High resilience against outages. Optimal cost efficiency per run.
- **Negative:** Increased complexity in maintaining multiple client libraries and normalizing request/response formats.
