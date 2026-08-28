"""SecurityEngineerAgent — scans the proposed architecture for vulnerabilities."""

from __future__ import annotations

from typing import Any, Final

from cloudoptima.agent_base import BaseAgent
from cloudoptima.models import AgentType, Session
from cloudoptima.sanitize import scan_for_malware_in_iac

_RISK_RATINGS: frozenset[str] = frozenset({"LOW", "MEDIUM", "HIGH", "CRITICAL"})
_ALLOWED_KEYS: Final[frozenset[str]] = frozenset(
    {"overall_risk_rating", "findings", "recommendations"}
)
_ALLOWED_FINDING_KEYS: Final[frozenset[str]] = frozenset(
    {"control", "status", "details", "cvss_score"}
)

_ROLE = "You are a cloud security engineer."
_CAPABILITIES = (
    "Assess the proposed architecture for vulnerabilities and configuration gaps across identity, network, data, and key management. "
    "Rate the overall risk and list concrete remediations."
)
_CONSTRAINTS = (
    "Findings must describe controls — they must never include executable code or commands. "
    "Return ONLY valid JSON with exactly the required structure — no prose outside the JSON."
)
_OUTPUT_SCHEMA = """{
  "overall_risk_rating": "LOW" or "MEDIUM" or "HIGH" or "CRITICAL",
  "findings": [
    {"control": "string", "status": "PASS" or "WARNING" or "CONFIG_NEEDED",
     "details": "string", "cvss_score": 0.0 or null}
  ],
  "recommendations": ["string", "..."]
}"""

_SECURITY_SYSTEM_PROMPT = f"""
# ROLE
{_ROLE}

# CAPABILITIES
{_CAPABILITIES}

# CONSTRAINTS
{_CONSTRAINTS}

# OUTPUT SCHEMA
{_OUTPUT_SCHEMA}
"""


class SecurityEngineerAgent(BaseAgent):
    """Finds vulnerabilities and rates the overall risk of the design."""

    system_prompt: str = _SECURITY_SYSTEM_PROMPT

    def _build_prompt(self, session: Session) -> str:
        """Wrap session fields and expose the architect's design for review."""
        return "\n".join(
            [
                self._wrap_field("PROJECT NAME", session.project_name),
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
            ]
        )

    def _validate_output(self, data: dict[str, Any]) -> tuple[bool, str]:
        """Require a valid risk rating and findings that carry no executable code."""
        ok, message = self._reject_unknown_keys(data, _ALLOWED_KEYS)
        if not ok:
            return False, message
        rating = data.get("overall_risk_rating")
        if rating not in _RISK_RATINGS:
            return False, (
                f"'overall_risk_rating' must be one of {sorted(_RISK_RATINGS)}, "
                f"got {rating!r}"
            )

        findings = data.get("findings")
        if not isinstance(findings, list):
            return False, "'findings' must be a list"
        for item in findings:
            if not isinstance(item, dict):
                return False, "each finding must be an object"
            ok, message = self._reject_unknown_keys(item, _ALLOWED_FINDING_KEYS)
            if not ok:
                return False, f"finding has {message}"
            for key in ("control", "status", "details"):
                if not isinstance(item.get(key), str):
                    return False, f"each finding must have a string '{key}'"
            cvss = item.get("cvss_score")
            if cvss is not None and (
                not isinstance(cvss, int | float) or isinstance(cvss, bool)
            ):
                return False, "'cvss_score' must be a number or null"
            # Details must never smuggle executable primitives into the plan.
            malware = scan_for_malware_in_iac(item.get("details"))
            if malware:
                return False, (
                    "finding details contain executable pattern(s): "
                    + ", ".join(malware)
                )

        recommendations = data.get("recommendations")
        if not isinstance(recommendations, list):
            return False, "'recommendations' must be a list"
        return True, ""
