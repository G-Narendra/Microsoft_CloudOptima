# CloudOptima — Developer & Teammate Setup Guide

> **Welcome to CloudOptima!** This guide provides step-by-step instructions for getting the system running on your local machine, configuring external LLM providers, and deploying or connecting to the full Azure Enterprise stack.

---

## 1. Quick Orientation

CloudOptima is designed with **graceful fallback** across all layers. You can run and test the complete system locally without an Azure subscription or external API keys, or connect it to production Azure resources when ready.

| Environment Mode | Required Credentials | Capabilities | Typical Use Case |
|---|---|---|---|
| **Local Development (Mock / Offline)** | None (zero API keys needed) | Full 5-agent pipeline, deterministic mock responses, keyword RAG, offline security filters, all unit tests pass (<2s) | Fast feature development, UI tweaks, local unit & integration testing |
| **Local Development with Multi-Provider LLMs** | Any one LLM API key (OpenAI, Anthropic, Gemini, or Nvidia) | Real LLM generation, smart/fast model routing, live Azure Retail Prices API, local semantic RAG | Prompt engineering, live architecture generation, cost analysis validation |
| **Enterprise Azure Stack** | Azure OpenAI + Azure AI Search + Content Safety | Production Azure deployments, hybrid vector search with semantic re-ranking over 7 regulatory frameworks, Azure Content Safety Prompt Shields, AGT governance | Full enterprise compliance auditing, security red teaming, cloud deployment |

---

## 2. Installation & Scaffolding

### Prerequisites
- **Python 3.11+** (Python 3.11 or 3.12 recommended)
- **Git**
- **PowerShell** (Windows) or **bash/zsh** (Linux / macOS)

### Step-by-Step Installation

#### On Windows (PowerShell):
```powershell
# 1. Clone the repository and switch to the working branch
git clone https://github.com/G-Narendra/Microsoft_CloudOptima.git
cd Microsoft_CloudOptima
git checkout dev

# 2. Create and activate a Python virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 3. Install core dependencies
pip install -r requirements.txt

# 4. Install the package in editable mode
pip install -e .

# 5. Create your local environment configuration file
Copy-Item .env.example .env
```

#### On Linux / macOS (bash/zsh):
```bash
# 1. Clone and checkout
git clone https://github.com/G-Narendra/Microsoft_CloudOptima.git
cd Microsoft_CloudOptima
git checkout dev

# 2. Virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install requirements
pip install -r requirements.txt
pip install -e .

# 4. Environment setup
cp .env.example .env
```

---

## 3. Running in Local Development (Mock / Offline Mode)

In this mode, CloudOptima uses deterministic mock backends and local static pricing databases. No API calls are made, and no billing is incurred.

1. Ensure your `.env` has:
   ```dotenv
   DEMO_MODE=true
   LLM_PROVIDER=mock
   ```

2. **Launch the Streamlit Interactive Dashboard:**
   ```powershell
   streamlit run cloudoptima/dashboard.py
   ```
   Open your browser at `http://localhost:8501`. You can toggle between different architecture workloads, configure budgets and regions, and view the generated IaC templates, cost forecasts, security findings, and compliance checks.

3. **Run via the Command Line Interface (CLI):**
   ```powershell
   python -m cloudoptima.app --project "E-Commerce Cloud" --workload realtime --budget 5000 --region eastus --compliance HIPAA
   ```

4. **Run the Full Test Suite:**
   ```powershell
   pytest cloudoptima/tests/ -v
   ```

---

## 4. Running with External LLM Providers

If you have API keys from OpenAI, Anthropic, Google Gemini, or Nvidia NIM, you can run CloudOptima with live generative models while still operating locally.

1. Open `.env` and configure:
   ```dotenv
   DEMO_MODE=false
   LLM_PROVIDER=openai   # Options: openai | anthropic | gemini | nvidia | azure
   ```

2. Add your provider's API key:
   ```dotenv
   # For OpenAI:
   OPENAI_API_KEY=sk-...
   OPENAI_MODEL_NAME=gpt-4o
   OPENAI_FAST_MODEL_NAME=gpt-4o-mini

   # For Anthropic:
   ANTHROPIC_API_KEY=sk-ant-...

   # For Google Gemini:
   GOOGLE_API_KEY=AIzaSy...

   # For Nvidia NIM:
   NVIDIA_API_KEY=nvapi-...
   ```

