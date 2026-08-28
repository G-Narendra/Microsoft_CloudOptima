# CloudOptima — Engineering Build Checklist

> **Project Mission:** Build a production-grade multi-agent AI system that designs, prices, audits, and secures enterprise Azure architectures.
> **Core Stack:** Python 3.11+ · Streamlit · Pydantic v2 · Multi-Provider LLMs (Azure OpenAI, OpenAI, Anthropic, Gemini, Nvidia) · Azure AI Search · Docker · Azure App Service
> **Engineering Tracking:** See [`docs/PROGRESS_REPORT.md`](./PROGRESS_REPORT.md) and [`docs/adr/`](./adr/).

---

## Tracking Legend

| Status | Symbol | Meaning |
|---|---|---|
| Complete | `[x]` | Implemented, tested, and verified |
| In Progress | `[~]` | Actively being developed |
| Planned | `[ ]` | Scoped for upcoming milestone |
| Blocked | `[!]` | Blocked by external dependency |

---

## Phase 0: Project Scaffolding ✅ COMPLETE

- [x] Create Git repository with `dev` working branch and protected `main`
- [x] Configure `pyproject.toml` and `requirements.txt` with Python 3.11+ requirements
- [x] Establish package structure under `cloudoptima/` with typed module namespaces
- [x] Add `.gitignore` for virtual environments, secrets, caches, and build artifacts
- [x] Create `.env.example` defining all environment variables and secrets

---

## Phase 1: Configuration & Domain Models ✅ COMPLETE

- [x] Implement Pydantic `Settings` class in `cloudoptima/config.py` with `.env` loading
- [x] Enforce `SecretStr` for API keys (prevent credential leakage in logs and `__repr__`)
- [x] Build core domain models in `cloudoptima/models.py`: `Session`, `AgentTurn`, `Conflict`, `Artifact`
- [x] Define enums: `AgentType`, `WorkloadType`, `DeploymentScale`, `AzureRegion`, `ComplianceFramework`
- [x] Configure strict schema validation with `extra="forbid"` and automated null-byte removal

---

## Phase 2: LLM Client & Caching ✅ COMPLETE

- [x] Define abstract `BaseLLMClient` with `generate()` and async `agenerate()` interfaces
- [x] Implement `MockClient` for zero-cost local development and rapid test execution
- [x] Implement `AzureClient` supporting Azure OpenAI deployments and JSON-mode extraction
- [x] Build `create_llm_client()` factory with exponential backoff retry wrappers
- [x] Build `llm_cache.py` with SHA-256 keyed, gzip-compressed, TTL-expiring response caching

---

## Phase 3: Input & Output Sanitization ✅ COMPLETE

- [x] Build `clean_input()` to strip null bytes, control characters, and Unicode Bidi overrides (`U+202E`)
- [x] Build `clean_output()` to remove ANSI escapes and prevent prompt leakage
- [x] Build `detect_injection()` scanning for jailbreaks, DAN patterns, and role-override attacks
- [x] Implement robust `extract_json()` parser capable of extracting JSON from markdown fences
- [x] Add recursive Base64/ROT13/Atbash unscrambling (`decode_base64_tokens`) before scanning

---

## Phase 4: BaseAgent Core Architecture ✅ COMPLETE

- [x] Implement `BaseAgent` template method pattern in `cloudoptima/agents/agent_base.py`
- [x] Standardize execution loop: prompt creation → input sanitization → cache lookup → LLM call → output cleaning → schema validation → turn wrapping
- [x] Enforce strict prompt isolation with boundary delimiters
- [x] Implement structured error turns (`error_kind`: `llm`, `parse`, `validation`, `prompt_build`)

---

## Phase 5: The Five Specialist Agents ✅ COMPLETE

- [x] **Architect Agent:** Designs compute, storage, networking, and tier structures
- [x] **Cost Analyst Agent:** Calculates operational expenditures grounded in pricing data
- [x] **Security Engineer Agent:** Identifies threats, identity boundaries, and encryption rules
- [x] **Compliance Officer Agent:** Checks architectures against regulatory frameworks
- [x] **Judge Agent:** Evaluates pairwise conflicts with invariant that security controls cannot be overridden

---

## Phase 6: Orchestrator & CLI Pipeline ✅ COMPLETE

- [x] Implement `Orchestrator` in `cloudoptima/orchestrator.py` executing 5-agent pipeline
- [x] Implement pairwise conflict matrix checking all 6 agent pairings deterministically
- [x] Generate 4 production artifacts: IaC Bicep template, Cost Forecast, Compliance Matrix, Arbitration Summary
- [x] Build AST/regex malware scanner for generated IaC files (scanning for `exec()`, `os.system()`, command backticks)
- [x] Build CLI interface (`python -m cloudoptima.app`) with UTF-8 console output support

