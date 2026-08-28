# ADR 0008: Defense-in-Depth Security & Red Teaming (0.0% ASR Gate)

## Status
Accepted

## Context
AI agents handling user infrastructure inputs are vulnerable to direct and indirect prompt injection, Base64 smuggling, and encoding obfuscations.

## Decision
Implement a layered defense model:
1. **Input Sanitization:** Auto-strip null bytes, control characters, and bidirectional (Bidi) Unicode overrides (`U+202E`).
2. **Recursive Decode-and-Scan:** Decode Base64, ROT13, and Atbash transformations before scanning for injection patterns.
3. **Enterprise Prompt Shields:** Azure AI Content Safety ML integration via REST `text:shieldPrompt`.
4. **Immutable Compliance Rules:** 21 hardcoded rules embedded in prompts and validation logic to prevent model drift.
5. **CI Gating:** Automated PyRIT campaigns and deterministic red-team suites must achieve an Attack Success Rate (ASR) of 0.0%.

## Consequences
- **Positive:** Enterprise-grade security verified against adversarial simulation. 
- **Negative:** Slight latency overhead on input ingestion to process multi-layer security scans.
