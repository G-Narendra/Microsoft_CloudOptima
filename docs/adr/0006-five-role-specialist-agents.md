# ADR 0006: Five-Role Specialist Agent Decomposition

## Status
Accepted

## Context
Single monolithic LLM prompts attempting to design, price, audit security, and check compliance simultaneously suffer from severe hallucination and instruction omission. The prompt size exceeds the effective attention window for highly structured JSON output.

## Decision
Decompose cloud architecture evaluation into 5 distinct agent personas:
1. **Architect:** Compute, storage, and networking design.
2. **Cost Analyst:** Financial estimates grounded in live Retail APIs.
3. **Security Engineer:** Threat modeling and defense baselines.
4. **Compliance Officer:** Regulatory verification across full legal corpora.
5. **Judge:** Pairwise conflict arbitration.

**Invariant:** The Judge is strictly forbidden from overriding security controls.

## Consequences
- **Positive:** Specialized agents can use fast/cheap models (e.g. Gemini Flash) for specific tasks, while complex tasks (Architect) use reasoning models (GPT-4o).
- **Negative:** Requires an arbitration step (Judge) to resolve conflicting recommendations (e.g., Security demanding Premium tier vs Cost demanding Basic tier).
