"""Regression tests for the adversarial testing harness (issue #3).

The harness lives under ``scripts/redteam`` and is imported directly here.
These tests lock in the current security posture: there are **no** known-gap
attack cases left (the soft-tone rag_poison gap was closed by the always-on
offline floor in :mod:`cloudoptima.safety`, issue #2) and every payload in
the corpus is neutralized by at least one defense layer — so the ``--strict``
CI gate can never silently pass on an unblocked vector.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts" / "redteam"))

import redteam_cloudoptima as redteam  # noqa: E402


def test_no_known_gap_cases_remain() -> None:
    """The soft-tone gap is closed — nothing is excluded from the strict gate."""
    assert all(not case.known_gap for case in redteam.ATTACK_CASES)


def test_harness_blocks_every_attack_case() -> None:
    """Every payload is neutralized by at least one defense layer."""
    rows = redteam.run_harness()
    passed = [row for row in rows if row["passed"]]
    assert passed == [], [
        f"{row['vector']}: {row['payload']}" for row in passed
    ]
