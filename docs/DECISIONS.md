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
