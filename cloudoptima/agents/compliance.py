"""ComplianceOfficerAgent — checks the architecture against 21 hardcoded rules.

The compliance officer assesses the proposed architecture against the target
regulatory frameworks and the **21 immutable compliance rules** below.

The rules are hardcoded three times on purpose (a v1 lesson):

1. Here, as the ``COMPLIANCE_RULES`` constant — the single source of truth.
2. In the system prompt, **explicitly listed** (never referenced by name) so the
   model cannot invent or silently drop rules.
3. In validation — every ``rule_id`` in the output must match one of the 21,
   and if any rule is not PASS the overall status must be NEEDS_WORK.
"""

from __future__ import annotations

from typing import Any, Final

from cloudoptima.agent_base import BaseAgent
from cloudoptima.models import AgentType, Session

# ── The 21 immutable compliance rules (id, name, description) ────────────────
COMPLIANCE_RULES: Final[tuple[dict[str, str], ...]] = (
    {"id": "01", "name": "Data Residency",
     "description": "Customer data stored within approved geography"},
    {"id": "02", "name": "Encryption at Rest",
     "description": "All storage encrypted with AES-256"},
    {"id": "03", "name": "Encryption in Transit",
     "description": "TLS 1.2+ for all data in motion"},
    {"id": "04", "name": "Access Control",
     "description": "RBAC with least-privilege principle"},
    {"id": "05", "name": "Audit Logging",
     "description": "All access logged and monitored"},
    {"id": "06", "name": "Data Retention",
     "description": "Define and enforce retention policies"},
    {"id": "07", "name": "Right to Deletion",
     "description": "Users can request data deletion"},
    {"id": "08", "name": "Breach Notification",
     "description": "Notify authorities within 72 hours"},
    {"id": "09", "name": "Incident Response",
     "description": "Documented incident response plan"},
    {"id": "10", "name": "Vendor Assessment",
     "description": "Third-party vendors must meet standards"},
    {"id": "11", "name": "Data Classification",
     "description": "Classify data by sensitivity"},
    {"id": "12", "name": "Backup & Recovery",
     "description": "Regular backups with DR testing"},
    {"id": "13", "name": "Business Continuity",
     "description": "Documented BCP"},
    {"id": "14", "name": "Network Security",
     "description": "Segmentation, firewalls, DDoS protection"},
    {"id": "15", "name": "Patch Management",
     "description": "Regular security patching"},
    {"id": "16", "name": "Identity Management",
     "description": "MFA for all privileged access"},
    {"id": "17", "name": "Key Management",
     "description": "Managed HSM for encryption keys"},
    {"id": "18", "name": "Secure Development",
     "description": "SDLC with security reviews"},
    {"id": "19", "name": "Vulnerability Scanning",
     "description": "Regular scans with remediation SLAs"},
    {"id": "20", "name": "Staff Training",
     "description": "Security awareness training"},
    {"id": "21", "name": "Third-party Data",
     "description": "Agreements with data processors"},
)

_VALID_RULE_IDS: frozenset[str] = frozenset(rule["id"] for rule in COMPLIANCE_RULES)
_RULE_STATUSES: frozenset[str] = frozenset({"PASS", "FAIL", "WARNING", "CONFIG_NEEDED"})
_OVERALL_STATUSES: frozenset[str] = frozenset({"PASS", "NEEDS_WORK"})

# The rules, rendered once for the system prompt. Kept in the exact order of
# COMPLIANCE_RULES so the numbering cannot drift.
_RULES_TEXT: Final[str] = "\n".join(
    f"{rule['id']}. {rule['name']} — {rule['description']}" for rule in COMPLIANCE_RULES
)

_COMPLIANCE_SYSTEM_PROMPT = f"""\
You are a compliance officer. Assess the proposed architecture against the
target compliance frameworks and THE ONLY 21 RULES LISTED BELOW. These rules
are hardcoded — you must never invent, drop, or modify a rule.

THE 21 RULES:
{_RULES_TEXT}

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
        return "\n".join(
            [
                self._wrap_field("PROJECT NAME", session.project_name),
                self._wrap_field("AZURE REGION", getattr(session.region, "value", session.region)),
                self._wrap_field("COMPLIANCE FRAMEWORKS", frameworks),
                self._wrap_field("REQUIREMENTS", session.user_prompt),
                "ARCHITECT DESIGN (trusted pipeline output):",
                self._prior_turn_json(session, AgentType.ARCHITECT),
            ]
        )

    def _validate_output(self, data: dict[str, Any]) -> tuple[bool, str]:
        """Require known rule IDs and an overall status consistent with the rules."""
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