3. **Cost-Aware Routing:** When multiple keys are present, the built-in LLM router (`cloudoptima/llm_routing.py`) will automatically select the cheapest healthy model, handle automated failovers on HTTP 429 rate limits, and assign reasoning-tier models to the Architect/Judge while assigning fast-tier models to specialist agents.

---

## 5. Setting up the Enterprise Azure Stack

To run CloudOptima with the complete Microsoft Enterprise Stack (Azure OpenAI, Azure AI Search, and Content Safety):

### 5.1 Azure Credentials in `.env`
Update your `.env` with your Azure resource credentials:

```dotenv
DEMO_MODE=false
LLM_PROVIDER=azure

# Azure OpenAI
AZURE_OPENAI_ENDPOINT=https://<your-resource-name>.openai.azure.com/
AZURE_OPENAI_API_KEY=<your-azure-openai-key>
AZURE_OPENAI_API_VERSION=2024-02-01
AZURE_OPENAI_DEPLOYMENT=<your-chat-deployment-name>            # e.g., gpt-4o
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=<your-embedding-deployment> # e.g., text-embedding-3-large

# Azure AI Search
AZURE_SEARCH_ENDPOINT=https://<your-search-service>.search.windows.net
AZURE_SEARCH_API_KEY=<your-search-admin-key>
AZURE_SEARCH_INDEX_NAME=compliance-index

# Azure AI Content Safety (Optional ML Prompt Shield)
AZURE_CONTENT_SAFETY_ENDPOINT=https://<your-content-safety>.cognitiveservices.azure.com/
AZURE_CONTENT_SAFETY_KEY=<your-content-safety-key>
```

### 5.2 Provisioning the Azure AI Search Index
Run the automated schema provisioning script to configure the `compliance-index` with vector search support:

```powershell
python setup_azure_index.py
```

### 5.3 Vectorizing and Seeding the Regulatory Corpus
Ingest the full regulatory corpus (GDPR, HIPAA, ISO-27001, NIST, PCI-DSS, PDPL, SOC 2) into Azure AI Search:

```powershell
python seed_azure.py
```
*Note: This script chunks the markdown documents in the `corpus/` folder, filters injection attacks, generates embeddings via Azure OpenAI, and batch-uploads them to Azure AI Search.*

---

## 6. Running Security & Quality Tools

### 6.1 PyRIT AI Red Teaming Campaign
To run Microsoft's Python Risk Identification Tool (PyRIT) against the agent pipeline:

```powershell
python scripts/redteam/pyrit_redteam.py
```
*Validates that obfuscated prompt injection attacks (Base64, ROT13, Atbash, Leetspeak, Bidi controls) achieve an Attack Success Rate (ASR) of 0.0%.*

### 6.2 Azure AI Evaluation Harness
To run automated quality scoring (groundedness, relevance, coherence, F1, and Rouge metrics):

```powershell
python scripts/evaluate/run_evaluation.py
```

### 6.3 Model Context Protocol (MCP) Server
To start the FastMCP tool server:

```powershell
python -m cloudoptima.mcp_server
```

---

## 7. Troubleshooting & Common Pitfalls

| Issue | Cause | Resolution |
|---|---|---|
| `UnicodeEncodeError: 'charmap' codec can't encode...` | Windows console defaults to cp1252 | Ensure Python runs with UTF-8 encoding: set `$env:PYTHONIOENCODING="utf-8"` in PowerShell. |
| `Azure Search 400 Bad Request (Invalid document key)` | Document ID contains spaces or invalid characters | Ensure IDs are encoded with URL-safe Base64 (`base64.urlsafe_b64encode(id.encode()).decode()`). (Handled in `rag.py`). |
| `HTTP 404 DeploymentNotFound` on Azure OpenAI | Deployment name in `.env` doesn't match the deployment in Azure OpenAI Studio | Double-check `AZURE_OPENAI_DEPLOYMENT` and `AZURE_OPENAI_EMBEDDING_DEPLOYMENT` against your Azure OpenAI portal. |
| `429 Too Many Requests` | LLM rate limits reached | The built-in router will automatically try secondary providers. You can also switch `LLM_PROVIDER=mock` for testing. |
| `ModuleNotFoundError: No module named 'cloudoptima'` | Package not installed in editable mode | Run `pip install -e .` from the project root. |
