"""Application entry points for CloudOptima — wiring and CLI (Phase 6).

Provides :func:`create_orchestrator` (wires the full pipeline from settings —
the dashboard imports this) and :func:`main` (a CLI that reads a Session JSON
object from stdin, runs the pipeline, and prints the updated session as JSON
to stdout). The CLI never prints API keys or secrets; the session model only
carries user inputs and pipeline output.

Usage:
    $ echo '{"project_name": "E-Shop", "user_prompt": "Design a scalable web app"}' \\
        | python -m cloudoptima.app
"""

from __future__ import annotations

import json
import sys
from typing import Any, Final

from pydantic import ValidationError

from cloudoptima.config import Settings
from cloudoptima.models import Session
from cloudoptima.orchestrator import Orchestrator

CLI_USAGE: Final[str] = (
    "usage: echo '{\"project_name\": \"My App\", \"user_prompt\": \"...\"}' "
    "| python -m cloudoptima.app"
)


def create_orchestrator(settings: Settings) -> Orchestrator:
    """Wire the full orchestrator from application settings.

    Builds the LLM client for the configured provider and instantiates all
    five agents in pipeline order.

    Args:
        settings: The application :class:`Settings`.

    Returns:
        A ready-to-run :class:`Orchestrator`.
    """
    return Orchestrator.from_settings(settings)


def main(argv: list[str] | None = None) -> int:
    """CLI entry point: read a Session JSON on stdin, run, print JSON.

    Exit codes: ``0`` success, ``1`` unexpected pipeline failure,
    ``2`` missing/malformed input.

    Args:
        argv: Reserved for future CLI flags (currently unused).

    Returns:
        The process exit code.
    """
    del argv

    _configure_utf8_stdio()

    payload = _read_stdin_payload()
    if payload is None:
        print(CLI_USAGE, file=sys.stderr)
        return 2

    settings = Settings()
    orchestrator = create_orchestrator(settings)

    try:
        session = Session.model_validate(payload)
    except ValidationError as exc:
        print(f"error: invalid session JSON: {exc}", file=sys.stderr)
        return 2

    try:
        result = orchestrator.run(session)
    except Exception as exc:  # run() is designed not to raise; belt and suspenders
        print(f"error: pipeline failed: {exc}", file=sys.stderr)
        return 1

    print(result.model_dump_json(indent=2))
    return 0


def _configure_utf8_stdio() -> None:
    """Reconfigure stdout/stderr to UTF-8 so Unicode output never crashes.

    On Windows the console defaults to cp1252, and generated artifacts contain
    characters outside that codec (e.g. the ``──`` separators in the Bicep
    template), which made ``print()`` raise ``UnicodeEncodeError`` after the
    pipeline had already succeeded. Best-effort: on platforms where
    ``reconfigure`` is unavailable this is a no-op.
    """
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is None:
            continue
        try:
            reconfigure(encoding="utf-8", errors="replace")
        except (OSError, ValueError):
            pass


def _read_stdin_payload() -> dict[str, Any] | None:
    """Read and parse a Session JSON object from stdin.

    Returns ``None`` (with a usage/error message on stderr) when stdin is a
    TTY, empty, not valid JSON, or not an object.
    """
    if sys.stdin is None or sys.stdin.isatty():
        return None

    raw = sys.stdin.read().strip()
    if not raw:
        return None

    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        print(f"error: stdin is not valid JSON: {exc}", file=sys.stderr)
        return None

    if not isinstance(parsed, dict):
        print("error: expected a JSON object on stdin", file=sys.stderr)
        return None
    return parsed


if __name__ == "__main__":
    raise SystemExit(main())
