"""ComplianceOfficerAgent — checks the design against the 21 rules + RAG."""

from __future__ import annotations

import logging
from typing import Any, Final

from cloudoptima.agent_base import BaseAgent
from cloudoptima.compliance.rag import ComplianceRAG
from cloudoptima.compliance.rules import RULE_IDS, render_rules_text
from cloudoptima.models import AgentType, AzureRegion, Session
from cloudoptima.safety import shield_prompt

_logger = logging.getLogger(__name__)

_VALID_RULE_IDS: frozenset[str] = RULE_IDS
_RULE_STATUSES: frozenset[str] = frozenset({"PASS", "FAIL", "WARNING", "CONFIG_NEEDED"})
_OVERALL_STATUSES: frozenset[str] = frozenset({"PASS", "NEEDS_WORK"})

# Output schema contract
_ALLOWED_KEYS: frozenset[str] = frozenset(
    {"framework", "overall_status", "rules", "remediation_steps"}
)
_ALLOWED_RULE_KEYS: frozenset[str] = frozenset({"rule_id", "rule_name", "status", "details"})
_RULES_TEXT: Final[str] = render_rules_text()
_MAX_RAG_PASSAGES: Final[int] = 2

# Region to Framework data residency mapping
_REGION_FRAMEWORK_MAP: Final[dict[str, str]] = {
    AzureRegion.UAE_NORTH.value: "pdpl",
    AzureRegion.WEST_US.value: "ccpa",
    AzureRegion.WEST_US_2.value: "ccpa",
    AzureRegion.WEST_EUROPE.value: "gdpr",
    AzureRegion.NORTH_EUROPE.value: "gdpr",
    AzureRegion.GERMANY_WEST_CENTRAL.value: "gdpr",
}

_ROLE = "You are a compliance officer specializing in cloud architecture reviews."
_CAPABILITIES = (
    "Assess the proposed architecture against the compliance frameworks selected by the user. "
    "The 21 rules below are your complete authority — they cover PDPL, GDPR, PCI-DSS, SOC 2, HIPAA, ISO 27001, and NIST CSF. "
    "If the user selected specific frameworks (e.g. 'gdpr, hipaa'), focus your detailed analysis on those frameworks' rules. "
    "For rules from frameworks NOT selected by the user, you may still include them if they are universally applicable "
    "(e.g. encryption, backup, access control apply to every deployment), but mark them as advisory. "
    "If the prompt includes a 'RELEVANT COMPLIANCE GUIDANCE' section, use it to inform your judgment on framework-specific edge cases."
)
_CONSTRAINTS = (
    "The 21 rules are hardcoded — you must never invent, drop, or modify a rule. "
    "Only assess rules that are relevant to the selected frameworks and the deployment's context. "
    "Return ONLY valid JSON with exactly the required structure — no prose outside the JSON."
)
_OUTPUT_SCHEMA = """{
  "overall_status": "PASS" or "NEEDS_WORK",
  "rules": [
    {"rule_id": "01", "rule_name": "string",
      "status": "PASS" or "FAIL" or "WARNING" or "CONFIG_NEEDED",
      "details": "string"}
  ],
  "remediation_steps": ["string", "..."]
}"""

_COMPLIANCE_SYSTEM_PROMPT = f"""
# ROLE
{_ROLE}

# CAPABILITIES
{_CAPABILITIES}

# CONSTRAINTS
{_CONSTRAINTS}

# THE 21 RULES (your complete authority — do not invent others)
{_RULES_TEXT}

# OUTPUT SCHEMA
{_OUTPUT_SCHEMA}
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

        # Phase 8.2: enrich with RAG guidance from the selected frameworks.
        # Parse frameworks into a list for metadata filtering
        frameworks_to_query = [f.strip() for f in frameworks.split(",") if f.strip() and f.strip().lower() != "not specified"]
        region_val = getattr(session.region, "value", session.region)
        if region_val in _REGION_FRAMEWORK_MAP:
            mapped_fw = _REGION_FRAMEWORK_MAP[region_val]
            if mapped_fw not in frameworks_to_query:
                frameworks_to_query.append(mapped_fw)

        rag_engine = ComplianceRAG(self.config)
        
        # Rewrite raw prompt into focused keywords
        raw_prompt = session.user_prompt or "compliance assessment"
        focused_query = rag_engine.rewrite_query(raw_prompt, self.client)
        _logger.info("Compliance RAG: Rewrote query from %r to %r", raw_prompt, focused_query)

        raw_passages = rag_engine.query_rag(
            focused_query,
            framework=frameworks_to_query,
            top_k=_MAX_RAG_PASSAGES + 2,
        )
        if raw_passages:
            shield = shield_prompt(
                session.user_prompt or "", raw_passages, self.config
            )
            if shield.user_prompt_attack:
                _logger.warning(
                    "Compliance RAG: user prompt flagged by Prompt Shields (session %s)",
                    session.session_id,
                )
            if shield.documents_attack and len(shield.documents_attack) == len(raw_passages):
                raw_passages = [
                    passage
                    for passage, attacked in zip(
                        raw_passages, shield.documents_attack, strict=False
                    )
                    if not attacked
                ]
        if raw_passages:
            sections.append("RELEVANT COMPLIANCE GUIDANCE (for the selected frameworks):")
            for passage in raw_passages[:_MAX_RAG_PASSAGES]:
                sections.append(f"- {passage}")

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
