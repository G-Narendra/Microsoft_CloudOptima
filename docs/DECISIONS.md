# Architecture Decision Log

> Record major decisions we made, so the team has context on why things were done a certain way.

| Date | Decision | Rationale | Decided By |
|------|----------|-----------|------------|
| Jul 2026 | Continue from Narendra's existing CloudOptima architecture rather than starting from scratch | Already had a proven multi-agent design; team would rebuild implementation phase-by-phase | Team + Punit Shah |
| Jul 2026 | `dev` branch is the working branch; `main` only receives reviewed, merged phases | Keeps stable history reviewable and prevents broken builds on main | Narendra |
| Jul 2026 | Python 3.11+, Pydantic v2, Streamlit, Mock/Nvidia/Azure LLM backends | Fast AI-native stack with a free mock path for demos and tests | Team |
| Jul 2026 | Every text field auto-strips null bytes; `extra="forbid"` on all models | LLM and user output must never smuggle unvalidated fields or control chars | Phase 1 |
| Jul 2026 | Single `BaseAgent` template method with delimiters + injection guard + caching + error turns | Security and caching must live in one place so subclasses cannot forget them | Phase 4 |
| Jul 2026 | Compliance agent embeds the 21 rules hardcoded in the prompt AND validation | The LLM must never invent, drop, or modify rules (AI-poisoning defense) | Phase 5 |
| Jul 2026 | Judge may override any recommendation but can never disable security controls | Hard safety invariant on the final output | Phase 5 |
| Jul 2026 | Deterministic 6-pair conflict detection keyed per pair | v1 bug: budget conflicts fired for every pair, tripling duplicates | Phase 6 |
| Jul 2026 | 4 artifacts generated deterministically; IaC malware-scanned before storage | Dashboard always renders a complete result set; exec/eval never reaches the UI | Phase 6 |
| Aug 2026 | Dashboard runs the pipeline in a background thread and polls `agent_turns` | Real progress bar — advances only when a turn actually finishes, never faked | Phase 7 |
| Aug 2026 | CLI reconfigures stdout to UTF-8 | Windows cp1252 consoles crashed printing Unicode artifact content | Phase 6 fix |
| Aug 2026 | Cost-aware LLM routing (Phase 7.5) | Production cost optimization — cheapest healthy provider first, failover on 429s, tiered models, spend guard + tracking | Narendra |
| Aug 2026 | Multi-provider expansion planned (Phase 7.6) | Router is provider-agnostic; add OpenAI direct, Anthropic, Google Gemini as drop-in clients with price-tiered routing — never vendor-locked to Nvidia | Narendra |
| Aug 2026 | Persistence + auth planned (Phase 15) | Sessions must survive restarts (DB) and the dashboard must require login before public deployment | Narendra |
| Aug 2026 | LLM outputs scanned for jailbreak/refusal/executable echoes before parsing (advisory); strict schema validation is the enforcement gate | Defense-in-depth — a compromised model leaves a forensic trail but can never inject output | Phase 10 |
| Aug 2026 | Per-agent EWMA anomaly detection on response length + token usage (flags >50% token drops) | Catches degraded models early without hardcoding "normal" sizes | Phase 10 |
| Aug 2026 | Pricing is an immutable static catalog (MappingProxyType); agents reject unknown services and extra JSON keys | AI-poisoning defense — the model can never invent prices or smuggle fields | Phase 10 |
| Aug 2026 | Rate limiting enforced inside Orchestrator.run BEFORE any LLM call (global hourly + per-session in-flight gate) | Throttled analysis costs zero API credits; concurrent CLI/UI calls cannot interleave a session | Phase 10 |
| Aug 2026 | CLI sanitizes input identically to the dashboard (single input contract across entry points) | Audit found `<script>` could sit in CLI sessions; both UIs now enforce the same contract | Phase 10 fix |
| Aug 2026 | The 21 compliance rules moved to `cloudoptima/compliance/rules.py` as the single immutable source; the agent imports them and renders them into the prompt | One definition, three uses (module → prompt → validation) can never drift | Phase 8 |
| Aug 2026 | Compliance RAG uses ChromaDB when installed, else a deterministic keyword-overlap retriever over the same corpus | chromadb's `chroma-hnswlib` wheel fails to build on Windows without a C++ toolchain; the public API is identical either way, so the pipeline never breaks | Phase 8 |
| Aug 2026 | Pricing split into `static_db.py` (read-only lookup/estimate) + `azure_api.py` (live Retail Prices API, 1h cache, static fallback) | Free no-auth live prices when online; offline always works; static catalog stays the validation authority | Phase 8 |
| Aug 2026 | OpenAI (direct), Anthropic Claude, and Google Gemini added as routed providers; price table covers all 5 providers; `ROUTING_PROVIDERS` registry expanded | Never vendor-locked — cheapest healthy provider wins with automatic failover | Phase 7.6 |
| Aug 2026 | New providers use httpx (Nvidia pattern) or the existing openai SDK; Gemini key rides in a header, never in the URL | Consistent, testable clients; keys never leak into proxy/access logs | Phase 7.6 |
