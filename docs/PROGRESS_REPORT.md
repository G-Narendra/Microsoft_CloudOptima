# CloudOptima — Team Progress Report

> **Branch:** `dev` · **Date:** August 2026
> **Team:** Narendra (lead) · Andrew · Ivan
> **Microsoft reviewer:** Punit Shah
>
> **One line:** Phases 0–11 are complete in practice (**527 tests · 92.62% coverage · mypy & ruff clean**),
> all **six of Punit's GitHub issues (#2–#7)** are implemented with the **real Microsoft
> frameworks** (not look-alikes), an **independent external principal-engineer review**
> scored the project 7.5/10 and every finding is fixed, and the remaining roadmap is
> clear: **Phases 12–15** (Docker → Azure deploy → production → persistence & auth).

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
| **#3** | PyRIT + AI Red Teaming at scale | `pyrit` 0.14 — custom `PromptTarget`, converters (UnicodeConfusable, Base64, Flip, ROT13, Atbash, Leetspeak, Bidi), `SubStringScorer`, `SQLiteMemory` | Campaign drives **119 strict variants → 0.0% ASR** (leet-of-base64 = documented known gap) — it *found real gaps* each round (short-base64 smuggling, Flip/ROT13 bypasses, then Atbash/leet/Bidi) and we fixed them |
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

- **PyRIT campaign: 0.0% ASR on 119 strict variants** (leet-of-base64 reported as the one documented known gap)
- **Deterministic red-team gate: 0.0% (16 vectors)**
- **Zero false positives** on legitimate Base64 (e.g. `"US--Canada 0--9"` passes)

### Every integration degrades gracefully

The pattern we used for pricing holds everywhere: **when the optional package or API key is
absent, the app behaves exactly as before** (offline mirror / regex floor). CloudOptima never
breaks without an Azure resource — demo mode and tests still work with the mock provider.

## 2.5 External Principal-Engineer Review — Scorecard → Fixes

