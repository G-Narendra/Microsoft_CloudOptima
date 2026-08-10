"""ComplianceOfficerAgent — checks the design against the 21 rules + RAG.

The compliance officer grades the proposed architecture against the target
regulatory frameworks and the **21 immutable compliance rules** in
:mod:`cloudoptima.compliance.rules`.

Those rules are enforced three times on purpose (a v1 lesson):

1. The module is the single immutable source of truth (Phase 8.1).
2. The system prompt lists them **explicitly** (never by reference), so the
   model can't invent or quietly drop a rule.
3. Validation checks every ``rule_id`` in the output against the 21, and
   demands NEEDS_WORK overall whenever any rule isn't PASS.

For framework-specific edge cases the prompt is enriched with RAG passages
from :mod:`cloudoptima.compliance.rag` (Phase 8.2) — treated as untrusted
and cleaned before they enter the prompt.
"""

from __future__ import annotations

import logging
from typing import Any, Final

from cloudoptima.agent_base import BaseAgent
from cloudoptima.compliance.rag import query_rag
from cloudoptima.compliance.rules import RULE_IDS, render_rules_text
from cloudoptima.models import AgentType, Session
from cloudoptima.safety import shield_prompt

_logger = logging.getLogger(__name__)

_VALID_RULE_IDS: frozenset[str] = RULE_IDS
_RULE_STATUSES: frozenset[str] = frozenset({"PASS", "FAIL", "WARNING", "CONFIG_NEEDED"})
_OVERALL_STATUSES: frozenset[str] = frozenset({"PASS", "NEEDS_WORK"})

# Phase 10.2: the compliance officer's contract is exactly these keys.
_ALLOWED_KEYS: frozenset[str] = frozenset(
    {"framework", "overall_status", "rules", "remediation_steps"}
)
_ALLOWED_RULE_KEYS: frozenset[str] = frozenset({"rule_id", "rule_name", "status", "details"})

# The rules, rendered once for the system prompt. Kept in the exact order of
# the rules module so the numbering cannot drift.
_RULES_TEXT: Final[str] = render_rules_text()

# Maximum number of RAG passages injected into the prompt.
_MAX_RAG_PASSAGES: Final[int] = 2

_COMPLIANCE_SYSTEM_PROMPT = f"""\
You are a compliance officer. Assess the proposed architecture against the
target compliance frameworks and THE ONLY 21 RULES LISTED BELOW. These rules
are hardcoded — you must never invent, drop, or modify a rule.

THE 21 RULES:
{_RULES_TEXT}

If the prompt includes a "RELEVANT COMPLIANCE GUIDANCE" section, use it to
inform your judgment on framework-specific edge cases, but the 21 rules above
remain the authority.

Return ONLY valid JSON with exactly this structure — no prose outside the JSON:

{{
  "overall_status": "PASS" or "NEEDS_WORK",
  "rules": [
    {{"rule_id": "01", "rule_name": "string",
      "status": "PASS" or "FAIL" or "WARNING" or "CONFIG_NEEDED",
      "details": "string"}}
  ],
  "remediation_steps": ["string", "..."]
}}
"""


class ComplianceOfficerAgent(BaseAgent):
    """Checks the design against the 21 hardcoded compliance rules."""

    system_prompt: str = _COMPLIANCE_SYSTEM_PROMPT

    def _build_prompt(self, session: Session) -> str:
        """Wrap session fields, name the frameworks, and expose the architect's design."""
        # NOTE: pydantic's use_enum_values stores list items as plain strings
        # ("pdpl"), while scalar enum fields keep their members. getattr handles
        # both, so this works regardless of how the session was constructed.
        frameworks = ", ".join(
            str(getattr(framework, "value", framework))
            for framework in session.compliance_frameworks
        ) or "not specified"
        sections = [
            self._wrap_field("PROJECT NAME", session.project_name),
            self._wrap_field("AZURE REGION", getattr(session.region, "value", session.region)),
            self._wrap_field("COMPLIANCE FRAMEWORKS", frameworks),
            self._wrap_field("REQUIREMENTS", session.user_prompt),
            "ARCHITECT DESIGN (trusted pipeline output):",
            self._prior_turn_json(session, AgentType.ARCHITECT),
        ]

        # Phase 8.2: enrich with framework-specific RAG guidance. Retrieved
        # passages are untrusted — query_rag already cleans + injection-scans
        # them; issue #2 adds the Prompt Shield (document / indirect-attack
        # detection) on top, and attacked passages are dropped here. The
        # shield works in two modes: the always-on offline floor (no Azure
        # resource needed) and the ML shield; both report per-document attack
        # flags, and any flagged passage is dropped before it reaches the prompt.
        for framework in frameworks.split(", "):
            passages = query_rag(session.user_prompt or "compliance", framework, _MAX_RAG_PASSAGES)
            if passages:
                shield = shield_prompt(
                    session.user_prompt or "", passages, self.config
                )
                if shield.user_prompt_attack:
                    _logger.warning(
                        "Compliance RAG: user prompt flagged by Prompt Shields "
                        "(session %s)",
                        session.session_id,
                    )
                if shield.documents_attack and len(shield.documents_attack) == len(passages):
                    passages = [
                        passage
                        for passage, attacked in zip(
                            passages, shield.documents_attack, strict=False
                        )
                        if not attacked
                    ]
            if passages:
                sections.append("RELEVANT COMPLIANCE GUIDANCE:")
                for passage in passages:
                    sections.append(f"- {passage}")
                break  # one framework's guidance is enough for a focused prompt

        return "\n".join(sections)

    def _validate_output(self, data: dict[str, Any]) -> tuple[bool, str]:
        """Require known rule IDs and an overall status consistent with the rules."""
        ok, message = self._reject_unknown_keys(data, _ALLOWED_KEYS)
        if not ok:
            return False, message
        overall = data.get("overall_status")
        if overall not in _OVERALL_STATUSES:
            return False, (
                f"'overall_status' must be one of {sorted(_OVERALL_STATUSES)}, "
                f"got {overall!r}"
            )

        rules = data.get("rules")
        if not isinstance(rules, list) or not rules:
            return False, "'rules' must be a non-empty list"

        any_non_pass = False
        for item in rules:
            if not isinstance(item, dict):
                return False, "each rule check must be an object"
            ok, message = self._reject_unknown_keys(item, _ALLOWED_RULE_KEYS)
            if not ok:
                return False, f"rule check has {message}"
            rule_id = item.get("rule_id")
            if rule_id not in _VALID_RULE_IDS:
                return False, (
                    f"rule_id {rule_id!r} is not one of the 21 hardcoded rules"
                )
            if not isinstance(item.get("rule_name"), str):
                return False, "each rule check must have a string 'rule_name'"
            status = item.get("status")
            if status not in _RULE_STATUSES:
                return False, (
                    f"rule status must be one of {sorted(_RULE_STATUSES)}, got {status!r}"
                )
            if not isinstance(item.get("details"), str):
                return False, "each rule check must have a string 'details'"
            if status != "PASS":
                any_non_pass = True

        if any_non_pass and overall != "NEEDS_WORK":
            return False, "if any rule is not PASS, 'overall_status' must be NEEDS_WORK"
        if not any_non_pass and overall != "PASS":
            return False, "if every rule passes, 'overall_status' must be PASS"

        remediation = data.get("remediation_steps")
        if not isinstance(remediation, list):
            return False, "'remediation_steps' must be a list"
        return True, ""
