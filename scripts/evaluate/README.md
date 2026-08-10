# Quality Evaluation (issue #4 — Azure AI Evaluation SDK)

This harness scores the **real CloudOptima pipeline** on a golden dataset using
Microsoft's `azure-ai-evaluation` built-in evaluators. Unit tests prove the
pipeline is *well-formed*; these metrics prove the output is *good*
(grounded in the user's requirements, relevant, coherent, safe).

Two tiers, both using the real SDK:

1. **Offline metrics — always run, no judge needed.** `F1ScoreEvaluator` and
   `RougeScoreEvaluator` compare the pipeline's summary against each prompt's
   `golden_summary` (deterministic token overlap, 0–1). You get real numbers
   with zero API keys.
2. **Judge-model metrics — when configured.** `GroundednessEvaluator`,
   `RelevanceEvaluator`, `CoherenceEvaluator` plus the safety evaluators
   (`ViolenceEvaluator`, `HateUnfairnessEvaluator`, `SelfHarmEvaluator`,
   `SexualEvaluator`) graded by an Azure OpenAI judge model.

## Setup

```bash
cd /c/Users/naren/Desktop/Microsoft_CloudOptima
.venv/Scripts/activate
pip install -e ".[evaluation]"
```

Optionally configure the judge model in `.env` (the LLM that *grades* the
answers) to enable tier 2:

```dotenv
AZURE_OPENAI_ENDPOINT=https://<resource>.openai.azure.com/
AZURE_OPENAI_API_KEY=...
AZURE_OPENAI_EVAL_DEPLOYMENT=gpt-4o-mini
```

The pipeline under test uses your normal `LLM_PROVIDER` (defaults to the mock
client — set `nvidia` or `azure` for a real run).

## Run

```bash
python scripts/evaluate/run_evaluation.py
```

Output: mean **f1 / rouge** scores (always) plus **groundedness / relevance /
coherence / violence / hate_unfairness / self_harm / sexual** (with a judge),
a composite, and `scripts/evaluate/results/latest_eval.json` (with
`judge_used` so you can tell which tier ran).

## Extending

Add prompts to `eval_data.jsonl` (one JSON object per line with `query`,
`context`, and `golden_summary` fields). Keep it small — every prompt runs the
full pipeline plus one call per evaluator.
