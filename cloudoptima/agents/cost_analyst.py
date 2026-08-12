"""CostAnalystAgent — prices the design and checks it against the budget.

The cost analyst reads the architect's design (from ``session.agent_turns``)
and the user's budget, then returns a numeric estimate with a line-item
breakdown, a budget status (UNDER/NEAR/OVER), and concrete savings ideas.

The budget is a **read-only reference**: it's rendered into the prompt so the
model can judge against it, and validation never lets output rewrite the
session budget.
"""

from __future__ import annotations

import json
from typing import Any, Final

from cloudoptima.agent_base import BaseAgent
from cloudoptima.models import AgentType, Session
from cloudoptima.pricing import (
    KNOWN_AZURE_SERVICES,
    extract_services,
    live_prices,
    render_price_block,
)

# The only budget statuses the model may report.
_BUDGET_STATUSES: frozenset[str] = frozenset({"UNDER", "NEAR", "OVER"})

# Phase 10.2: the cost analyst's contract is exactly these keys. Prices are
# STATIC by design — the model may only name services from the immutable
# KNOWN_AZURE_SERVICES catalog, so it can never inject invented line items.
_ALLOWED_KEYS: Final[frozenset[str]] = frozenset(
    {"estimate", "currency", "breakdown", "budget_status", "savings"}
)
_ALLOWED_ITEM_KEYS: Final[frozenset[str]] = frozenset({"service", "cost", "notes"})

_COST_SYSTEM_PROMPT = """\
You are a cloud cost analyst specializing in Azure FinOps. Estimate the monthly
cost of the proposed architecture and compare it against the user's budget. The
budget is a READ-ONLY reference — you may read it and judge against it, but you
must never modify it or invent a new one.

The prompt carries a LIVE AZURE RETAIL PRICES block with real per-unit prices
from the Azure Retail Prices API. Prefer those numbers over your training-data
estimates when pricing line items, and scale them by the quantities the design
implies. If the block says no live prices were fetched, fall back to your own
Azure pricing knowledge.

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
                self._wrap_field(
                    "DEPLOYMENT SCALE",
                    getattr(session.scale, "value", session.scale),
                ),
                self._wrap_field(
                    "AZURE REGION",
                    getattr(session.region, "value", session.region),
                ),
                self._wrap_field("REQUIRED SERVICES", session.services),
                self._wrap_field("REQUIREMENTS", session.user_prompt),
                "ARCHITECT DESIGN (trusted pipeline output):",
                self._prior_turn_json(session, AgentType.ARCHITECT),
                "AZURE RETAIL PRICES (LIVE, per-unit list prices in USD):",
                self._live_pricing_block(session),
            ]
        )

    def _live_pricing_block(self, session: Session) -> str:
        """Fetch real Azure Retail Prices for the services the design mentions.

        Scans the user's services text plus the architect's validated JSON for
        known Azure services, then prices each one against the live Retail
        Prices API (static catalog as the offline fallback). Never raises — a
        network blip degrades to a factual "no prices fetched" line instead of
        breaking the pipeline.

        Args:
            session: The session being analyzed (architect turn already run).

        Returns:
            The rendered price block for the prompt.
        """
        texts: list[str | None] = [session.services, session.user_prompt]
        for turn in session.agent_turns:
            if turn.agent_type == AgentType.ARCHITECT and "error" not in turn.output:
                try:
                    texts.append(json.dumps(turn.output))
                except (TypeError, ValueError):  # pragma: no cover - defensive
                    texts.append(None)
                break
        names = extract_services(*texts)
        region = str(getattr(session.region, "value", session.region) or "uaenorth")
        return render_price_block(live_prices(names, region), region)

    def _validate_output(self, data: dict[str, Any]) -> tuple[bool, str]:
        """Require a numeric estimate, a valid budget status, and a breakdown.

        Defense-in-depth (Phase 10.2):
        - The budget is read-only — a ``budget`` key in the output would be an
          unexpected key and rejected.
        - Every breakdown service must exist in the immutable
          :data:`KNOWN_AZURE_SERVICES` catalog, so the model can't invent line
          items or tamper with prices.
        """
        ok, message = self._reject_unknown_keys(data, _ALLOWED_KEYS)
        if not ok:
            return False, message

        estimate = data.get("estimate")
        if not isinstance(estimate, int | float) or isinstance(estimate, bool):
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
            ok, message = self._reject_unknown_keys(item, _ALLOWED_ITEM_KEYS)
            if not ok:
                return False, f"breakdown item has {message}"
            if not isinstance(item.get("service"), str):
                return False, "each breakdown item must have a string 'service'"
            if item["service"] not in KNOWN_AZURE_SERVICES:
                return False, (
                    f"unknown Azure service in breakdown: {item['service']!r} "
                    "(pricing is a fixed catalog — see cloudoptima.pricing)"
                )
            cost = item.get("cost")
            if not isinstance(cost, int | float) or isinstance(cost, bool):
                return False, "each breakdown item must have a numeric 'cost'"

        savings = data.get("savings")
        if savings is not None and not isinstance(savings, list):
            return False, "'savings' must be a list"
        return True, ""
