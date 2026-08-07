"""The 21 compliance rules — one immutable source of truth (Phase 8.1).

These rules used to be hardcoded inside the compliance agent. They now live
here so any module can import them, and they stay immutable:

- ``COMPLIANCE_RULES`` is keyed by rule id and wrapped in
  :class:`types.MappingProxyType`, so nothing can add, remove, or edit a rule
  at runtime.
- :func:`render_rules_text` produces the ``"01. Name — description"`` block
  the compliance agent embeds in its system prompt, so the LLM sees the rules
  explicitly (never by reference) — the Phase 10.2 AI-poisoning defense.
- The agent's validation checks every ``rule_id`` against :data:`RULE_IDS`,
  so a model can't invent, drop, or rewrite a rule.

Coverage per BUILD_CHECKLIST Phase 8.1: residency, encryption, access control,
audit logging, retention, incident response, vendor assessment, DR, network
security, and identity.
"""

from __future__ import annotations

from types import MappingProxyType
from typing import Final

# (id, name, description). A tuple, so the set of rules is fixed at import
# time. Each entry is a plain dict kept private; the public views below are
# read-only proxies.
_COMPLIANCE_RULES: Final[tuple[tuple[str, str, str], ...]] = (
    ("01", "Data Residency", "Customer data stored within approved geography"),
    ("02", "Encryption at Rest", "All storage encrypted with AES-256"),
    ("03", "Encryption in Transit", "TLS 1.2+ for all data in motion"),
    ("04", "Access Control", "RBAC with least-privilege principle"),
    ("05", "Audit Logging", "All access logged and monitored"),
    ("06", "Data Retention", "Define and enforce retention policies"),
    ("07", "Right to Deletion", "Users can request data deletion"),
    ("08", "Breach Notification", "Notify authorities within 72 hours"),
    ("09", "Incident Response", "Documented incident response plan"),
    ("10", "Vendor Assessment", "Third-party vendors must meet standards"),
    ("11", "Data Classification", "Classify data by sensitivity"),
    ("12", "Backup & Recovery", "Regular backups with DR testing"),
    ("13", "Business Continuity", "Documented BCP"),
    ("14", "Network Security", "Segmentation, firewalls, DDoS protection"),
    ("15", "Patch Management", "Regular security patching"),
    ("16", "Identity Management", "MFA for all privileged access"),
    ("17", "Key Management", "Managed HSM for encryption keys"),
    ("18", "Secure Development", "SDLC with security reviews"),
    ("19", "Vulnerability Scanning", "Regular scans with remediation SLAs"),
    ("20", "Staff Training", "Security awareness training"),
    ("21", "Third-party Data", "Agreements with data processors"),
)

# Public immutable views — MappingProxyType raises TypeError on assignment.
COMPLIANCE_RULES: Final[MappingProxyType[str, MappingProxyType[str, str]]] = (
    MappingProxyType(
        {
            rule_id: MappingProxyType(
                {"id": rule_id, "name": name, "description": description}
            )
            for rule_id, name, description in _COMPLIANCE_RULES
        }
    )
)

#: The exact set of valid rule ids — validation authority for the agent.
RULE_IDS: Final[frozenset[str]] = frozenset(rule_id for rule_id, _, _ in _COMPLIANCE_RULES)

#: Ordered list of the 21 rule names (for display and prompt rendering).
RULE_NAMES: Final[tuple[str, ...]] = tuple(name for _, name, _ in _COMPLIANCE_RULES)


def get_rule(rule_id: str) -> MappingProxyType[str, str] | None:
    """Return the rule with ``rule_id`` (e.g. ``"05"``), or ``None``.

    Args:
        rule_id: Two-digit rule id from ``"01"`` to ``"21"``.

    Returns:
        A read-only ``{"id", "name", "description"}`` mapping, or ``None``.
    """
    return COMPLIANCE_RULES.get(rule_id)


def render_rules_text() -> str:
    """Render the 21 rules as the prompt block ``"01. Name — description"``.

    Kept in the exact order of :data:`COMPLIANCE_RULES` so the numbering can
    never drift from the ids.
    """
    return "\n".join(
        f"{rule_id}. {name} — {description}"
        for rule_id, name, description in _COMPLIANCE_RULES
    )
