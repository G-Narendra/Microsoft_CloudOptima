# CloudOptima — Team Progress Report

> **Branch:** `dev` · **Date:** August 2026
> **Team:** Narendra (lead) · Andrew · Ivan
> **Microsoft reviewer:** Punit Shah
>
> **One line:** Phases 0–11 are complete in practice (**478 tests · 93% coverage · mypy & ruff clean**),
> all **six of Punit's GitHub issues (#2–#7)** are implemented with the **real Microsoft
> frameworks** (not look-alikes), and the remaining roadmap is clear: **Phases 12–15**
> (Docker → Azure deploy → production → persistence & auth).

---

## 1. Executive Summary

CloudOptima is a multi-agent AI system that designs cloud architectures. A user describes
their infrastructure in plain English, and five AI agents (Architect, Cost Analyst,
Security Engineer, Compliance Officer) collaborate while a Judge resolves their conflicts —
producing IaC templates, a cost forecast, a security report, and a compliance status.

We continued from Narendra's pre-existing architecture (the team's decision, agreed with
Punit) and rebuilt it phase by phase. Everything up to **Phase 10** is complete and merged,
**Phase 11 (Testing)** is complete in practice — the 30-test / 85%-coverage bar was exceeded
long ago — and **Punit's six review issues** raised on GitHub have all been implemented and
verified live on this machine.

What remains is the deployment half of the project: **Phase 12 (Docker)**, **Phase 13
(Azure deploy)**, **Phase 14 (production reliability)** and **Phase 15 (persistence &
auth)**. Each is small, well-defined, and gated by the same quality bar we already hold.

---

## 2. Punit's GitHub Issues — Asked vs Fixed

Punit opened six issues. Read together they were a roadmap toward **Microsoft's enterprise
agent stack** (MCP, Agent Governance Toolkit, Azure AI Foundry) plus **Microsoft's
Responsible AI program** (Content Safety, PyRIT red teaming, azure-ai-evaluation). None of
them required reopening a completed phase — they were new capabilities and a documentation
gap, so we extended the open phases (11–13) to carry them.

| Issue | What he asked | The actual Microsoft/industry package we used | Live verification |
|---|---|---|---|
| **#2** | Azure AI Content Safety + Prompt Shields | `azure-ai-contentsafety` SDK for moderation; **Prompt Shields via the real REST `text:shieldPrompt` endpoint** (`httpx`, `Ocp-Apim-Subscription-Key`) | Moderation SDK wired; shield REST path tested; graceful fallback to the offline floor |
| **#3** | PyRIT + AI Red Teaming at scale | `pyrit` 0.14 — custom `PromptTarget`, `UnicodeConfusableConverter` + `Base64Converter`, `SubStringScorer`, `SQLiteMemory` | Campaign drives **45 variants → 0.0% ASR** — and it *found a real gap* we then fixed (short-base64 smuggling) |
| **#4** | Automated evaluation via Azure AI Evaluation SDK | `azure-ai-evaluation` `evaluate()` — F1 + Rouge (always on, offline) + Groundedness/Relevance/Coherence + safety evaluators (when a judge model is configured) | Real metric numbers written to `scripts/evaluate/results/latest_eval.json` with **zero API keys needed** |
| **#5** | Agent Governance Toolkit (AGT) | `agentmesh.governance.PolicyEngine` loads `cloudoptima/policies/tools.yaml` at runtime; `agt lint-policy` passes clean | `check_action` consults the **real AGT engine**: `get_live_price` → allow, `deploy` → deny, unknown → deny (fail closed) |
| **#7** | MCP tool-driven agents | Official `mcp` SDK — FastMCP server (stdio) + `ClientSession` bridge, with an in-process registry fallback | `bridge.call_tool('list_regions')` → `source: 'mcp'` full protocol round-trip |
| **#6** | RFC: custom orchestrator vs MAF / LangGraph / LangChain | Documentation artifact | `docs/rfcs/0001-custom-orchestrator.md` + a `DECISIONS.md` row — honest comparison, recommend staying custom, revisit at deployment |

### The most important moment — PyRIT found a real gap

The **first** real PyRIT campaign scored **31% ASR**: every Base64-converted payload reached
output. Short Base64 smuggling bypassed our old 200-character blob heuristic. That is exactly
what Punit's red-teaming request was for. We fixed it properly at the sanitizer layer
(`decode_base64_tokens` — recursive decode-then-scan, re-checked against injection patterns
and dangerous categories), added a CI case, and re-ran:

