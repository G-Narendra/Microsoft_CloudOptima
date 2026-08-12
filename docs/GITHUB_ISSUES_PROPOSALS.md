# Punit's GitHub Issues — Analysis & Proposed Solutions

> **Status:** ⚡ **Implemented (Aug 2026)** — all six issues are addressed in code
> and scripts; see `docs/BUILD_CHECKLIST.md` Phases 11–13 and `docs/DECISIONS.md`
> for what landed. This file remains the issue → solution reference for the
> GitHub comments. Every proposal is grounded in the current CloudOptima codebase
> and uses the **exact** Microsoft packages/APIs as of Aug 2026.
>
> **Team:** Narendra (lead), Andrew, Ivan · **Reviewer:** Punit Shah · **Branch:** `dev`
> **Team progress:** See `docs/PROGRESS_REPORT.md` — issue resolutions, phase status,
> team contributions, and the roadmap for the remaining phases (12–15).

---

## 0. Implementation status — real framework usage (verified live, not look-alikes)

| Issue | What Punit asked for | The actual Microsoft/industry package used | Live verification (this machine) |
|---|---|---|---|
| **#2** | Azure AI Content Safety **+ Prompt Shields** | `azure-ai-contentsafety` SDK for moderation · **Prompt Shields via the real REST `text:shieldPrompt` endpoint** (`httpx`, `Ocp-Apim-Subscription-Key`) | moderation SDK wired; shield REST path tested with mocked responses; graceful fallback to offline floor + regex
| **#3** | **PyRIT** + AI Red Teaming at scale | `pyrit` 0.14 — custom `PromptTarget`, converters (UnicodeConfusable, Base64, Flip, ROT13, Atbash, Leetspeak, Bidi), `SubStringScorer`, `SQLiteMemory` | campaign drives **119 strict variants → 0.0% ASR** (leet-of-base64 = documented known gap); each round it found + we fixed a real gap (short-base64, Flip/ROT13, Atbash/leet/Bidi)
| **#4** | **Azure AI Evaluation SDK** | `azure-ai-evaluation` `evaluate()` — `F1ScoreEvaluator`, `RougeScoreEvaluator` (always on) + `Groundedness/Relevance/Coherence` + safety evaluators (judge configured) | real numbers written to `results/latest_eval.json` with **no API key needed** (offline tier)
| **#5** | **AGT** runtime control + auditability | `agent-governance-toolkit(-core)` — `agentmesh.governance.PolicyEngine` loads `policies/tools.yaml` at runtime; `agt lint-policy` passes clean | `check_action` consults the real AGT engine (`AGT_AVAILABLE=True`): price→allow, deploy→deny
| **#7** | **MCP** tool-driven agents | official `mcp` SDK — `MCPServer` (v2) + stdio `ClientSession` bridge | `bridge.call_tool('list_regions')` → `source: 'mcp'` full protocol round-trip
| **#6** | RFC custom vs MAF/LangGraph/LangChain | documentation artifact | `docs/rfcs/0001-custom-orchestrator.md` + DECISIONS row

Every tool call also passes through governance + output sanitization, and the
whole responsible-AI loop is gated in CI (deterministic red-team `--strict`,
527 unit tests, mypy strict, ruff). An independent external principal-engineer
review (see `docs/PROGRESS_REPORT.md` §2.5) went 7.5 → **8.8/10** across two
rounds; every finding — including real PyRIT bypasses (Flip/ROT13, then
Atbash/leetspeak/Bidi) — is fixed with a regression test, and the suite grew
from 478 to 527 tests.

---

## 1. Executive Summary

Punit opened **six issues**. Read together they are not random feedback — they are a
**roadmap toward Microsoft's enterprise agent stack** (Azure AI Foundry, Microsoft
Agent Framework, Agent Governance Toolkit) plus **Microsoft's Responsible AI program**
(evaluation, red teaming, content safety). He explicitly said *"for you and team to
review, discuss and implement"* — so each issue deserves a written evaluation, then an
agreed implementation.

