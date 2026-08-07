"""JudgeAgent — arbitrates disagreements between the four specialist agents.

The judge reviews all four agent outputs and the detected conflicts, then
produces an arbitration summary, a final recommendation, and the list of
agents whose proposals were overridden.

Hard rule: the judge may override any recommendation but can **never** suggest
disabling security controls. Validation rejects any final recommendation
containing ``disable_encryption`` or ``disable_mfa``.
"""

from __future__ import annotations

import re
from typing import Any, Final

from cloudoptima.agent_base import _DELIMITER_MARKER, BaseAgent
from cloudoptima.models import AgentType, Session

# Phrases that must never appear in a final recommendation. Kept as exact
# substrings (lowercased for the match) so the check is simple and auditable.
_BANNED_PHRASES: Final[tuple[str, ...]] = ("disable_encryption", "disable_mfa")

# Phase 10.2: the judge's contract is exactly these keys.
_ALLOWED_KEYS: Final[frozenset[str]] = frozenset(
    {"arbitration", "final_recommendation", "overridden_agents"}
)
_ALLOWED_ARB_KEYS: Final[frozenset[str]] = frozenset(
    {"conflicts_detected", "conflict_summaries"}
)
_ALLOWED_SUMMARY_KEYS: Final[frozenset[str]] = frozenset(
    {"dimension", "agents_involved", "issue", "resolution"}
)

_JUDGE_SYSTEM_PROMPT = """\
You are an impartial judge overseeing a panel of four cloud expert agents.
Review their outputs and the detected conflicts, then arbitrate. You may
override any recommendation, but you can never suggest disabling security
controls such as encryption or MFA.

Return ONLY valid JSON with exactly this structure — no prose outside the JSON:

{
  "arbitration": {
    "conflicts_detected": 0,
    "conflict_summaries": [
      {"dimension": "string", "agents_involved": ["string", "..."],
       "issue": "string", "resolution": "string"}
    ]
  },
  "final_recommendation": "string",
  "overridden_agents": ["string", "..."]
}
"""


class JudgeAgent(BaseAgent):
    """Resolves conflicts and issues the final arbitration."""

    system_prompt: str = _JUDGE_SYSTEM_PROMPT

    def _build_prompt(self, session: Session) -> str:
        """Expose every agent's output plus the detected conflicts for arbitration."""
        return "\n".join(
            [
                self._wrap_field("PROJECT NAME", session.project_name),
                self._wrap_field("REQUIREMENTS", session.user_prompt),
                "ARCHITECT OUTPUT (trusted pipeline data):",
                self._prior_turn_json(session, AgentType.ARCHITECT),
                "COST ANALYST OUTPUT (trusted pipeline data):",
                self._prior_turn_json(session, AgentType.COST_ANALYST),
                "SECURITY OUTPUT (trusted pipeline data):",
                self._prior_turn_json(session, AgentType.SECURITY),
                "COMPLIANCE OUTPUT (trusted pipeline data):",
                self._prior_turn_json(session, AgentType.COMPLIANCE),
                "DETECTED CONFLICTS (trusted pipeline data):",
                self._render_conflicts(session),
            ]
        )

    def _render_conflicts(self, session: Session) -> str:
        """Render the session's conflicts as plain text blocks, or ``"(none)"``."""
        if not session.conflicts:
            return "(none)"
        blocks: list[str] = []
        for index, conflict in enumerate(session.conflicts, start=1):
            agents = ", ".join(str(getattr(agent, "value", agent)) for agent in conflict.agents)
            # Strip delimiter-marker runs from conflict text too: a hostile
            # value could otherwise forge a "--- FIELD ---" boundary here.
            blocks.append(
                f"{index}. dimension={_DELIMITER_MARKER.sub('', conflict.dimension)}\n"
                f"   agents_involved={agents}\n"
                f"   issue={_DELIMITER_MARKER.sub('', conflict.issue)}\n"
                f"   resolution={_DELIMITER_MARKER.sub('', conflict.resolution)}"
            )
        return "\n".join(blocks)

    def _validate_output(self, data: dict[str, Any]) -> tuple[bool, str]:
        """Require a well-formed arbitration and a safe final recommendation."""
        ok, message = self._reject_unknown_keys(data, _ALLOWED_KEYS)
        if not ok:
            return False, message
        arbitration = data.get("arbitration")
        if not isinstance(arbitration, dict):
            return False, "'arbitration' must be an object"
        ok, message = self._reject_unknown_keys(arbitration, _ALLOWED_ARB_KEYS)
        if not ok:
            return False, f"arbitration has {message}"

        count = arbitration.get("conflicts_detected")
        if not isinstance(count, int) or isinstance(count, bool) or count < 0:
            return False, "'conflicts_detected' must be a non-negative integer"

        summaries = arbitration.get("conflict_summaries")
        if not isinstance(summaries, list):
            return False, "'conflict_summaries' must be a list"
        for item in summaries:
            if not isinstance(item, dict):
                return False, "each conflict summary must be an object"
            ok, message = self._reject_unknown_keys(item, _ALLOWED_SUMMARY_KEYS)
            if not ok:
                return False, f"conflict summary has {message}"
            for key in ("dimension", "issue", "resolution"):
                if not isinstance(item.get(key), str):
                    return False, f"each conflict summary must have a string '{key}'"
            if not isinstance(item.get("agents_involved"), list):
                return False, "each conflict summary must have an 'agents_involved' list"

        final = data.get("final_recommendation")
        if not isinstance(final, str):
            return False, "'final_recommendation' must be a string"
        # Normalize both sides so spacing/punctuation tricks ("disable
        # encryption", "disable-mfa", "disable\nencryption") all collapse
        # onto the same string and can't dodge the check.
        normalized = re.sub(r"[_\-\s]", "", final.lower())
        for phrase in _BANNED_PHRASES:
            normalized_phrase = re.sub(r"[_\-\s]", "", phrase.lower())
            if normalized_phrase in normalized:
                return False, f"'final_recommendation' must not suggest '{phrase}'"

        overridden = data.get("overridden_agents")
        if not isinstance(overridden, list):
            return False, "'overridden_agents' must be a list"
        return True, ""
