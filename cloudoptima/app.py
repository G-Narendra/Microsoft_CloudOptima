"""Entry points: orchestrator wiring + a stdin-to-stdout CLI (Phase 6)."""

from __future__ import annotations

import asyncio
import json
import sys
from typing import Any, Final

from pydantic import ValidationError

from cloudoptima.config import Settings
from cloudoptima.models import Session
from cloudoptima.orchestrator import Orchestrator
from cloudoptima.safety import enforce_production_safety, moderate_input_fields
from cloudoptima.sanitize import DEFAULT_MAX_LENGTH, clean_input

CLI_USAGE: Final[str] = (
    "usage: echo '{\"project_name\": \"My App\", \"user_prompt\": \"...\"}' "
    "| python -m cloudoptima.app"
)


def create_orchestrator(settings: Settings) -> Orchestrator:
    """Wire the full orchestrator from application settings.

    Builds the LLM client for the configured provider and instantiates all
    five agents in pipeline order. In production mode (``demo_mode=False``)
    the Azure AI Content Safety layer is mandatory: the entry point fails
    closed instead of serving unguarded traffic (external principal-engineer
    review finding — real LLM runs require the ML safety layer).

    Args:
        settings: The application :class:`Settings`.

    Returns:
        A ready-to-run :class:`Orchestrator`.

    Raises:
        SafetyConfigurationError: When production mode is active but the ML
            safety resource is missing or disabled.
    """
    enforce_production_safety(settings)
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

    # Same first line of defense as the dashboard (build_session): clean every
    # user-supplied string before it enters the model, so hostile input (XSS,
    # SQL, null bytes) never survives into the session, the prompt, or the
    # printed output. Issue #2: when Azure AI Content Safety is enabled, the
    # cleaned fields are additionally moderated and blocked values are blanked.
    payload = _sanitize_payload(payload)
    payload, blocked = moderate_input_fields(payload, settings)
    if blocked:
        print(
            f"warning: blocked input field(s): {', '.join(blocked)}",
            file=sys.stderr,
        )

    try:
        session = Session.model_validate(payload)
    except ValidationError as exc:
        print(f"error: invalid session JSON: {exc}", file=sys.stderr)
        return 2

    try:
        # run() is async (round-3 P1); the CLI is a plain sync process, so we
        # bridge with asyncio.run and get the full parallel pipeline.
        result = asyncio.run(orchestrator.run(session))
    except Exception as exc:  # run() is designed not to raise; belt and suspenders
        print(f"error: pipeline failed: {exc}", file=sys.stderr)
        return 1

    print(result.model_dump_json(indent=2))
    return 0


def _sanitize_payload(payload: dict[str, Any]) -> dict[str, Any]:
    """Run user-supplied text fields through :func:`clean_input`.

    Mirrors the dashboard's ``build_session`` so the CLI and the UI enforce the
    same input contract. Enum fields and ``budget`` are passed through
    unchanged (pydantic validates their types).

    Args:
        payload: The parsed stdin session object.

    Returns:
        A new dict with the text fields cleaned (never raises).
    """
    cleaned = dict(payload)
    # Same caps as the dashboard's build_session: project names are short,
    # free-text fields allow the full default budget.
    limits = {
        "project_name": 120,
        "services": DEFAULT_MAX_LENGTH,
        "user_prompt": DEFAULT_MAX_LENGTH,
    }
    for field, max_length in limits.items():
        value = cleaned.get(field)
        if isinstance(value, str):
            cleaned[field] = clean_input(value, max_length=max_length)
    return cleaned


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
