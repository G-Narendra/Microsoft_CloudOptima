# RFC 0001 — Custom Orchestrator vs Microsoft Agent Framework / LangGraph / LangChain

- **Status:** Accepted — keep the custom orchestrator for the current phase; revisit at deployment
- **Date:** Aug 2026
- **Decision owners:** Narendra, Andrew, Ivan
- **Reviewer:** Punit Shah (Microsoft) — raised as issue #6
- **Related files:** `cloudoptima/orchestrator.py`, `cloudoptima/agent_base.py`,
  `docs/DECISIONS.md`

## 1. Summary

CloudOptima runs a fixed five-agent pipeline (Architect → Cost Analyst → Security →
Compliance → Judge) with deterministic conflict detection and judge arbitration.
We evaluated four ways to build that orchestration and chose to **keep our custom
orchestrator** for the current phase. We will **revisit this decision at deployment**,
because hosting agents in Azure AI Foundry Agent Service changes the math in favour of
the Microsoft Agent Framework (MAF).

## 2. Context

- The pipeline is a **fixed linear DAG** with one arbitration step — not a dynamic
  graph. There is no branching, no retry-on-condition, no runtime topology change.
- Every agent returns **schema-validated structured JSON**; correctness is enforced by
  tests (478 tests, 93% coverage), not by framework features.
- The project is a learning exercise: understanding every layer is a goal in itself.
- Constraints: minimal dependency footprint, deterministic execution, failure
  isolation (one failing agent must not crash the pipeline), and a clean audit trail.

## 3. Decision criteria (and why they matter here)

| Criterion | Why | Weight |
|---|---|---|
| Determinism | Same input ⇒ same pipeline order, same conflicts | High |
| Testability | Schema validation + conflict detection must be unit-testable | High |
| Transparency | The team must understand every step (learning project) | High |
| Dependency weight | Fewer moving parts = fewer breaking upgrades | Medium |
| Azure alignment | We deploy on Azure; the stack should not fight that | Medium |
| Ecosystem | Access to prebuilt tools/agents from a framework | Low (we need none today) |

## 4. Options compared

| Option | Determinism | Testability | Transparency | Dependencies | Azure alignment | Verdict |
|---|---|---|---|---|---|---|
| **Custom orchestrator (chosen)** | ✅ Explicit loop in `Orchestrator.run` | ✅ 478 tests | ✅ ~600 lines, fully owned | 0 | Neutral (provider-agnostic LLM router) | **Accepted** |
| **Microsoft Agent Framework (MAF)** | ✅ `WorkflowBuilder` executes in deterministic supersteps | ✅ | ⚠️ Higher abstraction to learn | `agent-framework` | ✅ Native (FoundryChatClient) | Defer — revisit at deployment |
| **LangGraph** | ✅ `StateGraph` is deterministic | ✅ | ⚠️ State/reducer mental model | langgraph | Neutral | Rejected — overkill for a fixed DAG |
| **LangChain** | ⚠️ Abstraction-heavy chains | ⚠️ | ⚠️ Large surface | Large | Neutral | Rejected — was the original plan, outgrown |

### Why MAF is the strongest alternative (notes for the revisit)

MAF (Microsoft's open-source successor to AutoGen + Semantic Kernel; Python packages
`agent-framework` / `agent-framework-core`) expresses our pipeline cleanly:
`SequentialBuilder(participants=[...])` for the linear chain, and a custom resolver
step for judge arbitration. It also bridges to Azure AI Foundry via `FoundryChatClient`,
which matters once we deploy. It was not chosen now because the framework's value —
managed state, teams, handoffs, cloud hosting — is realised only when we adopt the
Foundry Agent Service; locally it would add an abstraction layer without removing any
of our own code.

## 5. Consequences

- **Kept:** `Orchestrator.run`, `_detect_conflicts` (6 deterministic pairs),
  `_apply_judge_resolutions`, rate-limit gates, artifact generation.
- **Continued:** every new capability (MCP tools, governance, evaluation) plugs into
  the existing orchestrator as plain modules — no framework migration needed.
- **Cost:** if we migrate later, the porting effort is contained to `orchestrator.py`
  and `agent_base.py`; the agents themselves stay as-is because they are plain
  Python classes with a shared contract.

## 6. Revisit triggers (when this decision gets re-opened)

1. We deploy the dashboard to **Azure AI Foundry Agent Service** (managed hosting,
   threads, file search) — then MAF becomes the natural client SDK.
2. The pipeline grows **dynamic** behaviour (conditional branches, retry-on-condition,
   agent handoffs) that the fixed loop would have to hand-roll.
3. The team wants to consume **MAF/Foundry-managed agents or tools** rather than our
   own implementations.

Until one of those triggers fires, the custom orchestrator remains the right call —
it is smaller, fully understood, and completely covered by tests.

## 7. Brainstorming & Deliberation Record

This section records *how* the decision was made, not just what was decided. When
we were asked in review whether we actually thought the framework question through,
this is the trail that proves we did.

### 7.1 Timeline

| When | What happened |
|---|---|
| Phase 0 (planning) | The original plan was **LangChain** — the team discussed using it as the orchestration layer. |
| Phases 4–6 (build) | While building `BaseAgent`, we realised LangChain's abstractions were adding indirection to a simple fixed pipeline without removing any of our code. We pivoted to a custom loop and shipped it. The decision was made by consensus (Narendra, Andrew, Ivan) but never written down — a known documentation gap. |
| Aug 2026 (issue #6) | Punit asked for the reasoning on paper. RFC 0001 was written, reviewed by the three owners, and accepted. |

### 7.2 The actual debate (reconstructed from chat history)

1. **"Use a framework because it's the standard" (LangChain).** This was the
   original plan. The counter-argument that won: our pipeline is a fixed 5-step
   DAG with one arbitration step — LangChain would add chains, callbacks and
   wrappers without removing any of our own code, and a LangChain error trace is
   harder to debug than our explicit `Orchestrator.run` loop. We outgrew it
   during Phases 4–6 and dropped it.

2. **"Determinism and testability beat framework features."** Every agent
   returns schema-validated JSON; correctness is enforced by 478 tests, not by
   framework machinery. This was the strongest argument for custom, and it held.

3. **"What about MAF / Semantic Kernel / AutoGen?"** Evaluated during the RFC
   stage. MAF is the strongest alternative (`SequentialBuilder`, deterministic
   supersteps, `FoundryChatClient`), but its value is unlocked by Azure AI
   Foundry Agent Service hosting — which we don't use yet. Semantic Kernel and
   AutoGen were folded into MAF upstream, so the MAF row covers them.

4. **"When do we switch?"** The team set explicit revisit triggers (deploy to
   Foundry / the pipeline grows dynamic behaviour / we consume managed agents).
   Until one fires, custom stays.

### 7.3 Who weighed in

- **All three owners** (Narendra, Andrew, Ivan) — decision by consensus,
  recorded in `docs/DECISIONS.md` (Aug 2026, RFC 0001 row).
- **Punit (reviewer)** — asked for the RFC. The revisit triggers in §6 exist
  precisely so his concern stays on the table at deployment instead of being
  forgotten.
