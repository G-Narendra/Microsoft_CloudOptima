"""CloudOptima — Multi-agent cloud architecture design system.

A multi-agent AI system where users describe infrastructure needs,
5 AI agents analyze the requirements, and a Judge agent resolves
conflicts to produce a complete architecture with cost, security,
and compliance reports.

Typical usage:
    >>> from cloudoptima.config import Settings
    >>> from cloudoptima.orchestrator import Orchestrator
    >>> settings = Settings()
    >>> orch = Orchestrator.from_settings(settings)
    >>> session = orch.run(session)
"""

from __future__ import annotations

__version__ = "0.1.0"
