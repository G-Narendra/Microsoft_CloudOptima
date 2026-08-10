# Automated Adversarial Testing (issue #3 — PyRIT / AI red teaming)

Runs attack payloads against CloudOptima's **real** defenses and reports
**Attack Success Rate (ASR)** per vector — the metric Microsoft's AI Red Team
uses. Every run is deterministic (no network, no LLM), so ASR is comparable
across commits and can be gated in CI.

## Run

```bash
cd /c/Users/naren/Desktop/Microsoft_CloudOptima
.venv/Scripts/python.exe scripts/redteam/redteam_cloudoptima.py
```

Gate in CI (fails when any vector's ASR ≥ 5%):

```bash
.venv/Scripts/python.exe scripts/redteam/redteam_cloudoptima.py --strict
```

## Known gaps

Cases marked `known_gap` are **reported but excluded from the strict gate** —
the mechanism stays for future soft vectors. Today the corpus has **no known
gaps**: the soft-tone indirect injections regex cannot reliably catch (e.g.
*"from now on you are..."*) are handled by the always-on offline floor in
`cloudoptima/safety.py` (issue #2) — no Azure credentials needed — and the
optional ML **Prompt Shield** adds ML-grade detection on top when Content
Safety is configured.

## Vectors covered

| Vector | Defense probed |
|---|---|
| jailbreak / role_switch / delimiter_forge | `detect_injection` + `clean_input` |
| homoglyph | Unicode confusable folding in `sanitize.py` |
| xss / sql / path_traversal | `clean_input` neutralization |
| rag_poison | RAG index-time drop (`compliance/rag.py`) + offline shield floor |
| harm | offline harm floor in `safety.py` (no credentials needed) |
| base64_blob | `scan_llm_output` base64 flag |
| rate_limit | `rate_limit` sliding window |

## PyRIT path (the real framework)

The deterministic harness runs with **zero dependencies** on purpose. When you
want **PyRIT itself** to drive the attacks:

```bash
pip install -e ".[redteam]"
python scripts/redteam/pyrit_redteam.py --strict
```

`pyrit_redteam.py` is a genuine PyRIT 0.14 integration, not a stub:

- a custom `PromptTarget` subclass routes every payload through CloudOptima's
  real defenses (the same `probe_payload` the deterministic harness uses),
- PyRIT's `UnicodeConfusableConverter` + `Base64Converter` obfuscate payloads
  the way PyRIT's AI Red Team does,
- PyRIT's built-in `SubStringScorer` computes the Attack Success Rate,
- PyRIT's `SQLiteMemory` persists the run.

**It finds real gaps:** the campaign surfaced that short base64-encoded
payloads bypassed length-based blob heuristics (31% ASR on converted
variants). The fix — decode-then-scan in `cloudoptima/sanitize.py` — is now
locked in by a `base64_short` case in the deterministic corpus, and the
campaign reports **0.0% ASR across all 45 variants**.

PyRIT 0.14 replaced orchestrators with attacks/executors; the converter →
target → scorer pipeline above is the framework's supported low-level flow.
