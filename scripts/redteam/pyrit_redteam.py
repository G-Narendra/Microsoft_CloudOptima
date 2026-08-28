"""PyRIT-native red teaming campaign.

Drives the attack corpus through Microsoft's PyRIT framework components:
- CloudOptimaTarget routing through defenses
- PyRIT converters for adversarial obfuscation
- PyRIT SubStringScorer scoring attack success vs blocked
- PyRIT Memory for run persistence
"""

from __future__ import annotations

import argparse
import asyncio
from pathlib import Path
import sys
from typing import Any

# Make cloudoptima and redteam harness importable
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from redteam_cloudoptima import ATTACK_CASES, STRICT_ASR_LIMIT, probe_payload

KNOWN_GAP_VARIANTS: frozenset[tuple[str, str]] = frozenset(
    {("base64_short", "LeetspeakConverter")}
)

# Optional PyRIT dependency
try:
    from pyrit.memory import CentralMemory
    try:
        from pyrit.memory import DuckDBMemory as MemoryProvider
    except ImportError:
        try:
            from pyrit.memory import SQLiteMemory as MemoryProvider
        except ImportError:
            from pyrit.memory import DuckDBMemoryProvider as MemoryProvider

    try:
        from pyrit.models import PromptRequestResponse as Message
        from pyrit.models import PromptRequestPiece as MessagePiece
    except ImportError:
        from pyrit.models import Message, MessagePiece

    from pyrit.prompt_converter import (
        AtbashConverter,
        Base64Converter,
        FlipConverter,
        LeetspeakConverter,
        ROT13Converter,
        UnicodeConfusableConverter,
    )
    try:
        from pyrit.prompt_converter import BidiConverter
    except ImportError:
        BidiConverter = None

    from pyrit.prompt_target import PromptTarget
    from pyrit.score import SubStringScorer

    PYRIT_AVAILABLE = True
except Exception:
    PYRIT_AVAILABLE = False
    PromptTarget = object  # type: ignore[misc, assignment]
    SubStringScorer = object  # type: ignore[misc, assignment]


def _create_piece(role: str, text: str) -> Any:
    """Create a MessagePiece / PromptRequestPiece safely."""
    try:
        return MessagePiece(role=role, original_value=text, converted_value=text)
    except Exception:
        return MessagePiece(role=role, original_value=text)


def _create_message(piece: Any) -> Any:
    """Create a Message / PromptRequestResponse safely."""
    try:
        return Message(request_pieces=[piece])
    except TypeError:
        return Message(message_pieces=[piece])


def _extract_text(req: Any) -> str:
    """Extract prompt text from any PyRIT request structure."""
    if req is None:
        return ""
    if hasattr(req, "converted_value") and req.converted_value:
        return str(req.converted_value)
    if hasattr(req, "request_pieces") and req.request_pieces:
        return str(req.request_pieces[-1].converted_value or req.request_pieces[-1].original_value)
    if hasattr(req, "message_pieces") and req.message_pieces:
        return str(req.message_pieces[-1].converted_value or req.message_pieces[-1].original_value)
    if hasattr(req, "get_value"):
        return str(req.get_value())
    if isinstance(req, list) and req:
        return _extract_text(req[-1])
    return str(req)


class CloudOptimaTarget(PromptTarget):
    """PyRIT PromptTarget routing payloads through CloudOptima defenses."""

    def _validate_request(self, *, prompt_request: Any = None, **kwargs: Any) -> None:
        pass

    async def _send_prompt_to_target_async(
        self,
        *,
        normalized_conversation: Any = None,
        **kwargs: Any,
    ) -> Any:
        return await self.send_prompt_async(normalized_conversation=normalized_conversation, **kwargs)

    async def send_prompt_async(
        self,
        *,
        prompt_request: Any = None,
        message: Any = None,
        normalized_conversation: Any = None,
        **kwargs: Any,
    ) -> Any:
        req = prompt_request or message or normalized_conversation
        text = _extract_text(req)

        blocked, defense = probe_payload(text)
        verdict = f"BLOCKED:{defense}" if blocked else "PASSED"

        piece = _create_piece(role="assistant", text=verdict)
        if not hasattr(piece, "get_value"):
            setattr(piece, "get_value", lambda: verdict)

        res = _create_message(piece)
        if not hasattr(res, "get_value"):
            setattr(res, "get_value", lambda: verdict)

        if hasattr(Message, "message_pieces"):
            return [res]
        return res


