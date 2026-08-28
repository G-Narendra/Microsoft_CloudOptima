"""The 21 immutable compliance rules for regulatory auditing."""

from __future__ import annotations

from types import MappingProxyType
from typing import Final

_COMPLIANCE_RULES: Final[tuple[tuple[str, str, str], ...]] = (
    ("01", "PDPL Art. 29 (Data Residency)", "Personal data stored within KSA approved geography"),
    ("02", "GDPR Art. 32 (Encryption at Rest)", "All storage encrypted with AES-256 (Data at rest)"),
    ("03", "PCI-DSS Req 4 (Encryption in Transit)", "TLS 1.2+ for all data in motion across public networks"),
    ("04", "SOC 2 CC6.1 (Access Control)", "Logical access restricted via RBAC with least-privilege principle"),
    ("05", "HIPAA 164.312(b) (Audit Logging)", "Hardware, software, and procedural mechanisms to record and examine access"),
    ("06", "GDPR Art. 5(1)(e) (Data Retention)", "Define and enforce data retention policies (kept no longer than necessary)"),
    ("07", "GDPR Art. 17 (Right to Deletion)", "Users can request personal data deletion (Right to be forgotten)"),
    ("08", "GDPR Art. 33 (Breach Notification)", "Notify supervisory authorities within 72 hours of a breach"),
    ("09", "SOC 2 CC7.3 (Incident Response)", "Documented incident response plan to evaluate, respond, and mitigate"),
    ("10", "ISO 27001 A.15.1.1 (Vendor Assessment)", "Information security policy for supplier relationships must be agreed"),
    ("11", "ISO 27001 A.8.2.1 (Data Classification)", "Information classified by legal requirements, value, criticality and sensitivity"),
    ("12", "SOC 2 A1.2 (Backup & Recovery)", "Regular backups with Disaster Recovery testing (RTO/RPO objectives)"),
    ("13", "ISO 27001 A.17.1.2 (Business Continuity)", "Documented Business Continuity Procedures (BCP) implemented and tested"),
    ("14", "PCI-DSS Req 1 (Network Security)", "Install and maintain firewall configuration (Segmentation, DDoS protection)"),
    ("15", "PCI-DSS Req 6.2 (Patch Management)", "Regular security patching; install critical patches within 30 days"),
    ("16", "NIST CSF PR.AC-1 (Identity Management)", "MFA and managed identities enforced for all privileged access"),
    ("17", "NIST CSF PR.DS-1 (Key Management)", "Cryptographic keys managed securely via Managed HSM or Key Vault"),
    ("18", "ISO 27001 A.14.2.1 (Secure Development)", "Secure Software Development Life Cycle (SDLC) with security reviews"),
    ("19", "PCI-DSS Req 11.2 (Vulnerability Scanning)", "Internal and external vulnerability scans at least quarterly"),
    ("20", "HIPAA 164.308(a)(5) (Staff Training)", "Security awareness training program for all members of the workforce"),
    ("21", "GDPR Art. 28 (Third-party Data)", "Processing by a processor shall be governed by a contract (DPA)"),
)

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

RULE_IDS: Final[frozenset[str]] = frozenset(rule_id for rule_id, _, _ in _COMPLIANCE_RULES)
RULE_NAMES: Final[tuple[str, ...]] = tuple(name for _, name, _ in _COMPLIANCE_RULES)


def get_rule(rule_id: str) -> MappingProxyType[str, str] | None:
    """Return the rule with rule_id, or None."""
    return COMPLIANCE_RULES.get(rule_id)


def render_rules_text() -> str:
    """Render the 21 rules formatted for prompt injection."""
    return "\n".join(
        f"{rule_id}. {name} — {description}"
        for rule_id, name, description in _COMPLIANCE_RULES
    )
