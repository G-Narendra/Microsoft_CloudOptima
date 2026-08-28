# ADR 0003: Shadow Mode for LLM Evaluation

## Status
Accepted

## Context
As foundation models evolve (e.g., GPT-4 to GPT-4o) or when fine-tuned models are introduced, replacing the active production model entails significant risk. Models may regress on specific tasks (e.g., generating Bicep code or strictly adhering to compliance schemas). We need a mechanism to test new models with real production traffic without impacting users.

## Decision
We will implement a **Shadow Mode (A/B Routing)** within our LLM Routing layer.
- A configurable `routing_shadow_mode_percent` will determine the probability of a prompt being routed to the shadow tier (e.g., a newer or experimental model).
- Shadow requests will be processed asynchronously. The orchestrator will primarily rely on the main tier response, but the shadow tier's response will be logged for offline comparison.
- In `CostAwareRouter`, if the shadow tier is invoked but fails, traffic seamlessly falls back to the main tier to ensure high availability.
- Offline tools (like RAGAS) will be used to compare the main vs. shadow responses to detect model drift or regressions before fully promoting the shadow model.

## Consequences
- **Positive**: Enables zero-downtime, risk-free evaluation of new models on live production data.
- **Negative**: Increases overall API costs and token usage when shadow mode is enabled, as requests are duplicated.
