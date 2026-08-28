# RFC 0001 — Custom Async Orchestrator vs. Microsoft Agent Framework / LangGraph / LangChain

- **Status:** Accepted — Maintain purpose-built custom orchestrator; revisit upon Azure AI Foundry Agent Service deployment
- **Date:** August 2026
- **Decision Owners:** CloudOptima Engineering Team (Narendra, Andrew, Ivan)
- **Collaborating Microsoft Team:** Punit Shah (Issue #6)
- **Related Implementation:** `cloudoptima/orchestrator.py`, `cloudoptima/agents/agent_base.py`, `docs/adr/`

---

## 1. Executive Summary

CloudOptima executes a deterministic five-agent evaluation workflow:
`Architect → [Cost Analyst, Security Engineer, Compliance Officer in parallel] → Judge`

This RFC documents the formal evaluation between building on top of existing agent frameworks (Microsoft Agent Framework, LangGraph, LangChain) versus a purpose-built custom async orchestrator. We chose to **maintain our custom async orchestrator** for local and containerized deployments, establishing explicit criteria for when to adopt Microsoft Agent Framework (MAF) in cloud environments.

---

## 2. Context & Requirements

- **Deterministic Pipeline Structure:** The pipeline is a deterministic Directed Acyclic Graph (DAG) with one fan-out step and a final arbitration step. It does not require dynamic open-ended agent handoffs or nondeterministic conversational loops.
- **Zero-Trust Input & Schema Control:** Every agent must operate on strictly validated Pydantic v2 schemas (`extra="forbid"`), surrounded by prompt injection delimiters, and fail gracefully with structured `error_kind` turns.
- **High Concurrency & Low Latency:** The system must support asynchronous I/O (`asyncio.gather`) to allow parallel specialist analysis without thread starvation.
- **Enterprise Microsoft Tooling Interoperability:** The orchestrator must interface natively with Azure AI Content Safety, Agent Governance Toolkit (AGT), Model Context Protocol (MCP), and Azure AI Search without framework impedance.

---

## 3. Options Compared

| Evaluation Criterion | Custom Async Orchestrator (Chosen) | Microsoft Agent Framework (MAF) | LangGraph | LangChain |
|---|---|---|---|---|
| **Determinism & Order** | ✅ Strict deterministic DAG | ✅ Deterministic `WorkflowBuilder` | ✅ Deterministic `StateGraph` | ⚠️ Mutable chain state |
| **Concurrency & Speed** | ✅ Native coroutines + `asyncio.gather` (~0.5s warm) | ✅ Async execution model | ⚠️ Graph state machine overhead | ❌ High overhead on linear DAGs |
| **Zero-Trust Sanitization** | ✅ Fully owned prompt boundaries | ✅ Clean participant hooks | ⚠️ Opaque state wrappers | ❌ Hidden prompt formatting & wrappers |
| **Dependency Footprint** | ✅ Zero external orchestration deps | ⚠️ Emerging preview SDK | ⚠️ `langgraph` dependency graph | ❌ Heavy, volatile dependency tree |
| **Azure AI Foundry Alignment** | 🟡 Provider-agnostic router | ✅ Direct native integration | 🟡 Generic cloud support | 🟡 Generic cloud support |
| **Verdict** | **Accepted** | **Strong Cloud Alternative** | **Rejected (Overkill)** | **Rejected (Identified Drawbacks)** |

---

## 4. Why We Avoided LangChain: Findings from Architecture Prototyping

During the initial architectural prototyping phase of CloudOptima, several critical drawbacks of generic agent frameworks like LangChain were directly evaluated:

1. **Opaque Abstraction Layers & Prompt Mutations:**  
   LangChain's internal abstractions frequently inject hidden system prompts, format instructions, and wrappers. This directly interfered with the strict security requirements of sanitizing every user token and preventing prompt leakage.
2. **Brittle Error Handling & State Bleed:**  
   When an LLM failed to produce valid JSON or hit a rate limit, LangChain's chains often raised uncatchable exceptions that crashed the entire pipeline. In contrast, the custom `BaseAgent` wraps failures into structured `AgentTurn` objects with an explicit `error_kind` taxonomy (`llm`, `parse`, `validation`, `prompt_build`), allowing unaffected agents to finish their analysis.
3. **Heavy Dependency Chain & Version Instability:**  
   LangChain's extensive dependency graph caused frequent version pinning conflicts with preview enterprise SDKs.
4. **Unnecessary State Complexity on Structured Pipelines:**  
   For a structured 5-agent pipeline with deterministic 6-pair conflict analysis, LangChain's generic agents added indirection without delivering any capability that couldn't be implemented in clean, testable async Python code.

Because these fundamental trade-offs were identified early, the team deliberately avoided LangChain and adopted the purpose-built custom async orchestrator **from the very beginning** of this Microsoft industrial project.

---

## 5. Why Microsoft Agent Framework (MAF) is the Future Cloud Path

Microsoft Agent Framework (the evolution of AutoGen and Semantic Kernel) is the strongest enterprise alternative. MAF represents our pipeline cleanly via `SequentialBuilder` and integrates with Azure AI Foundry via `FoundryChatClient`.

We chose not to adopt MAF immediately for local development because its primary advantages (managed cloud state, hosted threads, agent pools in Foundry) are realized when deployed in Azure AI Foundry Agent Service.

---

## 6. Revisit Triggers

This architectural decision will be formally reopened when:
1. **Azure AI Foundry Agent Service Hosting:** CloudOptima is deployed to managed Azure AI Foundry infrastructure.
2. **Dynamic Multi-Turn Handoffs:** The business workflow requires open-ended conversational routing between agents.
3. **External Agent Toolboxes:** The system transitions from in-house FastMCP tools to cloud-hosted Foundry Toolboxes.