| Issue | Title | What he's really asking | Related phase(s) | Proposed solution (this doc) | Effort | Priority |
|---|---|---|---|---|---|---|
| **#7** | Evaluate MCP integration | "Your agents only write text — give them real tools." | **None in 1–10** — new capability; agent loop built text-only in Phases 4 & 6 | Add an MCP client layer to `BaseAgent`; ship 2 in-house FastMCP servers (live pricing, compliance lookup); optionally host via Azure AI Foundry Toolboxes later | 🔶 Medium | Phase 12–13 |
| **#6** | RFC: custom orchestrator vs MAF / LangGraph / LangChain | "Prove your architecture choice on paper." | **4 & 6** — choice made there, never documented as RFC/ADR | Write a formal RFC/ADR in `docs/` comparing 4 options against fixed criteria; recommend staying custom for now, revisit at deployment | 🟢 Docs only | **Do first** |
| **#5** | Evaluate & integrate Agent Governance Toolkit | "Who watches your agents at runtime? Where's the tamper-evident audit trail?" | **9 & 10** — custom governance built; AGT never evaluated | Gap-analysis vs our `observability.py`; adopt `agent-governance-toolkit` `govern()` for tool calls + `agt verify` OWASP check | 🔶 Medium | Phase 12–13 (pairs with #7) |
| **#4** | Automated evaluation via Azure AI Evaluation SDK | "Your 418 tests check *format*, not *quality*." | **11** — Testing phase open; quality never in its checklist | Add `azure-ai-evaluation` harness scoring groundedness/relevance/coherence of real pipeline runs; adversarial simulation | 🔶 Medium | Phase 11 |
| **#3** | Automated adversarial testing with PyRIT | "Stop pen-testing by hand — attack at scale." | **10 & 11** — manual pen tests in 10; automation never scoped | Add PyRIT red-team suite targeting our agents + scorers; wire curated attacks into CI | 🔶 Medium | Phase 11 |
| **#2** | Azure AI Content Safety + Prompt Shields | "Your regex defense is good — Microsoft's ML defense is better." | **3 & 10** — regex layer built/hardened; ML layer never scoped | Add `azure-ai-contentsafety` moderation + Prompt Shields wrapper in `sanitize.py` with graceful fallback (same pattern as pricing) | 🟢 Low | **First code win** |

**Recommended order:** #6 (RFC) → #2 (Content Safety) → #4 + #3 (Responsible AI pair)
→ #5 + #7 (agent-platform pair). Group them into two milestones:

- **Milestone A (Responsible AI):** #2 + #3 + #4
- **Milestone B (Agent platform):** #5 + #7, plus the #6 RFC as the decision document
  that frames both.

---

### 1.1 Phase Attribution — Where Each Gap Lives

> **Headline: nobody "missed" a checklist item.** Every issue below is either a
> **scope gap** (the item never appeared in any Phase 1–10 checklist) or a **new
> enterprise capability** beyond Phases 1–10. Attribution here is to *phase scope*,
> not to blame — it exists so we can see exactly where each item belongs and extend the
> right phase going forward.

| Issue | Originates from phase(s) | What that phase covered | What was missing | Gap type |
|---|---|---|---|---|
| **#7** | None in 1–10 (closest anchors: 4 Base Agent, 6 Orchestrator; hosted MCP fits 13 Deploy) | Agents are text-in → text-out (structured JSON, schema-validated) | Any tool-calling capability | New capability (never planned) |
| **#6** | **4** (Base Agent) + **6** (Orchestrator) | Custom orchestrator + `BaseAgent` built; 418 tests green | Written RFC/ADR comparing custom vs MAF / LangGraph / LangChain | Documentation gap inside completed phases |
| **#5** | **9** (Logging & Health) + **10** (Security) | `AuditLogger`, `AnomalyDetector`, rate limiting, output scanning | Evaluation of Microsoft's AGT (policy verdicts, tamper-evident audit, OWASP Agentic Top 10) | Enterprise-tooling gap (we built our own instead) |
| **#4** | **11** (Testing — open; 418 tests already exceed its 30+/85% bar) | Tests assert schema/structure, injection, caching, routing | Output-quality evaluation (groundedness / relevance / coherence) | Scope gap in the open Phase 11 |
| **#3** | **10** (Security) + **11** (Testing) | 27 hand-written penetration tests | Automated adversarial tooling + Attack Success Rate metric | Automation gap (manual tests only) |
| **#2** | **3** (Input/Output Sanitization) + **10** (Security) | Regex sanitization, injection detection, homoglyph normalization | ML-based moderation + Prompt Shields (user-prompt & document/indirect attacks) | Depth-of-defense gap (regex only) |

**Implementation owners (team notes):** Phase 0 (repo + checklists) — Narendra · Phase 1 — Ivan ·
Phases 2–3 — Andrew · Phases 4–10 — Narendra · Phase 11 — Narendra + team review (527 tests, 92.62% coverage) ·
Issues #2–#7 — Narendra + team review · External-review hardening (11.7) — Narendra.

