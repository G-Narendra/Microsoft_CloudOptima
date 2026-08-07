# ☁️ Microsoft CloudOptima

> **Multi-Agent Cloud Architecture Designer** — Describe your infrastructure, and 5 AI agents collaborate to design, cost, secure, and validate your cloud deployment.

![Status](https://img.shields.io/badge/status-10_phases_complete-brightgreen)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![Streamlit](https://img.shields.io/badge/ui-streamlit-red)
![Azure](https://img.shields.io/badge/deploy-azure-blue)

---

## What This Is

Microsoft_CloudOptima is a multi-agent AI system that helps you design cloud architectures. Instead of clicking through Azure Portal for hours, you describe what you need and our AI team handles the rest:

1. **Architect Agent** — Designs compute, storage, network, and data tiers
2. **Cost Analyst Agent** — Estimates monthly costs and finds savings
3. **Security Engineer Agent** — Scans for vulnerabilities and risks
4. **Compliance Officer Agent** — Checks against regulations (PDPL, HIPAA, SOC2, etc.)
5. **Judge Agent** — Resolves disagreements between the specialists

**Output:** A complete architecture plan with IaC templates, cost breakdown, security report, and compliance status.

---

## 🚧 Current Status — Phases 0–10 Complete (incl. 7.5, 7.6, 8)

| Phase | Status |
|-------|--------|
| Phase 0 — Scaffolding | ✅ **Done** (package structure, config files, team setup) |
| Phase 1 — Config + Models | ✅ **Done** (type-safe Settings, domain models, enums, null byte sanitization) |
| Phase 2 — LLM Client + Cache | ✅ **Done** (MockClient, NvidiaClient, AzureClient, retry wrapper, gzip cache) |
| Phase 3 — Input Sanitization | ✅ **Done** (sanitization pipeline, JSON extraction, rate limiting) |
| Phase 4 — Base Agent Class | ✅ **Done** (BaseAgent template method, prompt hardening, caching, error turns) |
| Phase 5 — All 5 Agents | ✅ **Done** (Architect, Cost, Security, Compliance with 21 hardcoded rules, Judge) |
| Phase 6 — Orchestrator | ✅ **Done** (5-agent pipeline, 6-pair conflict detection, judge arbitration, 4 artifacts, IaC malware scan, CLI) |
| Phase 7 — Streamlit Dashboard | ✅ **Done** (input form, real progress bar, 4 result tabs, artifact downloads, session history, demo toggle) |
| Phase 7.5 — Cost-Aware LLM Routing | ✅ **Done** (cheapest-first providers, failover on 429s, smart/fast model tiers, spend guard, per-provider tracking) |
| Phase 7.6 — Multi-Provider Expansion | ✅ **Done** (OpenAI direct, Anthropic Claude, Google Gemini clients + price-tier routing, 4+ provider failover) |
| Phase 8 — Compliance & Pricing | ✅ **Done** (21 immutable rules module, compliance RAG, static price DB, live Azure Retail Prices API with 1h cache — cost analyst grounded with real prices + dashboard panel) |
| Phase 9 — Logging & Health Checks | ✅ **Done** (audit logging, @trace, health registry) |
| Phase 10 — Security | ✅ **Done** (output jailbreak scanning, anomaly detection, strict schemas, static pricing, rate limiting enforced, 27 penetration tests) |
| Phase 11–15 | 📅 Planned (11 is effectively done — 400 tests · 93% coverage) |

📋 **Full build checklist:** See [`docs/BUILD_CHECKLIST.md`](./docs/BUILD_CHECKLIST.md)

---

## 🛠️ Getting Started (For Team Members)

### Prerequisites

- **Python 3.11+** installed on your machine
- **Git** installed
- A **GitHub account** with access to this repo

### Setup Instructions

```cmd
:: Step 1 — Clone the repository
git clone https://github.com/G-Narendra/Microsoft_CloudOptima.git

:: Step 2 — Switch to the dev branch (all work happens here)
git checkout dev

:: Step 3 — Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate

:: Step 4 — Install dependencies
pip install -r requirements.txt

:: Step 5 — Install the package in editable mode
pip install -e .

:: Step 6 — Set up your environment variables
copy .env.example .env

:: Step 7 — Verify everything works
python -c "import cloudoptima; print('CloudOptima v' + cloudoptima.__version__)"
```

> **Note:** `chromadb` is optional — only needed for Phase 8 (Compliance RAG). Don't worry if you see it commented out in `requirements.txt`.

---

## Architecture Overview

```
User Input (Streamlit Form)
        │
        ▼
┌───────────────────┐
│   Orchestrator    │
│  ┌─────────────┐  │
│  │  Architect  │  │
│  │ Cost Analyst│  │
│  │  Security   │  │
│  │ Compliance  │  │
│  │   Judge     │  │
│  └─────────────┘  │
└────────┬──────────┘
         │
         ▼
   Results Dashboard
  (4 tabs: Overview,
   Agents, Conflicts,
   Artifacts)
```

### Multi-Agent Workflow

```
User describes infrastructure needs
        │
        ▼
┌─────────────────┐     ┌──────────────────┐
│   Architect     │────▶│  Cost Analyst    │
│ (designs system)│     │ (estimates cost) │
└────────┬────────┘     └────────┬─────────┘
         │                       │
         ▼                       ▼
┌─────────────────┐     ┌──────────────────┐
│   Security      │     │   Compliance     │
│ (finds risks)   │     │ (checks rules)   │
└────────┬────────┘     └────────┬─────────┘
         │                       │
         └───────────┬───────────┘
                     ▼
            ┌──────────────────┐
            │     Judge        │
            │ (resolves        │
            │  conflicts)      │
            └────────┬─────────┘
                     │
                     ▼
          Architecture Plan + 
          Cost Report + 
          Security Audit + 
          Compliance Check
```

---

## Tech Stack

| Layer | Choice | Why |
|-------|--------|-----|
| Language | Python 3.11+ | Great AI/ML ecosystem |
| UI | Streamlit | Fast to build, perfect for internal tools |
| LLMs | Nvidia NIM / Azure OpenAI / OpenAI / Anthropic Claude / Google Gemini | 5 providers behind one router — cheapest healthy wins, failover automatic |
| Data validation | Pydantic v2 | Type safety, JSON schema generation |
| LLM cache | SHA-256 + TTL | Don't repeat expensive API calls |
| Security | Custom sanitization | Input validation, injection prevention |
| Container | Docker | Consistent dev-to-prod |
| Cloud | Azure App Service | Student credits, free tier available |

### 💰 Cost-Aware LLM Routing (production)

Instead of pinning the app to one provider, set `ROUTING_ENABLED=true` and each
agent call is routed to the **cheapest enabled provider with credentials**, with
automatic failover:

- **Cheapest first** — Nvidia NIM's free tier ($0) is tried before paid Azure
- **Rate-limit-aware failover** — a provider that keeps failing (e.g. free-tier
  HTTP 429s) is demoted until it recovers, shifting load to the next provider
- **Quality tiers** — Architect & Judge run the `smart` model, the other
  specialists the cheaper `fast` model
- **Spend guard** — requests whose estimated input cost exceed
  `ROUTING_MAX_COST_PER_REQUEST` skip that provider
- **Spend tracking** — per-provider USD spend via the router's `stats()`

Default models: Nvidia NIM (free) `meta/llama-3.3-70b-instruct` smart /
`meta/llama-3.1-8b-instruct` fast; Azure OpenAI `gpt-4o-mini` for both tiers.

---

## Project Structure

```
Microsoft_CloudOptima/
│
├── .env.example              # Environment variable template
├── .gitignore                # Git ignore rules
├── pyproject.toml            # Project metadata + tool config
├── requirements.txt          # Python dependencies
├── README.md                 # This file
│
├── cloudoptima/              # Python package (all code lives here)
│   ├── __init__.py
│   ├── agents/               # 5 AI agents (Architect, Cost, Security, Compliance, Judge)
│   ├── compliance/           # Compliance agent — 21 hardcoded rules
│   ├── pricing/              # Static Azure price catalog (Phase 10)
│   └── tests/                # 349 tests · 93% coverage
│
└── docs/
    ├── BUILD_CHECKLIST.md    # Phase-by-phase task tracker
    └── DECISIONS.md          # Architecture decision log
```

---

## Security First

We're building security into every layer from day one:

- **Prompt injection defense** — Input delimiters, system prompt hardening, output scanning
- **Schema enforcement** — Every agent output validated against strict Pydantic models
- **Input sanitization** — XSS, SQL injection, null bytes, ANSI codes all stripped
- **Rate limiting** — Prevent abuse at every entry point
- **Audit logging** — Append-only logs, never modified after writing
- **Penetration testing** — Dedicated test suite for attack scenarios

See [`docs/BUILD_CHECKLIST.md`](./docs/BUILD_CHECKLIST.md) → Phase 10 for full details.

---

*Phases 0–10 complete — the full 5-agent pipeline runs through the Streamlit dashboard (real progress, 4 result tabs, downloadable artifacts). Compliance & pricing (Phase 8) bring immutable rules, RAG-guided checks, and live Azure prices; the router (7.5–7.6) spans five LLM providers with cheapest-first failover; Phase 10 hardening covers jailbreak scanning, anomaly detection, strict schemas, and enforced rate limiting. Ready for the deployment phases (12–14) and persistence/auth (15).*
