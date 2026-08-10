"""PyRIT-native red teaming (issue #3) — the real framework drives the attack.

The deterministic harness (``redteam_cloudoptima.py``) is the CI gate:
identical payloads, zero dependencies. This script is the *framework* path —
it runs the same attack corpus through **PyRIT 0.14's own components**:

- a custom :class:`PromptTarget` subclass that routes every payload through
  CloudOptima's real defenses (input sanitizer, injection detector, output
  scanner, RAG index filter, offline safety floor, Prompt Shields),
- PyRIT's ``UnicodeConfusableConverter`` + ``Base64Converter`` to obfuscate
  payloads exactly the way PyRIT's AI Red Team does,
- PyRIT's built-in :class:`SubStringScorer` scoring each response as attack
  success or blocked, producing the Attack Success Rate (ASR),
- PyRIT's ``SQLiteMemory`` to persist the run.

PyRIT 0.14 ships attacks/executors instead of the old orchestrators; the
converter -> target -> scorer pipeline below is the framework's supported
low-level flow, and ``probe_payload`` (imported from the deterministic
harness) is the scoring ground truth both paths share.

Usage:
    python scripts/redteam/pyrit_redteam.py            # full campaign
    python scripts/redteam/pyrit_redteam.py --strict   # fail on ASR >= 5%
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path
from typing import Any

# Make `cloudoptima` and the sibling harness importable from any directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from redteam_cloudoptima import ATTACK_CASES, STRICT_ASR_LIMIT, probe_payload  # noqa: E402

# Guarded import: pyrit is an optional dependency (extra `redteam`).
try:  # pragma: no cover - exercised only when pyrit is installed
    from pyrit.memory import CentralMemory, SQLiteMemory
    from pyrit.models import Message, MessagePiece
    from pyrit.prompt_converter import Base64Converter, UnicodeConfusableConverter
    from pyrit.prompt_target import PromptTarget
    from pyrit.score import SubStringScorer

    PYRIT_AVAILABLE = True
except Exception:  # pragma: no cover - exercised only when pyrit is missing
    PYRIT_AVAILABLE = False


class CloudOptimaTarget(PromptTarget):  # type: ignore[misc] - guarded import above
    """PyRIT ``PromptTarget`` — routes each payload through CloudOptima's defenses.

    The response text is ``BLOCKED:<defense>`` when a defense fired, or
    ``PASSED`` when the payload would have reached output. The ASR scorer
    keys off exactly this contract.

    PyRIT 0.14 requires subclasses to implement
    ``_send_prompt_to_target_async`` (the public ``send_prompt_async``
    handles validation + normalization and must not be overridden).
    """

    async def _send_prompt_to_target_async(  # type: ignore[override]
        self,
        *,
        normalized_conversation: list[Message],
    ) -> list[Message]:
        # The current request is the last message of the normalized conversation.
        text = normalized_conversation[-1].get_value()
        blocked, defense = probe_payload(text)
        verdict = f"BLOCKED:{defense}" if blocked else "PASSED"
        piece = MessagePiece(
            role="assistant",
            original_value=verdict,
            converted_value=verdict,
        )
        return [Message(message_pieces=[piece])]


def _attack_success_scorer() -> Any:
    """PyRIT scorer for the campaign: True when a payload reached output.

    The target answers ``PASSED`` exactly when the payload would have reached
    output, so PyRIT's built-in ``SubStringScorer`` scoring that substring is
    the ASR signal — a real framework scorer, zero custom abstract plumbing.
    """
    return SubStringScorer(substring="PASSED", categories=["attack_success"])


async def run_campaign(limit: int | None = None) -> list[dict[str, Any]]:
    """Drive the attack corpus through PyRIT; return one row per variant.

    Args:
        limit: Cap the number of attack cases (used by tests for speed).

    Returns:
        Rows with ``vector``, ``payload``, ``variant``, ``blocked``, ``passed``.
    """
    # PyRIT 0.14 requires a central memory instance before any target exists.
    memory = SQLiteMemory(db_path=str(Path(__file__).parent / "pyrit_memory.db"))
    CentralMemory.set_memory_instance(memory)

    target = CloudOptimaTarget()
    scorer = _attack_success_scorer()
    converters: list[Any] = [
        UnicodeConfusableConverter(deterministic=True),
        Base64Converter(),
    ]
    rows: list[dict[str, Any]] = []
    cases = list(ATTACK_CASES) if limit is None else list(ATTACK_CASES)[:limit]
    try:
        for case in cases:
            # PyRIT-native conversion pipeline: raw + every converter variant.
            variants: list[tuple[str, str]] = [(case.payload, "raw")]
            for converter in converters:
                try:
                    result = await converter.convert_async(
                        prompt=case.payload, input_type="text"
                    )
                    variants.append((result.output_text, type(converter).__name__))
                except Exception as exc:  # pragma: no cover - defensive
                    print(f"  converter {type(converter).__name__} failed: {exc}")

            for variant, converter_name in variants:
                piece = MessagePiece(
                    role="user",
                    original_value=variant,
                    converted_value=variant,
                )
                message = Message(message_pieces=[piece])
                responses = await target.send_prompt_async(message=message)
                # Score each response with PyRIT's SubStringScorer (ASR signal).
                reached = False
                for response in responses:
                    scores = await scorer.score_async(message=response)
                    reached = reached or any(
                        str(getattr(s, "score_value", "")) == "true" for s in scores
                    )
                # Persist the exchange through PyRIT memory (best-effort).
                try:  # pragma: no cover - depends on the installed pyrit version
                    await memory.add_message(message=message)
                    for response in responses:
                        await memory.add_message(message=response)
                except Exception:  # noqa: S110 - persistence is best-effort
                    pass
                rows.append(
                    {
                        "vector": case.vector,
                        "payload": (
                            case.payload
                            if len(case.payload) <= 48
                            else case.payload[:45] + "..."
                        ),
                        "variant": converter_name,
                        "blocked": not reached,
                        "passed": reached,
                    }
                )
    finally:
        memory.dispose_engine()
    return rows


def main() -> int:
    """Run the PyRIT campaign, print the ASR report, enforce --strict."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--strict",
        action="store_true",
        help=f"exit 1 when overall ASR >= {STRICT_ASR_LIMIT:.0%}",
    )
    args = parser.parse_args()

    if not PYRIT_AVAILABLE:
        print("pyrit not installed — run: pip install -e '.[redteam]'")
        return 1

    rows = asyncio.run(run_campaign())

    print("=== PyRIT red-team campaign (Attack Success Rate) ===")
    print(f"{'vector':<16}{'variant':<24}verdict")
    print("-" * 52)
    for row in rows:
        status = "PASSED" if row["passed"] else "BLOCKED"
        print(f"  {row['vector']:<14}  {row['variant']:<22} {status}")

    total = len(rows)
    passed = sum(1 for row in rows if row["passed"])
    asr = passed / total if total else 0.0
    print("-" * 52)
    print(f"PyRIT overall ASR: {asr:.1%} ({passed}/{total} variants reached output)")

    if args.strict and asr >= STRICT_ASR_LIMIT:
        print(
            f"\nSTRICT: ASR {asr:.1%} exceeds the {STRICT_ASR_LIMIT:.0%} gate — "
            "fix the vector before merging",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