**Takeaway:** the checklists were defined up front, and none of the six issues appeared
in any Phase 1–10 checklist — so the gaps are in **phase definition**, not execution.
The cleanest fix is to **extend Phase 11 with #2 + #3 + #4 (Responsible AI)** and
**Phases 12–13 with #5 + #7 (agent platform)** instead of reopening completed phases.

---

## 2. Common Thread — What Punit Is Really Signaling

Every issue maps to a Microsoft product or practice. Recognizing the pattern matters
because it tells us *how* to respond:

| Issue | Microsoft anchor |
|---|---|
| #7 MCP | Azure AI Foundry Agent Service (hosted MCP, Toolboxes) |
| #6 RFC | Engineering culture — ADRs / RFCs before big decisions |
| #5 AGT | Microsoft's open-source governance toolkit (OWASP Agentic Top 10) |
| #4 Eval SDK | Azure AI Foundry evaluation / Responsible AI |
| #3 PyRIT | Microsoft's AI Red Team tooling |
| #2 Content Safety | Azure AI Content Safety service |

**The response strategy:** for each issue we post a comment that (1) restates the
problem in our own words, (2) states what we already have, (3) proposes the concrete
approach below, and (4) gives an effort estimate. We do **not** silently implement all
six — we get alignment first, milestone by milestone. This matches his "review, discuss
and implement" framing.

---

## 3. Issue #7 — Evaluate MCP (Model Context Protocol) Integration

> **Phase attribution:** No phase in 1–10 owned tool-calling — this is a **new
> capability request**. Closest anchors: Phase 4 (Base Agent — agent loop designed
> text-only) and Phase 6 (Orchestrator); hosted MCP pairs with Phase 13 (Deploy to
> Azure). Nobody missed it — it was never in any checklist.

### 3.1 What he's asking
MCP is the industry-standard protocol (created by Anthropic, now governed by the
**Agentic AI Foundation under the Linux Foundation** since Dec 2025) that lets AI
agents call **external tools and data sources** through a standard client–server
interface. Punit wants us to evaluate whether CloudOptima's agents should become
**tool-driven** instead of text-only.

### 3.2 Why it matters
Today our agents are **text-in → text-out**:

- The **cost analyst** reads static pricing or the Azure Retail Prices API we call *ourselves* in code — the *model* cannot query anything.
- The **architect** writes Bicep from its own knowledge — it cannot look up a live resource catalog.
- The **compliance officer** reads our RAG corpus — it cannot fetch a current regulation.

With MCP, the *agent itself* could call tools: `get_live_price(service, region)`,
`list_azure_services()`, `lookup_compliance_rule(framework, topic)`. That is the
difference between "an app that suggests" and "an agent that acts." Microsoft is all-in
on MCP: Azure AI Foundry hosts MCP servers natively, bundles tools into **Toolboxes**
(versioned, centrally governed), and supports **approval workflows**
(`require_approval="always"`) with Entra ID identity passthrough.

### 3.3 Where we are today
- Agents produce structured JSON, validated by `BaseAgent._validate_output` (`cloudoptima/agent_base.py`).
- Live data access is **hardcoded in the app layer**, not agent-driven: `cloudoptima/pricing/azure_api.py` (Retail Prices API) and `cloudoptima/compliance/rag.py` (`query_rag`).
- The LLM router (`cloudoptima/llm_routing.py`, `CostAwareRouter`) is provider-agnostic — an MCP layer would slot above it cleanly.

### 3.4 Proposed solution
**Phase A — bring tools into the agent loop (local, framework-free):**

1. Add the official Python MCP SDK: `pip install "mcp[cli]"` (the `mcp` package, v2 line).
2. Write two small **FastMCP servers** inside the repo (e.g. `cloudoptima/mcp/servers.py`):
   - `azure_pricing` → wraps the existing `pricing/azure_api.py` live-price lookup.
   - `compliance_lookup` → wraps `compliance/rag.py` `query_rag`.
3. Add an **MCP client layer to `BaseAgent`**: before a specialist agent runs, the
   orchestrator connects to the servers via `ClientSession`, calls `list_tools()`,
   injects the tool schema into the prompt, and dispatches `call_tool()` when the model
   requests it. Results are **cleaned with `clean_output` and injection-scanned**
   (`sanitize.py`) before entering the prompt (untrusted tool data — same rule as RAG).

Minimal pattern (verified against the current `mcp` SDK):

