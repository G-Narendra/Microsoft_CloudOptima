# ☁️ Microsoft CloudOptima

> **Multi-Agent Cloud Architecture Designer** — Describe your infrastructure, and 5 AI agents collaborate to design, cost, secure, and validate your cloud deployment.

![Status](https://img.shields.io/badge/status-early--development-yellow)
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

## 🚧 Current Status — Phase 5 Complete

| Phase | Status |
|-------|--------|
| Phase 0 — Scaffolding | ✅ **Done** (package structure, config files, team setup) |
| Phase 1 — Config + Models | ✅ **Done** (type-safe Settings, domain models, enums, null byte sanitization) |
| Phase 2 — LLM Client + Cache | ✅ **Done** (MockClient, NvidiaClient, AzureClient, retry wrapper, gzip cache) |
| Phase 3 — Input Sanitization | ✅ **Done** (sanitization pipeline, JSON extraction, rate limiting) |
| Phase 4 — Base Agent Class | ✅ **Done** (BaseAgent template method, prompt hardening, caching, error turns) |
| Phase 5 — All 5 Agents | ✅ **Done** (Architect, Cost, Security, Compliance with 21 hardcoded rules, Judge) |
| Phase 6 — Orchestrator | 📅 Planned |
| Phase 7 — Streamlit Dashboard | 📅 Planned |
| Phase 9 — Logging & Health Checks | ✅ **Done** (audit logging, @trace, health registry) |
| Phases 8, 10–14 | 📅 Planned |

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
| LLMs | Nvidia NIM / Azure OpenAI | Free tier to start, scale when needed |
| Data validation | Pydantic v2 | Type safety, JSON schema generation |
| LLM cache | SHA-256 + TTL | Don't repeat expensive API calls |
| Security | Custom sanitization | Input validation, injection prevention |
| Container | Docker | Consistent dev-to-prod |
| Cloud | Azure App Service | Student credits, free tier available |

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
│   ├── compliance/           # Compliance rules (to be built)
│   ├── pricing/              # Pricing data (to be built)
│   └── tests/                # Test suite (to be built)
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

*Phase 5 complete — all five agents build structured, validated JSON. Ready for Phase 6 (orchestrator).*