---

## Phase 7: Streamlit Interactive Dashboard ✅ COMPLETE

- [x] Build multi-tab Streamlit dashboard (`cloudoptima/dashboard.py`)
- [x] Implement non-blocking background thread execution with live polling of `agent_turns`
- [x] Provide dedicated tabs: Overview, Agent Turns, Conflict Arbitration, Artifact Downloads
- [x] Enforce end-to-end sanitization on all UI inputs and outputs

---

## Phase 7.5 & 7.6: Multi-Provider Intelligent Router ✅ COMPLETE

- [x] Build cost-aware LLM router in `cloudoptima/llm_routing.py`
- [x] Support 5 providers: Azure OpenAI, OpenAI (direct), Anthropic Claude, Google Gemini, Nvidia NIM
- [x] Implement quality tiers: Smart models for Architect/Judge, Fast models for Cost/Security/Compliance
- [x] Add automatic failover on HTTP 429 rate limits and provider health demotions
- [x] Implement budget spend guard and per-session cost tracking

---

## Phase 8: Compliance RAG & Real Azure Pricing ✅ COMPLETE

- [x] Define 21 immutable compliance rules in `cloudoptima/compliance/rules.py`
- [x] Integrate live **Azure Retail Prices API** (`cloudoptima/pricing/azure_api.py`) with 1-hour cache
- [x] Implement Azure AI Search RAG connector (`cloudoptima/compliance/rag.py`) with hybrid vector search
- [x] Ingest and chunk full 7-framework regulatory corpus from `corpus/` folder
- [x] Implement LLM query rewriting before vector retrieval for enhanced search precision

---

## Phase 9 & 10: Observability, Governance & Security Hardening ✅ COMPLETE

- [x] Implement `AuditLogger` with append-only daily JSONL logs and 90-day retention
- [x] Build `@trace` decorator and system health registry (`cloudoptima/health.py`)
- [x] Integrate **Agent Governance Toolkit (AGT)** `PolicyEngine` for runtime tool authorization
- [x] Integrate **Azure AI Content Safety** & REST Prompt Shields (`cloudoptima/safety.py`)
- [x] Implement **FastMCP** tool server (`cloudoptima/mcp_server.py`) and client bridge

---

## Phase 11: Testing, Scaling & Red Teaming ✅ COMPLETE

- [x] Build comprehensive unit & integration test suite covering all 29 test modules
- [x] Implement fully async concurrency: `BaseAgent.analyze()` and `Orchestrator.run()` coroutines with `asyncio.gather()`
- [x] Implement `RateLimitStore` protocol supporting `MemoryRateLimitStore` and `RedisRateLimitStore`
- [x] Refactor architecture with `AppContext` dependency injection container
- [x] Run Microsoft PyRIT red-teaming campaign achieving **0.0% Attack Success Rate (ASR)**

---

## Phase 12: Docker & Packaging 📅 PLANNED

- [ ] Build production multi-stage `Dockerfile` (`python:3.11-slim`)
- [ ] Configure container to run under non-root security context (`useradd cloudoptima`)
- [ ] Add container health check endpoint and verify `.dockerignore` excludes `.env` and secrets
- [ ] Package and expose FastMCP server endpoints

---

## Phase 13: Azure App Service & CI/CD Deployment 📅 PLANNED

- [ ] Provision Azure App Service (Linux, Python 3.11) under dedicated resource group
- [ ] Configure App Settings for runtime environment variables
- [ ] Build GitHub Actions CI/CD workflow running ruff, mypy, pytest, and PyRIT on push to `main`
- [ ] Verify automated deployment with production smoke tests

---

## Phase 14: Production Reliability & Monitoring 📅 PLANNED

- [ ] Connect Azure Monitor and Application Insights for live latency and telemetry tracking
- [ ] Configure Sentry integration for real-time error alerts
- [ ] Deploy Azure Cache for Redis for distributed multi-instance rate limiting
- [ ] Configure automated daily backup for audit log stores

---

## Phase 15: Persistence & Enterprise Identity 📅 PLANNED

- [ ] Integrate Microsoft Entra ID / Azure AD B2C login gate on Streamlit UI
- [ ] Migrate session state storage to Azure Cosmos DB / PostgreSQL
- [ ] Implement multi-tenant session isolation and role-based access controls