```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def run_tool(session: ClientSession, name: str, args: dict) -> str:
    result = await session.call_tool(name, arguments=args)
    return "".join(part.text for part in result.content if hasattr(part, "text"))

async def main() -> None:
    params = StdioServerParameters(command="python", args=["cloudoptima/mcp/servers.py"])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()          # discover
            print([t.name for t in tools.tools])
            print(await run_tool(session, "get_live_price", {"service": "vm", "region": "uaenorth"}))
```

**Phase B — hosted (Azure, later):** when we deploy, the same tools can be re-exposed as
a remote MCP endpoint and connected through **Azure AI Foundry Agent Service** using the
`azure-ai-projects` SDK (`MCPTool(server_label=..., server_url=..., require_approval=...)`),
gaining approval workflows and credential management for free.

### 3.5 Risks & guardrails
- **Tool output is untrusted** → must pass through `clean_output` + `detect_injection` + `scan_llm_output` (same as our RAG passages after the Phase 10 fix).
- **Tool misuse** → all tool calls go through the same audit logging as LLM calls; sensitive tools marked `require_approval`.
- **Scope creep** → Phase A delivers *read-only* tools only (pricing, compliance). No write/exec tools. This keeps the security surface identical to today.

### 3.6 Acceptance criteria (what we show Punit)
- A dashboard run where the cost analyst's live prices visibly come **from a tool call** (logged in the audit trail with tool name + args).
- Tests: tool schema injected, tool call dispatched, hostile tool output blocked.

---

## 4. Issue #6 — RFC: Why a Custom Orchestrator Instead of MAF / LangGraph / LangChain?

> **Phase attribution:** Phase 4 (Base Agent) + Phase 6 (Orchestrator) — the custom
> framework choice was made and shipped there, but the **RFC/ADR documenting why was
> never written**. A documentation gap inside two completed phases.

### 4.1 What he's asking
He formalized the question he already asked in chat. An **RFC (Request For Comments)**
is the engineering-culture artifact that records *what we chose, what we compared it
against, and why* — so the decision is reviewable. This is a **documentation task, not a
code task.**

### 4.2 Why it matters
Microsoft teams live on **ADRs (Architecture Decision Records)**. We *did* make a
deliberate choice (evaluated LangChain early, built a custom deterministic pipeline),
but the reasoning lives in chat history, not the repo. An RFC makes it durable and
auditable — and it pre-empts the same question being asked again at every review.

### 4.3 Current state
- `docs/DECISIONS.md` already logs decisions (e.g. "Continue from existing architecture",
  "Single `BaseAgent` template method", "Deterministic 6-pair conflict detection").
- `cloudoptima/orchestrator.py`: `_PIPELINE_TYPES` (Architect → Cost → Security →
  Compliance → Judge), sequential execution, `_detect_conflicts`, `_apply_judge_resolutions`,
  failure isolation, rate-limit gates.
- No orchestration framework in `requirements.txt` (only pydantic, httpx, streamlit,
  openai, pytest, ruff, mypy; optional chromadb).

### 4.4 Proposed RFC structure (to write in `docs/rfcs/0001-custom-orchestrator.md`)

**Context:** 5 agents, fixed linear order, deterministic conflict detection + judge
arbitration. Constraints: must be testable (schema-validated JSON), auditable,
dependency-light, and a learning project.

**Options compared against criteria** (determinism · testability · transparency ·
dependency weight · learning value · Azure alignment):

| Option | Determinism | Testability | Dependencies | Azure alignment | Verdict |
|---|---|---|---|---|---|
| **Custom orchestrator (current)** | ✅ Full — async DAG (`asyncio.gather`, round-3 P1) | ✅ 540 tests | 0 | Neutral | **Recommended (for now)** |
| **Microsoft Agent Framework (MAF)** | ✅ `WorkflowBuilder` supersteps (BSP) | ✅ | `agent-framework` (new) | ✅ Native | Strong candidate at deployment |
| **LangGraph** | ✅ StateGraph | ✅ | langgraph | Neutral | Overkill for a fixed linear DAG |
| **LangChain** | ⚠️ abstraction-heavy | ⚠️ | Large | Neutral | Rejected (original plan, outgrown) |

**MAF note (verified Aug 2026):** MAF is Microsoft's unified open-source agent SDK
(successor to AutoGen + Semantic Kernel; Python package `agent-framework` /
`agent-framework-core`). A 5-agent linear pipeline is `SequentialBuilder(participants=[...])`
and a graph topology is `WorkflowBuilder` with executors/edges executing in deterministic
**supersteps** — including a conflict-resolution step natively. It also bridges to Azure
AI Foundry via `FoundryChatClient`.