class CloudOptimaSubStringScorer(SubStringScorer):
    """SubStringScorer robust across PyRIT releases and memory backends."""

    def __init__(self, substring: str = "PASSED", category: str = "attack_success", **kwargs: Any) -> None:
        try:
            super().__init__(substring=substring, category=category)
        except TypeError:
            try:
                super().__init__(substring=substring, categories=[category])
            except TypeError:
                super().__init__(substring=substring)
        self._substring = substring
        self._score_category = category
        self.scorer_type = "true_false"

    async def score_async(
        self,
        request_response: Any = None,
        *,
        message: Any = None,
        task: Any = None,
        **kwargs: Any,
    ) -> list[Any]:
        target = request_response if request_response is not None else message
        if hasattr(target, "request_pieces") and target.request_pieces:
            piece = target.request_pieces[0]
        elif hasattr(target, "message_pieces") and target.message_pieces:
            piece = target.message_pieces[0]
        elif isinstance(target, list) and target:
            first = target[0]
            if hasattr(first, "request_pieces") and first.request_pieces:
                piece = first.request_pieces[0]
            elif hasattr(first, "message_pieces") and first.message_pieces:
                piece = first.message_pieces[0]
            else:
                piece = first
        else:
            piece = target

        text = getattr(piece, "converted_value", "") or getattr(piece, "original_value", "") or str(piece)
        is_passed = self._substring in text

        try:
            from pyrit.models import Score
            score_obj = Score(
                score_value=str(is_passed),
                score_value_description=None,
                score_metadata="",
                score_type=getattr(self, "scorer_type", "true_false"),
                score_category=getattr(self, "_score_category", "attack_success"),
                score_rationale=None,
                scorer_class_identifier=self.get_identifier() if hasattr(self, "get_identifier") else {},
                prompt_request_response_id=getattr(piece, "id", None),
                task=task,
            )
            try:
                if hasattr(self, "_memory") and hasattr(self._memory, "add_scores_to_memory"):
                    self._memory.add_scores_to_memory(scores=[score_obj])
            except Exception:
                pass
            return [score_obj]
        except Exception:
            class _Score:
                def __init__(self, val: bool):
                    self.score_value = str(val)
                    self.score_type = "true_false"
                    self.score_category = "attack_success"
            return [_Score(is_passed)]


def _attack_success_scorer() -> Any:
    """PyRIT scorer: scores true when response substring is PASSED."""
    return CloudOptimaSubStringScorer(substring="PASSED", category="attack_success")


async def run_campaign(limit: int | None = None) -> list[dict[str, Any]]:
    """Drive attack corpus through PyRIT and return rows with results."""
    if not PYRIT_AVAILABLE:
        return []

    db_path = str(Path(__file__).parent / "pyrit_memory.db")
    try:
        memory = MemoryProvider(db_path=db_path)
        CentralMemory.set_memory_instance(memory)
    except Exception:
        memory = None

    target = CloudOptimaTarget()
    scorer = _attack_success_scorer()

    converters: list[Any] = []
    converter_candidates = [
        UnicodeConfusableConverter(deterministic=True),
        Base64Converter(),
        FlipConverter(),
        ROT13Converter(),
        AtbashConverter(),
        LeetspeakConverter(deterministic=True),
    ]
    if BidiConverter is not None:
        converter_candidates.append(BidiConverter())

    for conv in converter_candidates:
        try:
            converters.append(conv)
        except Exception:
            pass

    rows: list[dict[str, Any]] = []
    cases = list(ATTACK_CASES) if limit is None else list(ATTACK_CASES)[:limit]

    try:
        for case in cases:
            variants: list[tuple[str, str]] = [(case.payload, "raw")]
            for converter in converters:
                try:
                    result = await converter.convert_async(
                        prompt=case.payload, input_type="text"
                    )
                    variants.append((result.output_text, type(converter).__name__))
                except Exception:
                    pass

            for variant, converter_name in variants:
                piece = _create_piece(role="user", text=variant)
                req_obj = _create_message(piece)
                try:
                    response = await target.send_prompt_async(prompt_request=req_obj)
                except TypeError:
                    response = await target.send_prompt_async(message=req_obj)

                # Extract response piece to score
                if hasattr(response, "request_pieces") and response.request_pieces:
                    piece_to_score = response.request_pieces[0]
                elif hasattr(response, "message_pieces") and response.message_pieces:
                    piece_to_score = response.message_pieces[0]
                elif isinstance(response, list) and response:
                    first = response[0]
                    if hasattr(first, "message_pieces") and first.message_pieces:
                        piece_to_score = first.message_pieces[0]
                    elif hasattr(first, "request_pieces") and first.request_pieces:
                        piece_to_score = first.request_pieces[0]
                    else:
                        piece_to_score = first
                else:
                    piece_to_score = response

                # Score response
                scores = await scorer.score_async(request_response=piece_to_score, message=piece_to_score)

                reached = False
                for score in scores:
                    val = getattr(score, "score_value", "")
                    if str(val).lower() == "true":
                        reached = True

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
                        "known_gap": (case.vector, converter_name) in KNOWN_GAP_VARIANTS,
                    }
                )
    finally:
        if memory is not None and hasattr(memory, "dispose_engine"):
            try:
                memory.dispose_engine()
            except Exception:
                pass

    return rows


def main() -> int:
    """Run PyRIT campaign, print ASR report, and enforce strict limit."""
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
        status = "KNOWN GAP" if row["known_gap"] else ("PASSED" if row["passed"] else "BLOCKED")
        print(f"  {row['vector']:<14}  {row['variant']:<22} {status}")

    strict_rows = [row for row in rows if not row["known_gap"]]
    total = len(strict_rows)
    passed = sum(1 for row in strict_rows if row["passed"])
    asr = passed / total if total else 0.0
    print("-" * 52)
    print(f"PyRIT overall ASR: {asr:.1%} ({passed}/{total} strict variants reached output)")

    gaps = [row for row in rows if row["known_gap"] and row["passed"]]
    if gaps:
        print("known gaps (handled by ML Content Safety / Prompt Shields):")
        for row in gaps:
            print(f"  {row['vector']} + {row['variant']}: {row['payload']}")

    if args.strict and asr >= STRICT_ASR_LIMIT:
        print(
            f"\nSTRICT: ASR {asr:.1%} exceeds {STRICT_ASR_LIMIT:.0%} threshold",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
