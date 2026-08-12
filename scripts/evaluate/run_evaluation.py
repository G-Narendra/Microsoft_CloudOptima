"""Automated quality evaluation (issue #4) — azure-ai-evaluation.

Scores the *real* CloudOptima pipeline on the golden dataset
(``eval_data.jsonl``) with Microsoft's built-in evaluators. This answers the
critique that unit tests only check *format* — here we measure whether the
generated architecture is actually good, not just schema-valid.

Two tiers, both using the real ``azure-ai-evaluation`` SDK:

1. **Offline metrics (always run, no judge needed)** — ``F1ScoreEvaluator``
   and ``RougeScoreEvaluator`` compare the pipeline's summary against each
   prompt's ``golden_summary`` with deterministic token-overlap scores.
2. **Judge-model metrics (when configured)** — ``GroundednessEvaluator``,
   ``RelevanceEvaluator``, ``CoherenceEvaluator`` plus the safety evaluators
   (``ViolenceEvaluator``, ``HateUnfairnessEvaluator``, ``SelfHarmEvaluator``,
   ``SexualEvaluator``) using an Azure OpenAI judge model.

Requirements:
    - Optional extra: ``pip install -e ".[evaluation]"``
    - Judge model (tier 2 only): set AZURE_OPENAI_ENDPOINT,
      AZURE_OPENAI_API_KEY, and AZURE_OPENAI_EVAL_DEPLOYMENT in ``.env``.
    - The pipeline itself runs with the configured LLM_PROVIDER (defaults to
      the mock client — set nvidia/azure for a real run).

Usage:
    python scripts/evaluate/run_evaluation.py
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path

# Make `cloudoptima` importable when this script runs from any directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

DATA_PATH: Path = Path(__file__).parent / "eval_data.jsonl"
RESULTS_DIR: Path = Path(__file__).parent / "results"

#: Offline evaluators -> the metric keys they produce (always run).
OFFLINE_EVALUATORS: dict[str, tuple[str, ...]] = {
    "f1": ("f1_score",),
    "rouge": ("rouge",),
}

#: Judge-model evaluators -> metric keys (run when a judge is configured).
JUDGE_EVALUATORS: dict[str, tuple[str, ...]] = {
    "groundedness": ("groundedness",),
    "relevance": ("relevance",),
    "coherence": ("coherence",),
    "violence": ("violence",),
    "hate_unfairness": ("hate_unfairness",),
    "self_harm": ("self_harm",),
    "sexual": ("sexual",),
}


def _metric_key(evaluator: str, key: str) -> str:
    """The SDK namespaces aggregated metrics by evaluator (``f1.f1_score``)."""
    return f"{evaluator}.{key}"


def _load_prompts() -> list[dict[str, str]]:
    """Parse the golden dataset (one JSON object per line)."""
    prompts: list[dict[str, str]] = []
    for line in DATA_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            prompts.append(json.loads(line))
        except json.JSONDecodeError:
            print(f"warning: skipping malformed dataset line: {line[:60]}...")
    return prompts


def pipeline_target(query: str, context: str) -> dict[str, str]:
    """Run the real pipeline and return the summary the evaluators score.

    The summary is what a user would see in the dashboard: the architect's
    four-tier design, the cost estimate, security posture, and compliance
    status, serialized as JSON text. Evaluators compare it against the
    ``query``/``context`` (groundedness) and the row's ``golden_summary``
    (offline F1/Rouge), and rate relevance/coherence/safety. Extra data
    columns such as ``golden_summary`` are mapped straight from the dataset.
    """
    from cloudoptima.app import create_orchestrator
    from cloudoptima.config import Settings
    from cloudoptima.models import Session

    session = Session(project_name="eval-workload", user_prompt=query, services=context)
    orchestrator = create_orchestrator(Settings())
    # run() is async (round-3 P1) — this script is a plain sync process, so
    # asyncio.run bridges into the parallel pipeline.
    result = asyncio.run(orchestrator.run(session))

    summary: dict[str, object] = {"project": session.project_name}
    for turn in result.agent_turns:
        # use_enum_values stores list-of-enum items as plain strings, so
        # getattr tolerates both member and str forms.
        agent_type = str(getattr(turn.agent_type, "value", turn.agent_type))
        summary[agent_type] = turn.output
    summary["conflicts"] = [c.model_dump() for c in result.conflicts]
    return {"response": json.dumps(summary, default=str, ensure_ascii=False)}


def _model_config(judge_model: str = "") -> dict[str, str] | None:
    """Judge-model config from env; ``None`` when the judge is not configured.

    ``judge_model`` pins the judge model name (``AZURE_OPENAI_EVAL_MODEL``) so
    score drift from judge-model updates can never create phantom regressions
    — the same metric must come from the same judge (external review finding).
    """
    endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT", "")
    api_key = os.environ.get("AZURE_OPENAI_API_KEY", "")
    deployment = os.environ.get("AZURE_OPENAI_EVAL_DEPLOYMENT", "")
    if not (endpoint and api_key and deployment):
        return None
    config = {
        "azure_endpoint": endpoint,
        "api_key": api_key,
        "azure_deployment": deployment,
    }
    if judge_model:
        config["model"] = judge_model
    return config


def main() -> int:
    """Run the evaluation and write results to ``results/latest_eval.json``.

    ``--fail-under`` turns the harness into a CI gate: when the mean of the
    available numeric metrics drops below the threshold the script exits
    non-zero, so a quality regression blocks deployment instead of being
    reported in a JSON file nobody reads.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--fail-under",
        type=float,
        default=None,
        metavar="SCORE",
        help="exit non-zero when the mean of the available numeric metrics is below SCORE",
    )
    parser.add_argument(
        "--judge-model",
        default=os.environ.get("AZURE_OPENAI_EVAL_MODEL", ""),
        metavar="NAME",
        help="pin the judge model name (default: $AZURE_OPENAI_EVAL_MODEL)",
    )
    args = parser.parse_args()

    try:
        from azure.ai.evaluation import (
            CoherenceEvaluator,
            F1ScoreEvaluator,
            GroundednessEvaluator,
            HateUnfairnessEvaluator,
            RelevanceEvaluator,
            RougeScoreEvaluator,
            RougeType,
            SelfHarmEvaluator,
            SexualEvaluator,
            ViolenceEvaluator,
            evaluate,
        )
    except ImportError:
        print(
            "azure-ai-evaluation is not installed — run:\n"
            '    pip install -e ".[evaluation]"'
        )
        return 1

    prompts = _load_prompts()
    if not prompts:
        print(f"no prompts found in {DATA_PATH.name}")
        return 2

    model_config = _model_config(args.judge_model)
    evaluators: dict[str, object] = {
        "f1": F1ScoreEvaluator(),
        "rouge": RougeScoreEvaluator(rouge_type=RougeType.ROUGE_L),
    }
    metric_keys: dict[str, tuple[str, ...]] = dict(OFFLINE_EVALUATORS)
    if model_config is not None:
        evaluators.update(
            {
                "groundedness": GroundednessEvaluator(model_config),
                "relevance": RelevanceEvaluator(model_config),
                "coherence": CoherenceEvaluator(model_config),
                "violence": ViolenceEvaluator(model_config),
                "hate_unfairness": HateUnfairnessEvaluator(model_config),
                "self_harm": SelfHarmEvaluator(model_config),
                "sexual": SexualEvaluator(model_config),
            }
        )
        metric_keys.update(JUDGE_EVALUATORS)
    else:
        print(
            "Judge model not configured — running offline F1/Rouge metrics only. "
            "Set AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY and "
            "AZURE_OPENAI_EVAL_DEPLOYMENT in .env for groundedness/relevance/"
            "coherence + safety evaluation."
        )

    print(f"Evaluating {len(prompts)} prompts against the real pipeline...")
    result = evaluate(
        target=pipeline_target,
        evaluation_name="cloudoptima_quality",
        data=str(DATA_PATH),
        evaluators=evaluators,
        evaluator_config={
            "default": {
                "column_mapping": {
                    "query": "${data.query}",
                    "context": "${data.context}",
                    "response": "${target.response}",
                }
            },
            "f1": {
                "column_mapping": {
                    "response": "${target.response}",
                    "ground_truth": "${data.golden_summary}",
                }
            },
            "rouge": {
                "column_mapping": {
                    "response": "${target.response}",
                    "ground_truth": "${data.golden_summary}",
                }
            },
        },
    )

    metrics = result["metrics"]
    print("\n=== Quality metrics (0-5 scale for LLM judges, 0-1 for F1/Rouge) ===")
    overall = 0.0
    counted = 0
    for evaluator, keys in metric_keys.items():
        for key in keys:
            metric_key = _metric_key(evaluator, key)
            value = metrics.get(metric_key, "n/a")
            print(f"  {metric_key:>24}: {value}")
            if isinstance(metrics.get(metric_key), (int, float)):
                overall += float(metrics[metric_key])
                counted += 1
    if counted:
        print(f"\n  composite score: {overall:.2f} over {counted} metrics")

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    out = RESULTS_DIR / "latest_eval.json"
    out.write_text(
        json.dumps(
            {
                "metrics": metrics,
                "samples": len(prompts),
                "judge_used": model_config is not None,
                "judge_model": args.judge_model or None,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"\nResults written to {out}")

    # CI gate: fail when the mean of the available numeric metrics drops below
    # the threshold. Tracked baselines belong in the results JSON so Punit can
    # compare runs.
    if args.fail_under is not None and counted:
        mean = overall / counted
        if mean < args.fail_under:
            print(
                f"\nFAIL: mean metric {mean:.3f} is below --fail-under "
                f"{args.fail_under} — quality regression, gate blocked",
                file=sys.stderr,
            )
            return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
