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

## 🚧 Current Status

**We just started.** This repo has the plan and vision — code is being built phase by phase.

| Phase | Status |
|-------|--------|
| Planning & architecture | ✅ Complete |
| Config & data models | ⏳ Next up |
| Core engine | 📅 Planned |
| Streamlit dashboard | 📅 Planned |
| Azure deployment | 📅 Planned |

📋 **Full build checklist:** See [`BUILD_CHECKLIST.md`](./docs/BUILD_CHECKLIST.md)

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
| Language | Python 3.11+ | great AI/ML ecosystem |
| UI | Streamlit | Fast to build, perfect for internal tools |
| LLMs | Nvidia NIM / Azure OpenAI | Free tier to start, scale when needed |
| Data validation | Pydantic v2 | Type safety, JSON schema generation |
| LLM cache | SHA-256 + TTL | Don't repeat expensive API calls |
| Security | Custom sanitization | Input validation, injection prevention |
| Container | Docker | Consistent dev-to-prod |
| Cloud | Azure App Service | Student credits, free tier available |

---

## Getting Started (Once We Build)

```bash
# Clone
git clone https://github.com/G-Narendra/Microsoft_CloudOptima.git
cd Microsoft_CloudOptima

# Set up
python -m venv venv
venv\Scripts\activate     # On Mac OS: source venv/bin/activate
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env with your settings (demo mode works out of the box)

# Run
streamlit run Microsoft_CloudOptima/dashboard.py
```

> **No API key needed to start** — demo mode uses mock data and runs instantly.

---

## Project Structure

```
Microsoft_CLoudOptima/
├── config.py              # App settings & env vars
├── models.py              # Data types (Session, AgentTurn, etc.)
├── llm_client.py          # LLM providers (mock, Nvidia, Azure)
├── llm_cache.py           # Response caching
├── agent_base.py          # Base agent class
├── sanitize.py            # Input/output cleaning
├── observability.py       # Logging & tracing
├── health.py              # Health checks
├── orchestrator.py        # Multi-agent pipeline
├── dashboard.py           # Streamlit UI
├── agents/                # 5 AI agents
├── compliance/            # Compliance rules + RAG
├── pricing/               # Cost data + APIs
└── tests/                 # Test suite
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

See [`BUILD_CHECKLIST.md`](./docs/BUILD_CHECKLIST.md) → Phase 10 for full details.

---


## Team

Built by a student team collaborating with Microsoft engineers. This project started as an industry-academia collaboration to explore multi-agent AI systems for cloud architecture Optimization.

---

*Early stage — everything is a work in progress. Check the build checklist for what's being built next.*
