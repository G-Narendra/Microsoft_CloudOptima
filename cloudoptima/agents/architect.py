"""ArchitectAgent — designs the compute, storage, networking, and data tiers.

The architect is the first agent in the pipeline. It reads the user's
requirements from the :class:`Session` and proposes a concrete Azure
architecture split into four sections, each carrying a recommendation, a
justification, and a list of alternatives.

The output contract is enforced by :meth:`ArchitectAgent._validate_output`:
all four sections must be present and each must carry the three required keys.
Anything else is rejected, so downstream agents and the dashboard never see a
half-built design.
"""

from __future__ import annotations

from typing import Any, Final

from cloudoptima.agent_base import BaseAgent
from cloudoptima.models import Session

# Sections that must be present in the architect's output, and the keys each
# section must carry. Kept as module constants so validation and the system
# prompt cannot drift apart.
_REQUIRED_SECTIONS: tuple[str, ...] = ("compute", "storage", "networking", "data")
_SECTION_KEYS: tuple[str, ...] = ("recommendation", "justification", "alternatives")

# Phase 10.2: the architect's contract is exactly these keys — nothing else.
_ALLOWED_KEYS: Final[frozenset[str]] = frozenset(_REQUIRED_SECTIONS)
_ALLOWED_SECTION_KEYS: Final[frozenset[str]] = frozenset(_SECTION_KEYS)

_ARCHITECT_SYSTEM_PROMPT = """\
You are a senior cloud architect with deep Azure expertise. Given the user's
requirements, design a concrete architecture split into four tiers: compute,
storage, networking, and data. For each tier, recommend a specific Azure
service (or a small set of services), justify the choice against the stated
workload, scale, and region, and list realistic alternatives.

Return ONLY valid JSON with exactly this structure — no prose outside the JSON:

{
  "compute": {
    "recommendation": "string",
    "justification": "string",
    "alternatives": ["string", "..."]
  },
  "storage": {
    "recommendation": "string",
    "justification": "string",
    "alternatives": ["string", "..."]
  },
  "networking": {
    "recommendation": "string",
    "justification": "string",
    "alternatives": ["string", "..."]
  },
  "data": {
    "recommendation": "string",
    "justification": "string",
    "alternatives": ["string", "..."]
  }
}
"""


class ArchitectAgent(BaseAgent):
    """Designs compute, storage, networking, and data tiers for a workload."""

    system_prompt: str = _ARCHITECT_SYSTEM_PROMPT

    def _build_prompt(self, session: Session) -> str:
        """Wrap the session's user-supplied fields in safe delimiters."""
        return "\n".join(
            [
                self._wrap_field("PROJECT NAME", session.project_name),
                self._wrap_field(
                    "WORKLOAD TYPE", getattr(session.workload_type, "value", session.workload_type)
                ),
                self._wrap_field(
                    "DEPLOYMENT SCALE", getattr(session.scale, "value", session.scale)
                ),
                self._wrap_field(
                    "AZURE REGION", getattr(session.region, "value", session.region)
                ),
                self._wrap_field("REQUIRED SERVICES", session.services),
                self._wrap_field("REQUIREMENTS", session.user_prompt),
            ]
        )

    def _validate_output(self, data: dict[str, Any]) -> tuple[bool, str]:
        """Require all four sections, each with recommendation/justification/alternatives."""
        ok, message = self._reject_unknown_keys(data, _ALLOWED_KEYS)
        if not ok:
            return False, message
        missing_sections = [
            section
            for section in _REQUIRED_SECTIONS
            if not isinstance(data.get(section), dict)
        ]
        if missing_sections:
            return False, f"missing or invalid section(s): {', '.join(missing_sections)}"

        for section in _REQUIRED_SECTIONS:
            ok, message = self._reject_unknown_keys(data[section], _ALLOWED_SECTION_KEYS)
            if not ok:
                return False, f"'{section}' has {message}"
            for key in _SECTION_KEYS:
                if key not in data[section]:
                    return False, f"'{section}' is missing '{key}'"
            if not isinstance(data[section]["alternatives"], list):
                return False, f"'{section}.alternatives' must be a list"
        return True, ""