**Recommendation:** *Stay custom for this project's current phase* — our pipeline is a
fixed linear DAG, our value is transparency + learning, and our tests are the strongest
artifact we have. **Revisit the decision at deployment**: if we host agents in Azure AI
Foundry Agent Service, adopting MAF as the client SDK (or at least aligning with it)
becomes the right call. The RFC records the trigger conditions so the choice gets
re-evaluated, not forgotten.

### 4.5 Acceptance criteria
- RFC merged to `dev`, linked in `DECISIONS.md`, and referenced in our comment on issue #6.
- Punit can see we compared MAF/LangGraph/LangChain honestly, with a defensible
  recommendation and explicit revisit triggers.
- RFC includes a **brainstorming & deliberation record** (timeline, debate
  points, participants) — so the answer to "did you actually think about the
  framework?" is auditable in the repo, not just "yes, in chat".

---

## 5. Issue #5 — Evaluate & Integrate Agent Governance Toolkit (AGT)

> **Phase attribution:** Phase 9 (Logging & Health Checks — `AuditLogger`) + Phase 10
> (Security — anomaly detection, rate limiting). We built our own mini-governance there
> but **never evaluated Microsoft's AGT**. An enterprise-tooling gap in completed phases.

### 5.1 What he's asking
AGT is Microsoft's **open-source (MIT) runtime governance toolkit** —
"policy enforcement, zero-trust identity, execution sandboxing, and reliability
engineering for autonomous AI agents" (covers 10/10 of the OWASP Agentic Top 10).
Punit wants **runtime control and auditability**: *is this action allowed, which agent
did it, and can we prove what happened?*

### 5.2 Why it matters (verified from the AGT repo, Aug 2026)
- **Policy engine:** every tool call/message is evaluated against declarative YAML
  policies before it reaches the wire — actions denied are **structurally impossible**,
  not "politely refused."
- **Verdicts:** `allow` / `deny` / `require_approval` (human-in-the-loop) / `transform`.
- **Audit:** tamper-evident audit trails (Merkle) + OpenTelemetry metrics.
- **Security:** MCP Security Gateway (tool poisoning, typosquatting, hidden-instruction
  scanning), `agt red-team scan`, `agt verify --strict` for OWASP checks in CI.
- **Identity:** SPIFFE / DID / mTLS attribution — solves "five agents, one API key."
- **Python:** `pip install "agent-governance-toolkit[full]"` (v4.1.0 consolidated
  distributions: `-core`, `-runtime`, `-sre`, `-cli`, `[full]` meta-package).

### 5.3 Where we are today
We already built a **mini-version** of this ourselves (Phase 10):

- `cloudoptima/observability.py` — `AuditLogger` (append-only daily JSONL) + `AnomalyDetector` (EWMA flags).
- Rate limiting enforced in `Orchestrator.run` **before** any LLM call.
- `sanitize.py` — output scanning, injection detection, IaC malware scanning.
- `BaseAgent._scan_output` — jailbreak/refusal/executable/base64 content flags.

This is exactly why Punit raised it: *"you wrote your own governance — why not use the
enterprise one?"* (same pattern as issue #6).

### 5.4 Proposed solution — layered, honest adoption
We do **not** need the full 45-package stack. The README itself says: *"Most teams run
policy enforcement + audit logging and never need the full stack."* Proposal:

1. **Gap-analysis first** (deliverable of the GitHub comment): map our AuditLogger,
   anomaly detector, rate limiter, and scanners against AGT's capabilities; list what we
   lack (policy decisions on actions, require_approval, OWASP verification).
