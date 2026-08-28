# ADR 0005: Custom Deterministic Orchestrator vs. LangChain / Heavy Frameworks

## Status
Accepted & Enforced

## Context
When designing the multi-agent execution pipeline, we evaluated whether to build on top of LangChain/LangGraph, Microsoft Agent Framework (MAF), or a purpose-built custom async orchestrator.

## Drawbacks Identified with LangChain in Initial Prototyping
During the initial development of the CloudOptima prototype, Narendra identified several significant pain points with LangChain:
1. **Opaque Abstractions & Prompt Mutations:** LangChain's internal chains manipulate prompts and wrap outputs with hidden metadata, making it difficult to enforce our zero-trust prompt delimiters and strict Pydantic schema validation.
2. **Brittle Error Propagation:** When an agent in a LangChain chain experiences a malformed response or API rate limit, the chain tends to fail completely rather than isolating the failure to an `error_kind` turn while allowing other agents to proceed.
3. **Dependency Bloat & Version Conflicts:** Heavy dependency trees frequently conflicted with preview versions of enterprise Microsoft SDKs (`azure-ai-contentsafety`, `pyrit`, `agent-governance-toolkit`).
4. **Overhead on Structured Linear DAGs:** Our multi-agent system follows a deterministic workflow (Architect → [Cost, Security, Compliance in parallel] → Judge). Graph engines introduced unnecessary state-machine complexity for a pipeline that is fundamentally a clean async DAG.

Because these issues were already identified, we avoided LangChain entirely in this Microsoft industrial project from the start.

## Decision
We chose to implement a lightweight, fully async, custom orchestrator backed by a `BaseAgent` template method. (See RFC 0001 for the full breakdown).

## Consequences
- **Positive:** Zero framework overhead and instantaneous cold starts. Granular control over prompt injection sanitization. Direct async fan-out via `asyncio.gather`.
- **Negative:** We must manually implement features like tracing and state persistence that frameworks often provide out-of-the-box.