> An independent reviewer (a senior Azure AI engineer acting as an external reviewer, not
> the project's official Microsoft reviewer) audited the entire repo and scored it
> **7.5 / 10 overall** — the strongest areas were documentation (9), code quality (8.5) and
> security (8); production readiness (4) was the weak point. Every actionable finding is
> fixed and covered by regression tests.

| Reviewer score | Finding | What we did |
|---|---|---|
| Security 8 → | `Settings.__repr__` leaked the first 3 chars of API keys | All secrets render as `***REDACTED***` — not even a prefix leaks (tests assert it) |
| Code quality | Backtick regex flagged every Markdown inline-code span as command substitution | Scanner now only flags shell-looking backticks (operators, `$()`, command words); Markdown passes |
| Issue #7 follow-up | Tool args never validated; no timeout on tool execution | Args validated against the declared schema (missing/typed-wrong rejected); 15s execution timeout via a daemon thread |
| Responsible AI 7 → | All harm categories treated identically | `severity_action`: pass (0) / log (1–3) / block (≥threshold) / escalate (6); verdicts carry `max_severity` |
| Responsible AI | ML safety was opt-in (`content_safety_enabled=False` default) | **Fail closed:** `create_orchestrator` refuses to start in production mode (`demo_mode=false`) without Content Safety |
| Architecture 7.5 → | No error taxonomy — "LLM down" vs "bad output" indistinguishable | Error turns carry `error_kind` (llm / parse / validation / prompt_build); the orchestrator audits failed turns with the reason |
| Issue #5 | (Verified present) governance audit trail logs every decision; YAML↔Python sync test exists | Confirmed in `test_governance.py`; documented here for discoverability |
| Issue #4 | Eval was a script, not a gate; judge model unpinned | `--fail-under` exits non-zero on regression; judge pinned via `AZURE_OPENAI_EVAL_MODEL` |
| Issue #3 | Only 2 converters; regex boundaries unstressed | **Flip + ROT13 converters added — they found 3 real bypasses** (jailbreak/role-switch/RAG-poison under Flip, ROT13, and flip/ROT13-of-base64). Fixed with involution unscrambling (`obfuscated_forms` + `decoded_base64_forms`); the round-2 campaign added Atbash/Leetspeak/Bidi and found 5 more — now **119 strict variants → 0.0% ASR** |
| Production 4 → | No container, no CI/CD, no auth | `Dockerfile` (multi-stage, non-root, healthcheck) + `.dockerignore`; `.github/workflows/ci.yml` (ruff · mypy · pytest · red-team strict · PyRIT · eval · AGT lint · MCP smoke; Azure deploy on main); Phase 15 auth scaffold (`AUTH_*` config + dashboard login gate) |
| Production | Sessions/rate-limits/anomaly baselines in-memory | Documented Phase 15 plan: Cosmos/Postgres sessions, Redis rate limits, Key Vault secrets (deployment-phase work) |

### Round 2 — The Reviewer's Follow-up (8.8/10 after fixes)

> The reviewer re-scored **7.5 → 8.8/10** after round 1, then ran the campaign again with
> the converters we had just added and **found 5 more bypasses** (Atbash, leetspeak, Bidi).
> Same loop, third time: red-team → fix → regression-test. Numbers below are verified on this machine.

| Finding | What they said | What we did |
|---|---|---|
| **P0 — Bidi control chars** | `U+202E` RLO renders a backwards payload as an instruction; NFKC preserves it | `_BIDI_CONTROL` regex strips `[\u202A-\u202E \u2066-\u2069]` in both `clean_input` and `clean_output` |
| **Atbash (letters + digits)** | Another involution PyRIT ships; our fold missed digit complement (0↔9), so atbash(b64(x)) stayed undecodable | `_ATBASH_TABLE` now mirrors PyRIT exactly (A–Z + 0–9); `obfuscated_forms` closed under 2 transform rounds → atbash-of-base64 unwraps |
| **Leetspeak symbols** | PyRIT maps c→( — `1n57ru(710n5` never folded to "instructions" | Fold tables cover `(` → c and both ambiguous `1` resolutions (i-variant + l-variant) |
| **Leetspeak i/l collision** | "helpful assistant" mixes i and l, so no global fold recovers it | Whole-phrase leet-tolerant regexes (`_LEET_PHRASE_PATTERNS` in sanitize + `_OFFLINE_HARM_LEET` in safety floor) — each letter matches itself or its PyRIT substitution |
| **Leet-of-base64** | Genuinely undecodable: PyRIT maps letters to digits, base64 already contains digits | Reported honestly as a **known gap** in the campaign (same policy as the deterministic harness's `AttackCase.known_gap`); closed in production by the mandatory ML Content Safety layer |
| **P1 async / P2 Redis** | Reviewer explicitly deferred both for a student project | **Done in round 3** — see below |

**Round-2 results:** PyRIT campaign is now **119 strict variants → 0.0% ASR** (leet-of-base64 reported as the single known gap), plus the original 16-vector deterministic harness at 0.0%. Total suite **527 tests · 92.62% coverage**. mypy + ruff clean.

### Round 3 — The Scaling Review (9.0/10)

> "You are acting like a brilliant security researcher and a junior software
> engineer. You nailed the complex mathematical defenses, but you failed to
> build a system that can actually scale to 1,000 concurrent enterprise users."
> — the reviewer, re-scoring **8.8 → 9.0/10** and capping Architecture at 8.5
> and Production Readiness at 8.5 until the scaling homework was done.

| Homework | What they said | What we did |
|---|---|---|
| **P1 — async pipeline** | `def analyze` / `def run` block on LLM network I/O; 4 users on 4 threads = lockup; "synchronous LLM pipelines are an instant PR rejection" | `BaseAgent.analyze` and `Orchestrator.run` are now real coroutines. Every client got `agenerate()`: httpx.AsyncClient for Nvidia/Anthropic/Gemini, `AsyncAzureOpenAI`/`AsyncOpenAI` for Azure/OpenAI, async sleep for Mock. `generate_with_retry` gained an async twin (`agenerate_with_retry` with `await asyncio.sleep`). The three specialists that only depend on the architect run **concurrently** via `asyncio.gather` — a peak-concurrency test proves all three overlap |
| **P2 — rate limiting** | In-memory dict = 60/hour becomes 180/hour across 3 workers; "move it to Redis, or at least write an interface" | `RateLimitStore` protocol + `MemoryRateLimitStore` (default) + `RedisRateLimitStore` (INCR/EXPIRE, lazy redis import, injectable client for tests). `Settings.rate_limit_backend` (`memory`/`redis`) + `redis_url`; `build_rate_limiter()` maps config → store; `RateLimiter` is injected into the orchestrator |
| **P3 — singleton abuse** | Module globals (`_audit_logger`, `_anomaly_detector`, `_LIMITER`) break test isolation and multi-tenant scale; "pass a Context or Dependencies container around" | New `cloudoptima/context.py` — `AppContext` owns settings, llm client, audit logger, anomaly detector, and rate limiter. `Orchestrator.from_settings` builds it and injects the instances into every agent (agent constructor gained an optional `context=`). Module-level getters remain only as a fallback for direct construction |

**Round-3 results (verified on this machine):** 540 tests pass (527 + 13 new scaling tests) · **90.19% coverage** · mypy + ruff clean · both red-team gates still 0.0% ASR. The async pipeline runs the 5-agent flow in **~0.5s warm** (the ~14s first-run cost is the cost analyst's real Azure Retail Prices API fetch — 12 live HTTP calls, cached afterwards, exactly the "no mock data" requirement).

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
| 11 | Testing + **Punit's issues #2–#5** (Responsible AI) | ✅ Complete in practice — 527 tests · 92.62% coverage (85% gate); leftover: judge-model baseline scores | Narendra + team review |
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
  (verbose + coverage + **85% fail-under gate**), 527 tests, per-file coverage ≥90% on
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
| Unit/integration tests | **540 passed · 0 failed** (478 before the review fixes) |
| Coverage | **90.19% overall** (gate 85%) · tools/registry 100% · sanitize 99% · orchestrator 93% |
| mypy | Clean across the package |
| ruff | Clean (`cloudoptima/` + `scripts/`) |
| PyRIT campaign (issue #3) | **0.0% ASR** across **119 strict variants** (Flip, ROT13, Atbash, Leetspeak, Bidi, UnicodeConfusable, Base64 converters; leet-of-base64 = documented known gap) |
| Deterministic red-team gate | **0.0%** across 16 vectors |
| AGT (issue #5) | `agt lint-policy` clean · live `PolicyEngine` enforces allow/deny |
| MCP (issue #7) | Full protocol round-trip via the official SDK |
| Evaluation (issue #4) | Offline F1/Rouge produced with no API keys; `--fail-under` gate ready |
| External review (11.7–11.8) | Rounds 1–3: every finding fixed + regression-tested · **7.5 → 8.8 → 9.0/10** · Dockerfile + CI + auth scaffold + async + DI + Redis |
| Async pipeline (round-3 P1) | `analyze`/`run` are coroutines; peak-concurrency test proves the 3 specialists overlap via `asyncio.gather` |
| Rate-limit stores (round-3 P2) | `MemoryRateLimitStore` + `RedisRateLimitStore` (fake-client tested) behind one `RateLimiter` |
| Dependency injection (round-3 P3) | `AppContext` owned by the orchestrator; two contexts verified fully isolated |

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
pytest                                        # 540 tests · 90.19% coverage
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