2. **Adopt `govern()` for future tool calls** (pairs with #7). Two lines per tool:

```python
from agentmesh.governance import govern
safe_price_tool = govern(get_live_price, policy="policies/tools.yaml")
# every call is checked, logged to the audit trail, and enforced
```

```yaml
# policies/tools.yaml
apiVersion: governance.toolkit/v1
name: cloudoptima-tools
default_action: allow
rules:
  - name: read-only-tools-only
    condition: "action.type in ['get_live_price', 'compliance_lookup']"
    action: allow
  - name: block-write-actions
    condition: "action.type in ['deploy', 'delete', 'send']"
    action: deny
```

3. **CI gate:** `agt verify --evidence ./agt-evidence.json --strict` in the pipeline.
4. **Keep our own layer** as the app-specific defense (schema validation, sanitization,
   anomaly detection); AGT governs *actions*, our code governs *content*. Defense in depth.

### 5.5 Risks
- AGT is "public preview" — pin versions and keep the integration behind a thin
  wrapper so we can swap implementations.
- Full stack (runtime sandboxing, SRE chaos, identity mesh) is out of scope for a
  3-student project — document that boundary explicitly so Punit sees we scoped it.

### 5.6 Acceptance criteria
- Policy file in repo; every tool call decision appears in the audit log with
  verdict + rule id; a denied action raises `GovernanceDenied` and the pipeline keeps
  running (failure isolation preserved).

---

## 6. Issue #4 — Add Automated Evaluation Framework Using Azure AI Evaluation SDK

> **Phase attribution:** Phase 11 (Testing — open). Phase 11's checklist covers test
> counts/coverage; **output-quality evaluation was never scoped there**. A scope gap in
> the open phase — this is exactly where the fix lands.

### 6.1 What he's asking
`azure-ai-evaluation` is Microsoft's SDK for **measuring LLM output quality**, not just
validity. Punit's implicit critique: our 418 tests assert **schema and structure**, but
nobody measures whether the architect's design is actually good, or whether the cost
estimate is accurate.

### 6.2 Why it matters
"Green tests" ≠ "good AI". Microsoft ships built-in evaluators so teams can quantify
quality: **GroundednessEvaluator, RelevanceEvaluator, CoherenceEvaluator,
FluencyEvaluator** (quality) and **ViolenceEvaluator, HateUnfairnessEvaluator,
SexualEvaluator, SelfHarmEvaluator, PromptShieldEvaluator** (safety). Evaluation can run
**locally** with just a `model_config` (endpoint + key + deployment) — no Azure AI
project required — and optionally logs results to an Azure AI Foundry project dashboard.

### 6.3 Where we are today
- `cloudoptima/tests/` — 510 unit tests, 93% coverage: schemas, injection, caching,
  routing, pricing, compliance rules, safety, governance, red-teaming.
- **No evaluation of output quality.** The judge agent arbitrates conflicts, but there
  is no metric like "relevance of the architecture to the user's prompt."

### 6.4 Proposed solution
1. Add `pip install azure-ai-evaluation` to a dev extra.
2. Create `scripts/evaluate/` with a **golden dataset** (`eval_data.jsonl`) of ~15–20
   realistic project prompts (matching the dashboard input contract, incl. region,
   budget, compliance frameworks).
3. A runner that feeds each prompt through `Orchestrator.run` and scores the turns:

```python
import os
from azure.ai.evaluation import evaluate, GroundednessEvaluator, RelevanceEvaluator

model_config = {
    "azure_endpoint": os.environ["AZURE_OPENAI_ENDPOINT"],
    "api_key": os.environ["AZURE_OPENAI_API_KEY"],
    "azure_deployment": os.environ["AZURE_OPENAI_EVAL_DEPLOYMENT"],
}

def cloudoptima_pipeline(query: str) -> dict:
    from cloudoptima.orchestrator import Orchestrator   # real pipeline
    session = Orchestrator.create_default().run(...)     # run for real
    return {"response": json.dumps(session.artifacts), "query": query}

result = evaluate(
    target=cloudoptima_pipeline,
    evaluation_name="cloudoptima_quality_v1",
    data="eval_data.jsonl",
    evaluators={"groundedness": GroundednessEvaluator(model_config),
                "relevance": RelevanceEvaluator(model_config)},
)
print(result["metrics"])   # mean scores per metric
```

4. **Adversarial simulation** (`AdversarialSimulator`, scenario `adversarial_qa`)
   generates hostile prompts against the same target — this bridges into issue #3.
5. Commit a **score baseline** and make the runner a script Punit can run himself
   (or gate CI on it once baselines are set).

### 6.5 Risks
- Evaluator LLM cost (small: 20 prompts × 2 metrics).
- Groundedness needs a "context" (the user prompt + session) — wire the data mapping
  carefully so scores are meaningful.

### 6.6 Acceptance criteria
- A `scripts/evaluate/` folder with dataset + runner; scores above a documented baseline;
  results table attached to our issue #4 comment.

---

## 7. Issue #3 — Add Automated Adversarial Testing with PyRIT and AI Red Teaming

> **Phase attribution:** Phase 10 (Security) covered **27 manual pen tests**; Phase 11
> (Testing) never scoped automated adversarial tooling. An **automation gap** across
> Phases 10 + 11.

### 7.1 What he's asking
**PyRIT** (Python Risk Identification Tool; repo moved to `microsoft/PyRIT`) is
Microsoft's open-source framework for **automated adversarial testing** of generative AI
systems. We currently hand-write ~27 penetration tests in `cloudoptima/tests/test_security.py`.
PyRIT automates hundreds of attack variants and scores outcomes — the same tooling
Microsoft's AI Red Team uses. Red teaming is also a **required step in Microsoft's
Responsible AI process** for shipping AI features.

### 7.2 Why it matters
Manual pen tests don't scale and they rot. PyRIT gives us: **orchestrators**
(`PromptSendingOrchestrator`, `CrescendoOrchestrator`, `RedTeamingOrchestrator`),
**attack strategies** (jailbreak, crescendo, direct strings), **converters**
(base64, Unicode confusable — our homoglyph defense is directly testable here), and
**scorers** (`SelfAskRefusalScorer`, `PromptInjectionScorer`, `AzureContentFilterScorer`,
`HumanInTheLoopScorer`). Its headline metric — **Attack Success Rate (ASR)** — is the
canonical number for "how resistant is the system."

### 7.3 Where we are today
- Phase 10: `detect_injection` (with homoglyph normalization), `scan_llm_output`,
  `scan_for_malware_in_iac`, rate limiting, strict schema rejection — all unit-tested.
- But all tests are **deterministic unit tests**; none model an adaptive adversary.

### 7.4 Proposed solution
1. `pip install pyrit` (dev extra).
2. A red-team harness `scripts/redteam/` that points PyRIT at our pipeline through a
   **custom target** wrapping `BaseAgent.analyze` (or `Orchestrator.run`), e.g. using an
   OpenAI-compatible target against our router, or a custom `PromptTarget` subclass.
3. Attack scenarios mapped to our defenses:
   - `jailbreak` / `crescendo` → must trip `detect_injection` or `scan_llm_output`.
   - `UnicodeConfusableConverter` → must trip homoglyph normalization.
   - prompt-injection-through-RAG → must trip the Phase 10 RAG filter.
4. Score with `SelfAskRefusalScorer` + `PromptInjectionScorer`; report **ASR per vector**
   and gate CI on ASR thresholds (e.g. < 5% on critical vectors).
5. Keep our unit tests as the fast deterministic layer; PyRIT runs nightly/weekly.

### 7.5 Risks
- PyRIT against real LLM calls costs API credits → run against the **mock provider** by
  default (mock refuses on injected input by construction), real providers in a
  credential-gated slow job.
- Keep runtime bounded (attack budgets per scenario).

### 7.6 Acceptance criteria
- `scripts/redteam/` with reproducible runs; ASR report artifact attached to the issue.

---

## 8. Issue #2 — Enhance Safety & Harm Mitigation with Azure AI Content Safety and Prompt Shields

> **Phase attribution:** Phase 3 (Input/Output Sanitization) + Phase 10 (Security) —
> the **regex defense** was built and hardened there; the ML-based Content Safety +
> Prompt Shields layer was never in scope. A **depth-of-defense gap** in completed phases.

### 8.1 What he's asking
Azure AI Content Safety is Microsoft's **ML-based moderation service** (vs our regex
layer), and **Prompt Shields** are purpose-built detectors for **user-prompt attacks**
and **document/indirect attacks** — the exact vector we manually hardened in Phase 10
(RAG injection filter).