- **PyRIT campaign: 0.0% ASR (0/45 variants)**
- **Deterministic red-team gate: 0.0% (16 vectors)**
- **Zero false positives** on legitimate Base64 (e.g. `"US--Canada 0--9"` passes)

### Every integration degrades gracefully

The pattern we used for pricing holds everywhere: **when the optional package or API key is
absent, the app behaves exactly as before** (offline mirror / regex floor). CloudOptima never
breaks without an Azure resource — demo mode and tests still work with the mock provider.

---

## 3. Phase Status (0 → 15)

| Phase | What it delivered | Status | Owner |
|---|---|---|---|
| 0 | Repo, README, build checklist, team setup | ✅ Complete | Narendra |
| 1 | Type-safe config + data models | ✅ Complete | Ivan |
| 2 | LLM client (Mock/Nvidia/Azure) + gzip cache | ✅ Complete | Andrew |
| 3 | Input/output sanitization + rate limiting | ✅ Complete | Andrew |
| 4 | `BaseAgent` template method (prompt hardening, caching, error turns) | ✅ Complete | Narendra |
| 5 | All 5 agents with strict schema validation | ✅ Complete | Narendra |
| 6 | Orchestrator: 5-agent pipeline, 6-pair conflict detection, judge arbitration, 4 artifacts, CLI | ✅ Complete | Narendra |
| 7 | Streamlit dashboard (real progress bar, 4 result tabs, downloads) | ✅ Complete | Narendra |
| 7.5 | Cost-aware LLM routing (cheapest-first, failover, spend guard) | ✅ Complete | Narendra |
| 7.6 | Multi-provider expansion (OpenAI, Anthropic, Google + Azure + Nvidia) | ✅ Complete | Narendra |
| 8 | Compliance rules (21 immutable) + RAG + static & live Azure Retail Prices | ✅ Complete | Narendra |
| 9 | Audit logging, `@trace`, health checks | ✅ Complete | Narendra |
| 10 | Security hardening (jailbreak scan, anomaly detection, strict schemas, rate limiting, pen tests) | ✅ Complete | Narendra |
| 11 | Testing + **Punit's issues #2–#5** (Responsible AI) | ✅ Complete in practice — 478 tests · 93% coverage (85% gate); leftover: judge-model baseline scores | Narendra + team review |
| 12 | Docker (also carries **issue #7** MCP tools + **issue #5** AGT deploy notes) | 📅 Planned | Team |
| 13 | Deploy to Azure App Service + CI/CD | 📅 Planned | Team |
| 14 | Production reliability (monitoring, scaling, secrets, backup) | 📅 Planned | Team |
| 15 | Persistence + auth (DB sessions, Azure AD B2C) | 📅 Planned | Team |

**Completed: Phases 0–11** (including 7.5 and 7.6) and **all six of Punit's issues**.
**Remaining: Phases 12, 13, 14, 15.**

---

## 4. Team Contributions

| Who | Worked on | Notes |
|---|---|---|
| **Narendra** | Phase 0 (repo, README, checklist), Phases 4–10 (base agent, five agents, orchestrator, dashboard, routing 7.5, multi-provider 7.6, compliance & pricing, logging & health, security hardening), the implementations for Punit's issues #2–#7, and all recent docs (DECISIONS, PROGRESS_REPORT, checklist updates) | Also audited Andrew's and Ivan's work when their phases landed on `dev`, fixed small issues, and manages branch merges |
| **Ivan** | Phase 1 — type-safe `Settings`, domain models, enums, null-byte sanitation | Completed the Phase 1 checklist from the build checklist |
| **Andrew** | Phases 2–3 — LLM client + retry + cache, and the sanitization pipeline | Completed the Phase 2 and 3 checklists |

**How we work:** everything lands on the `dev` branch; `main` only receives reviewed,
merged phases after team + Punit approval (Narendra's standing rule — nothing pushes itself).
Phase 11 and the issue implementations were reviewed by the team before this report.

---

## 5. Remaining Phases & How We'll Solve Them

### Phase 11 — finishing touch (tiny)
- [ ] **Record baseline scores** with a judge model: once we have an Azure OpenAI
      evaluation deployment, run `scripts/evaluate/run_evaluation.py --judge` and commit
      `scripts/evaluate/results/latest_eval.json` as the quality baseline.
- Everything else in Phase 11 is done: `conftest.py`, pytest config in `pyproject.toml`
  (verbose + coverage + **85% fail-under gate**), 478 tests, per-file coverage ≥90% on
  `sanitize.py` (99%), `orchestrator.py` (93%), `agent_base.py` (92%).

### Phase 12 — Docker (Day 14–15)
1. `Dockerfile`: `python:3.11-slim`, install `requirements.txt`, copy the package,
   default `DEMO_MODE=true` / `LLM_PROVIDER=mock`, health check, port 8501,
   **run as non-root** (`useradd cloudoptima`).
2. `.dockerignore` so `.env` and `__pycache__` never enter the image.
3. Local proof: `docker build -t cloudoptima . && docker run -p 8501:8501 cloudoptima`,
   run an analysis in mock mode (<2 s), verify non-root and no `.env` inside the image.
4. Also expose the MCP server port when `MCP_ENABLED=true` (issue #7 note) and keep
   `agt lint-policy` in the image build (issue #5 note).

### Phase 13 — Deploy to Azure (Day 15–18)
1. Student Azure account ($100 credits) → `az login` → resource group `cloudoptima-rg`
   (uaenorth).
2. App Service plan (F1 free tier, Linux, Python 3.11) → `az webapp up`.
3. Env vars in **App Settings** (never code): `DEMO_MODE=true`, `LLM_PROVIDER=mock` first;
   real provider keys added only when the team agrees.
4. CI/CD via GitHub Actions: on push to `main` → install deps → `pytest` (+
   `redteam_cloudoptima.py --strict` gate) → deploy if green; publish profile stored as a
   GitHub secret.
5. Post-deploy checks: dashboard loads, a test analysis completes, health check passes,
   no secrets exposed.

### Phase 14 — Production reliability (Day 18–20)
1. Monitoring: Azure Monitor + Sentry for LLM timeouts / JSON parse errors / rate-limit hits.
2. Performance: cache TTL 24h, rate limit 60/min per user.
3. Secrets & backup: config in Azure Key Vault; daily audit-log backup to Azure Blob.
4. Final security checklist (all inputs sanitized, outputs schema-validated, no
   `unsafe_allow_html`, no keys in code/logs, rate limiting everywhere, non-root Docker,
   health checks, append-only audit logs, tests before deploy).

### Phase 15 — Persistence & auth (after deployment)
1. Session store: SQLite locally → Azure Database for PostgreSQL / Cosmos DB via env var;
   artifacts as blobs (Azure Blob Storage in prod).
2. Auth: **Azure AD B2C** login before the dashboard renders; sessions scoped per user
   (best fit for the Microsoft context); hashed passwords, never logged.
3. Optional: Azure Queue / Durable Functions for long analyses, dashboard polls job status.

**Sequencing:** 12 → 13 → 14 → 15. Every phase lands on `dev` in small PRs, is reviewed by
the team and Punit, and must pass tests + the red-team strict gate before the `main` merge.

---

## 6. Quality Gates (current numbers, verified on this machine)

| Gate | Result |
|---|---|
| Unit/integration tests | **478 passed · 0 failed** |
| Coverage | **93% overall** (gate 85%) · sanitize 99% · orchestrator 93% · agent_base 92% |
| mypy | Clean across the package |
| ruff | Clean (`cloudoptima/` + `scripts/`) |
| PyRIT campaign (issue #3) | **0.0% ASR** across 45 variants |
| Deterministic red-team gate | **0.0%** across 16 vectors |
| AGT (issue #5) | `agt lint-policy` clean · live `PolicyEngine` enforces allow/deny |
| MCP (issue #7) | Full protocol round-trip via the official SDK |
| Evaluation (issue #4) | Offline F1/Rouge produced with no API keys |

---

## 7. Run It Locally

```bash
python -m venv .venv && source .venv/Scripts/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt && pip install -e .
streamlit run cloudoptima/dashboard.py                  # demo mode by default — no keys needed
```

Test suite (optional extras activate the framework integrations):

```bash
pip install -e ".[dev,evaluation,redteam,governance,mcp]"
pytest                                        # 478 tests · 93% coverage
python scripts/redteam/redteam_cloudoptima.py --strict
python scripts/redteam/pyrit_redteam.py --strict
python scripts/evaluate/run_evaluation.py
```

---

## 8. Next Step — Approval

Everything above is pushed to **`dev`** for team + Punit review. On approval, Narendra
merges `dev` → `main` and we start **Phase 12 (Docker)**, followed by the Azure deployment
phases. The GitHub issue comments should point to this document for the complete
issue → resolution → roadmap story.
