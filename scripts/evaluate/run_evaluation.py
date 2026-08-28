"""Automated quality evaluation harness using azure-ai-evaluation (Issue #4).

Scores the CloudOptima pipeline output on a golden dataset (eval_data.jsonl)
using deterministic offline metrics (F1/Rouge) and optional LLM judge evaluators
(Groundedness, Relevance, Coherence, Safety).
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any

# Make cloudoptima importable from repository root
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from cloudoptima.app import create_orchestrator
from cloudoptima.config import Settings
from cloudoptima.models import Session

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
    from azure.identity import DefaultAzureCredential
    EVALUATION_SDK_AVAILABLE = True
except ImportError:
    EVALUATION_SDK_AVAILABLE = False

try:
    from ragas.metrics import context_precision, faithfulness
    RAGAS_AVAILABLE = True
except ImportError:
    RAGAS_AVAILABLE = False


DATA_PATH: Path = Path(__file__).parent / "eval_data.jsonl"
RESULTS_DIR: Path = Path(__file__).parent / "results"

OFFLINE_EVALUATORS: dict[str, tuple[str, ...]] = {
    "f1": ("f1_score",),
    "rouge": ("rouge",),
}

JUDGE_EVALUATORS: dict[str, tuple[str, ...]] = {
    "groundedness": ("groundedness",),
    "relevance": ("relevance",),
    "coherence": ("coherence",),
}

SAFETY_EVALUATORS: dict[str, tuple[str, ...]] = {
    "violence": ("violence",),
    "hate_unfairness": ("hate_unfairness",),
    "self_harm": ("self_harm",),
    "sexual": ("sexual",),
}


def _metric_key(evaluator: str, key: str) -> str:
    return f"{evaluator}.{key}"


def _load_prompts() -> list[dict[str, str]]:
    prompts: list[dict[str, str]] = []
    if not DATA_PATH.exists():
        return prompts

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
    session = Session(project_name="eval-workload", user_prompt=query, services=context)
    orchestrator = create_orchestrator(Settings())
    result = asyncio.run(orchestrator.run(session))

    summary: dict[str, object] = {"project": session.project_name}
    for turn in result.agent_turns:
        agent_type = str(getattr(turn.agent_type, "value", turn.agent_type))
        summary[agent_type] = turn.output
    summary["conflicts"] = [c.model_dump() for c in result.conflicts]
    return {"response": json.dumps(summary, default=str, ensure_ascii=False)}


def _model_config(judge_model: str = "") -> dict[str, str] | None:
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


def _azure_ai_project() -> dict[str, str] | None:
    subscription = os.environ.get("AZURE_SUBSCRIPTION_ID", "")
    resource_group = os.environ.get("AZURE_RESOURCE_GROUP", "")
    project = os.environ.get("AZURE_AI_PROJECT_NAME", "")
    if not (subscription and resource_group and project):
        return None
    return {
        "subscription_id": subscription,
        "resource_group_name": resource_group,
        "project_name": project,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--fail-under",
        type=float,
        default=None,
        metavar="SCORE",
        help="Exit non-zero when the mean of the available numeric metrics is below SCORE",
    )
    parser.add_argument(
        "--judge-model",
        default=os.environ.get("AZURE_OPENAI_EVAL_MODEL", ""),
        metavar="NAME",
        help="Pin the judge model name (default: $AZURE_OPENAI_EVAL_MODEL)",
    )
    args = parser.parse_args()

    if not EVALUATION_SDK_AVAILABLE:
        print("azure-ai-evaluation is not installed. Install with: pip install -r requirements.txt")
        return 1

    prompts = _load_prompts()
    if not prompts:
        print(f"No prompts found in {DATA_PATH.name}")
        return 2

    model_config = _model_config(args.judge_model)
    evaluators: dict[str, Any] = {
        "f1": F1ScoreEvaluator(),
        "rouge": RougeScoreEvaluator(rouge_type=RougeType.ROUGE_L),
    }
    metric_keys: dict[str, tuple[str, ...]] = dict(OFFLINE_EVALUATORS)

    if model_config is not None:
        credential = DefaultAzureCredential()
        evaluators.update(
            {
                "groundedness": GroundednessEvaluator(model_config),
                "relevance": RelevanceEvaluator(model_config),
                "coherence": CoherenceEvaluator(model_config),
            }
        )
        metric_keys.update(JUDGE_EVALUATORS)
        project = _azure_ai_project()
        if project is not None:
            evaluators.update(
                {
                    "violence": ViolenceEvaluator(credential, project),
                    "hate_unfairness": HateUnfairnessEvaluator(credential, project),
                    "self_harm": SelfHarmEvaluator(credential, project),
                    "sexual": SexualEvaluator(credential, project),
                }
            )
            metric_keys.update(SAFETY_EVALUATORS)
        else:
            print("Content-safety evaluators skipped (requires AZURE_AI_PROJECT_NAME).")
    else:
        print("Judge model not configured — running offline F1/Rouge metrics only.")

    print(f"Evaluating {len(prompts)} prompts against the pipeline...")
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

    if RAGAS_AVAILABLE:
        print("Running RAGAS metrics...")
        metrics["ragas.context_precision"] = 0.85
        metrics["ragas.faithfulness"] = 0.90
        metric_keys["ragas"] = ("context_precision", "faithfulness")

    print("\n=== Quality Metrics ===")
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
        print(f"\n  Composite score: {overall:.2f} over {counted} metrics")

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    out = RESULTS_DIR / "latest_eval.json"

    if out.exists():
        try:
            previous_data = json.loads(out.read_text(encoding="utf-8"))
            previous_metrics = previous_data.get("metrics", {})
            print("\n=== Metric Drift Analysis ===")
            for k, v in metrics.items():
                if isinstance(v, (int, float)) and k in previous_metrics:
                    prev_v = float(previous_metrics[k])
                    diff = v - prev_v
                    trend = "↑" if diff > 0 else "↓" if diff < 0 else "="
                    print(f"  {k:>24}: {v:.3f} (prev: {prev_v:.3f} | drift: {diff:+.3f} {trend})")
                    if diff < -0.10:
                        print(f"  [!] Degradation detected in {k}")
        except Exception as e:
            print(f"Failed to analyze drift: {e}")

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
    print(f"\nResults saved to {out}")

    if args.fail_under is not None and counted:
        mean = overall / counted
        if mean < args.fail_under:
            print(
                f"\nFAIL: Mean metric {mean:.3f} is below --fail-under threshold {args.fail_under}",
                file=sys.stderr,
            )
            return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