### 8.2 Verified facts (Aug 2026)
- Python package: **`azure-ai-contentsafety`**.
- **Text moderation:** `ContentSafetyClient.analyze_text(AnalyzeTextOptions(text=...))`;
  categories `Hate / SelfHarm / Sexual / Violence`, severity `0 (safe) → 6 (high)` in
  four-level output (`0,2,4,6`); REST `POST {endpoint}/contentsafety/text:analyze?api-version=2024-09-01`.
- **Prompt Shields:** `PromptShieldClient.analyze_text(...)` with `user_prompt` +
  `documents` → per-input `attackDetected` flags (User Prompt shield + Document /
  Indirect Attack shield); REST `text:shieldPrompt`.
- Free tier **F0** available; region availability applies (like our other Azure
  integrations, degrade gracefully when the key is absent).

### 8.3 Where we are today
- `cloudoptima/sanitize.py` — `clean_input`, `clean_output`, `detect_injection`
  (regex + homoglyph normalization), `scan_llm_output`, `scan_for_malware_in_iac`.
- Phase 10: RAG passages injection-scanned; poisoned cache excluded.
- Pattern precedent: `pricing/azure_api.py` calls live Azure with **static fallback** —
  exactly the graceful-degradation shape this should follow.

### 8.4 Proposed solution
Add an **optional ML layer** in front of/alongside the regex layer:

