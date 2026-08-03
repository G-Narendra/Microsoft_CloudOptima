"""CostAnalystAgent — estimates monthly cost and checks it against the budget.

The cost analyst reads the architect's design (via ``session.agent_turns``) and
the user's budget, then produces a numeric estimate with a line-item breakdown,
a budget status (UNDER/NEAR/OVER), and concrete savings suggestions.

The budget is a **read-only reference**: it is rendered into the prompt only so
the model can judge against it, and validation never accepts output that would
let the model rewrite the session budget.
"""

from __future__ import annotations

from typing import Any

from cloudoptima.agent_base import BaseAgent
from cloudoptima.models import AgentType, Session

# The only budget statuses the model may report.
_BUDGET_STATUSES: frozenset[str] = frozenset({"UNDER", "NEAR", "OVER"})

_COST_SYSTEM_PROMPT = """\
You are a cloud cost analyst specializing in Azure FinOps. Estimate the monthly
cost of the proposed architecture and compare it against the user's budget. The
budget is a READ-ONLY reference — you may read it and judge against it, but you
must never modify it or invent a new one.

Return ONLY valid JSON with exactly this structure — no prose outside the JSON:

{
  "estimate": 0.0,
  "currency": "USD",
  "breakdown": [{"service": "string", "cost": 0.0, "notes": "string"}],
  "budget_status": "UNDER" or "NEAR" or "OVER",
  "savings": ["string", "..."]
}
"""


class CostAnalystAgent(BaseAgent):
    """Estimates monthly costs and flags budget violations."""

    system_prompt: str = _COST_SYSTEM_PROMPT

    def _build_prompt(self, session: Session) -> str:
        """Wrap session fields and expose the architect's design to cost the plan."""
        budget = session.budget if session.budget is not None else "not provided"
        return "\n".join(
            [
                self._wrap_field("PROJECT NAME", session.project_name),
                self._wrap_field("MONTHLY BUDGET (READ-ONLY REFERENCE)", budget),
                self._wrap_field("DEPLOYMENT SCALE", session.scale.value),
                self._wrap_field("AZURE REGION", session.region.value),
                self._wrap_field("REQUIRED SERVICES", session.services),
                self._wrap_field("REQUIREMENTS", session.user_prompt),
                "ARCHITECT DESIGN (trusted pipeline output):",
                self._prior_turn_json(session, AgentType.ARCHITECT),
            ]
        )

    def _validate_output(self, data: dict[str, Any]) -> tuple[bool, str]:
        """Require a numeric estimate, a valid budget status, and a breakdown."""
        estimate = data.get("estimate")
        if not isinstance(estimate, (int, float)) or isinstance(estimate, bool):
            return False, "'estimate' must be a number"

        status = data.get("budget_status")
        if status not in _BUDGET_STATUSES:
            return False, (
                f"'budget_status' must be one of {sorted(_BUDGET_STATUSES)}, "
                f"got {status!r}"
            )

        breakdown = data.get("breakdown")
        if not isinstance(breakdown, list):
            return False, "'breakdown' must be a list"
        for item in breakdown:
            if not isinstance(item, dict):
                return False, "each breakdown item must be an object"
            if not isinstance(item.get("service"), str):
                return False, "each breakdown item must have a string 'service'"
            cost = item.get("cost")
            if not isinstance(cost, (int, float)) or isinstance(cost, bool):
                return False, "each breakdown item must have a numeric 'cost'"

        savings = data.get("savings")
        if savings is not None and not isinstance(savings, list):
            return False, "'savings' must be a list"
        return True, ""