1. New module `cloudoptima/safety.py` with two functions, mirroring the pricing
   fallback pattern:
   - `moderate_text(text) -> SafetyVerdict` — calls `ContentSafetyClient`; returns
     category severities + `blocked` when any severity ≥ threshold (recommended 4).
   - `shield_prompt(user_prompt, documents) -> ShieldVerdict` — calls `PromptShieldClient`;
     returns per-document `attack_detected` flags.
2. **Wire points:**
   - `clean_input` path in `app.py` → `moderate_text` on user input before any LLM call.
   - Compliance agent RAG enrichment → `shield_prompt` on retrieved passages (replaces
     the manual regex-only filter as the second line of defense).
   - Dashboard rendering → already HTML-safe; optionally moderate the final summary.
3. **Config** (`cloudoptima/config.py`): `content_safety_endpoint` / `content_safety_key`
   (SecretStr) + `content_safety_threshold` (default 4) + `content_safety_enabled`.
4. **Fallback:** when key/endpoint missing or the call fails → log + return
   "no ML verdict" and let the existing regex layer enforce. The app **never breaks**
   without the Azure resource (same contract as pricing).

Minimal call pattern:

```python
from azure.ai.contentsafety import ContentSafetyClient, AnalyzeTextOptions, TextCategory
from azure.core.credentials import AzureKeyCredential

client = ContentSafetyClient(endpoint, AzureKeyCredential(key))
res = client.analyze_text(AnalyzeTextOptions(text=user_input))
severity = {a.category: a.severity for a in res.categories_analysis}
blocked = max(severity.values(), default=0) >= THRESHOLD   # 4 = Medium
```

### 8.5 Risks
- Latency (~100–300 ms per call) → apply to the **user prompt once** and RAG passages,
  not every token; cache verdicts per input hash (we already have an LLM cache pattern).
- False positives → threshold configurable per category.

### 8.6 Acceptance criteria
- With a key: hostile input and injected RAG doc are blocked; benign input passes.
- Without a key: everything works exactly as today (fallback path tested).

---

## 9. Proposed Execution Plan

| Step | Issue | Deliverable | Where | Est. effort |
|---|---|---|---|---|
| 1 | #6 | RFC `0001-custom-orchestrator.md` + DECISIONS.md link | `docs/rfcs/` | 1 day |
| 2 | #2 | `cloudoptima/safety.py` + config + tests | code | 2–3 days |
| 3 | #4 | `scripts/evaluate/` (dataset + runner + baseline) | scripts | 2–3 days |
| 4 | #3 | `scripts/redteam/` (PyRIT harness + ASR gate) | scripts | 2–3 days |
| 5 | #5 | Gap-analysis doc + `govern()` on tool calls + `agt verify` CI | code + docs | 2–3 days |
| 6 | #7 | MCP servers + client layer in `BaseAgent` | code | 3–5 days |

All changes land on `dev` in small reviewable PRs; `main` merges only after team +
Punit approval. Every milestone comment on GitHub states what we did and what we
deliberately did **not** do (and why) — that honesty is what makes the evaluation
credible.

---

## 10. References (verified Aug 2026)

- **MCP:** `mcp` PyPI package · FastMCP · Agentic AI Foundation (Linux Foundation) ·
  Azure AI Foundry: "Connect agents to MCP server endpoints" (Microsoft Learn) ·
  Foundry Toolboxes
- **MAF:** `agent-framework` / `agent-framework-core` PyPI · `SequentialBuilder` /
  `WorkflowBuilder` (superstep execution) · Azure AI Foundry Agent Service
- **AGT:** `github.com/microsoft/agent-governance-toolkit` · `agent-governance-toolkit[full]`
  (v4.1.0) · `agentmesh.governance.govern` · Agent Control Specification · OWASP Agentic
  Top 10 · `agt verify` / `agt red-team scan`
- **Evaluation:** `azure-ai-evaluation` · `evaluate()` with custom target ·
  Groundedness/Relevance/Coherence + safety evaluators · `AdversarialSimulator`
- **PyRIT:** `github.com/microsoft/PyRIT` · `PromptSendingOrchestrator` ·
  `CrescendoOrchestrator` · `SelfAskRefusalScorer` · Attack Success Rate (ASR)
- **Content Safety:** `azure-ai-contentsafety` · `ContentSafetyClient.analyze_text`
  (severity 0–6) · `PromptShieldClient` (user prompt + document/indirect attack shields) ·
  REST `text:analyze` / `text:shieldPrompt` (api-version 2024-09-01) · F0 free tier
