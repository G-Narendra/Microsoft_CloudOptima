"""Input/output sanitization for CloudOptima.

Everything entering the system goes through :func:`clean_input`; everything
coming back from an LLM goes through :func:`clean_output`. Both always return a
string and never raise, because the orchestrator (Phase 6) must not crash on
hostile input.

Detection is kept separate from cleaning: :func:`detect_injection` reports
whether text looks like a jailbreak attempt without modifying it, so callers
decide whether to warn, log, or block.

Typical usage:
    >>> clean_input("  hello\\x00world  ")
    'helloworld'
    >>> detect_injection("Ignore previous instructions")
    True
    >>> extract_json('Here you go: {"a": 1}')
    {'a': 1}
"""

from __future__ import annotations

import json
import re
import threading
import time
import unicodedata
from typing import Any

__all__ = [
    "DEFAULT_MAX_LENGTH",
    "clean_input",
    "clean_output",
    "detect_injection",
    "extract_json",
    "rate_limit",
    "reset_rate_limits",
    "try_parse_json",
]

# Mirrors MAX_INPUT_LENGTH in .env.example. Phase 1's Settings should pass its
# own value explicitly.
DEFAULT_MAX_LENGTH = 5000

# C0/C1 controls, keeping tab, newline and carriage return.
_CONTROL_CHARS = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]")

# ANSI/VT sequences: CSI, OSC, and single-character escapes.
_ANSI_ESCAPE = re.compile(
    r"""
    \x1b \[ [0-?]* [ -/]* [@-~]
    | \x1b \] .*? (?: \x07 | \x1b\\ )
    | \x1b [@-Z\\-_]
    """,
    re.VERBOSE | re.DOTALL,
)

# SQL comment markers and quotes. '#' is excluded on purpose: it is MySQL-only
# and would mangle "C#" and "#1", which are common in Azure descriptions.
_SQL_COMMENT = re.compile(r"(--+|/\*|\*/)")
_SQL_QUOTES = re.compile(r"[\"';`]")

# Executable elements lose their content; other tags are dropped but their text
# survives, so "<b>budget</b>" reads as "budget".
_SCRIPT_BLOCK = re.compile(
    r"<\s*(script|style|iframe|object|embed)\b.*?<\s*/\s*\1\s*>", re.I | re.S
)
_DANGLING_SCRIPT = re.compile(r"<\s*/?\s*(script|style|iframe|object|embed)\b[^>]*>", re.I)
_HTML_TAG = re.compile(r"<[^>]*>")

# Only genuinely executable schemes. A bare "data:" is inert once tags are
# stripped, and matching it would eat the label in "Data: Azure SQL".
_JS_SCHEME = re.compile(r"\b(?:javascript|vbscript)\s*:|\bdata\s*:\s*text/html", re.I)

# Named handlers only. A generic \bon[a-z]+= also matches "online =".
_EVENT_HANDLER = re.compile(
    r"\bon(?:error|load|click|focus|blur|submit|change|input|toggle|scroll"
    r"|mouse\w+|key\w+|animation\w+|drag\w+|pointer\w+)\s*=",
    re.I,
)

# "../" and "..\" runs, plus a leading ~ home reference.
_PATH_TRAVERSAL = re.compile(r"(?:\.{2,}[\\/])+|^~[\\/]?|(?<=[\s\"'])~[\\/]")

# Jailbreak heuristics. These only report, so they favour precision over
# recall: "act as a reverse proxy" is ordinary architecture prose.
_INJECTION_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"\bignore\b[^.\n]{0,40}\b(?:previous|prior|above|earlier|all)\b", re.I),
    re.compile(r"\b(?:disregard|forget|override|bypass)\b[^.\n]{0,40}\b"
               r"(?:instruction|prompt|rule|direction|guideline)", re.I),
    re.compile(r"\byou\s+are\s+now\b", re.I),
    re.compile(r"\b(?:act\s+as|pretend\s+(?:to\s+be|you(?:\s+are)?))\s+"
               r"(?:a|an|the)?\s*(?:helpful\s+)?"
               r"(?:AI|assistant|chatbot|language\s+model|LLM|bot|hacker|DAN|"
               r"unrestricted|jailbroken|different)\b", re.I),
    re.compile(r"\bdo\s+anything\s+now\b|\bjailbreak\b|\bdeveloper\s+mode\b", re.I),
    # Case-sensitive so the name "Dan" is not treated as the DAN jailbreak.
    re.compile(r"\bDAN\b"),
    re.compile(r"\b(?:reveal|show|print|repeat|output|tell\s+me)\b[^.\n]{0,40}\b"
               r"(?:system\s+prompt|initial\s+prompt|instructions?)\b", re.I),
    re.compile(r"\bdisable\b[^.\n]{0,40}\b(?:security|safety|encryption|mfa|control|filter)", re.I),
    re.compile(r"^\s*(?:system|assistant|user)\s*:", re.I | re.M),
    re.compile(r"---\s*(?:END|BEGIN|START)\b[^-]*---", re.I),
    re.compile(r"<\s*/?\s*(?:system|im_start|im_end)\b", re.I),
)

# Phrases an LLM should never echo back to the UI.
_LEAKAGE_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"^\s*(?:system|assistant)\s*prompt\s*:.*$", re.I | re.M),
    re.compile(r"<\s*/?\s*(?:system|im_start|im_end)\b[^>]*>", re.I),
    re.compile(r"^\s*(?:system|assistant)\s*:\s*", re.I | re.M),
)

# Cyrillic/Greek lookalikes that survive NFKC. See BUILD_CHECKLIST Phase 10.5
# ("UAE Nortе" with a Cyrillic 'е').
_CONFUSABLES: dict[str, str | int | None] = {
    "а": "a", "е": "e", "о": "o", "р": "p",
    "с": "c", "х": "x", "у": "y", "і": "i",
    "А": "A", "Е": "E", "О": "O", "Р": "P",
    "С": "C", "Х": "X", "І": "I", "М": "M",
    "ο": "o", "Α": "A", "Β": "B", "Η": "H",
    "⁄": "/", "∕": "/",
}
_CONFUSABLE_TABLE = str.maketrans(_CONFUSABLES)

_JSON_OBJECT = re.compile(r"\{.*\}", re.S)
_JSON_ARRAY = re.compile(r"\[.*\]", re.S)
_CODE_FENCE = re.compile(r"```(?:json|javascript)?\s*(.*?)```", re.S | re.I)


def _normalize_unicode(text: str) -> str:
    """Fold compatibility forms and homoglyphs to their ASCII equivalents."""
    text = unicodedata.normalize("NFKC", text)
    return text.translate(_CONFUSABLE_TABLE)


def _strip_html(text: str) -> str:
    """Remove executable markup, keeping the readable text of benign tags."""
    text = _SCRIPT_BLOCK.sub(" ", text)
    text = _DANGLING_SCRIPT.sub(" ", text)
    text = _EVENT_HANDLER.sub(" ", text)
    text = _JS_SCHEME.sub(" ", text)
    return _HTML_TAG.sub("", text)


def clean_input(text: object, max_length: int = DEFAULT_MAX_LENGTH) -> str:
    """Clean untrusted user input. Always returns a string; never raises.

    Strips null bytes and control characters, normalizes Unicode homoglyphs,
    removes HTML/JS injection, neutralizes SQL metacharacters, strips path
    traversal, collapses whitespace, and truncates to ``max_length``.

    Non-string input is coerced with ``str``; ``None`` becomes ``""``.

    Args:
        text: The untrusted value to clean.
        max_length: Maximum length of the result, in characters.

    Returns:
        The cleaned text, at most ``max_length`` characters.
    """
    if text is None:
        return ""
    if not isinstance(text, str):
        text = str(text)

    text = _normalize_unicode(text)
    # ANSI before controls: ESC is itself a control char, and removing it first
    # would leave "[31m" behind as literal text.
    text = _ANSI_ESCAPE.sub("", text)
    text = _CONTROL_CHARS.sub("", text)
    text = _strip_html(text)
    text = _PATH_TRAVERSAL.sub("", text)
    text = _SQL_COMMENT.sub("", text)
    text = _SQL_QUOTES.sub("", text)

    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = text.strip()

    if max_length >= 0 and len(text) > max_length:
        text = text[:max_length].rstrip()
    return text


def clean_output(text: object, max_length: int = DEFAULT_MAX_LENGTH * 10) -> str:
    """Clean an LLM response before parsing or display. Never raises.

    Strips ANSI codes and control characters, removes system-prompt leakage,
    and neutralizes HTML so the dashboard can render the result as plain text
    (Streamlit must never use ``unsafe_allow_html``).

    Quotes and braces survive, so this is safe to call before
    :func:`extract_json`.

    Args:
        text: The raw model response.
        max_length: Maximum length of the result, in characters.

    Returns:
        The cleaned text, at most ``max_length`` characters.
    """
    if text is None:
        return ""
    if not isinstance(text, str):
        text = str(text)

    # ANSI before controls, as in clean_input.
    text = _ANSI_ESCAPE.sub("", text)
    text = _CONTROL_CHARS.sub("", text)
    for pattern in _LEAKAGE_PATTERNS:
        text = pattern.sub("", text)
    text = _SCRIPT_BLOCK.sub(" ", text)
    text = _DANGLING_SCRIPT.sub(" ", text)
    text = _EVENT_HANDLER.sub(" ", text)
    text = _JS_SCHEME.sub(" ", text)
    text = text.strip()

    if max_length >= 0 and len(text) > max_length:
        text = text[:max_length].rstrip()
    return text


def try_parse_json(text: object) -> tuple[Any | None, str | None]:
    """Attempt a strict JSON parse. Never raises.

    Args:
        text: Candidate JSON text.

    Returns:
        ``(data, None)`` on success, or ``(None, error_message)`` on failure.
    """
    if not isinstance(text, str) or not text.strip():
        return None, "empty or non-string input"
    try:
        return json.loads(text), None
    except (json.JSONDecodeError, ValueError, RecursionError) as exc:
        return None, str(exc)


def extract_json(text: object) -> Any | None:
    """Pull a JSON value out of a model response. Never raises.

    Models wrap JSON in prose or code fences, so this makes four attempts in
    order: direct parse, fenced code block, outermost ``{...}``, outermost
    ``[...]``.

    Args:
        text: The model response to search.

    Returns:
        The parsed JSON value, or ``None`` if nothing parseable was found.
    """
    if not isinstance(text, str) or not text.strip():
        return None

    data, _ = try_parse_json(text.strip())
    if data is not None:
        return data

    fence = _CODE_FENCE.search(text)
    if fence:
        data, _ = try_parse_json(fence.group(1).strip())
        if data is not None:
            return data

    # Try whichever delimiter opens first, so "[{...}]" yields the array rather
    # than its first element.
    brace = text.find("{")
    bracket = text.find("[")
    array_first = bracket != -1 and (brace == -1 or bracket < brace)
    patterns = (_JSON_ARRAY, _JSON_OBJECT) if array_first else (_JSON_OBJECT, _JSON_ARRAY)

    for pattern in patterns:
        match = pattern.search(text)
        if match:
            data, _ = try_parse_json(match.group(0))
            if data is not None:
                return data

    return None


def detect_injection(text: object) -> bool:
    """Report whether text looks like a prompt-injection or jailbreak attempt.

    Detection only; the text is not modified. Checks the raw value and a
    Unicode-normalized copy so homoglyph obfuscation still trips the patterns.

    Args:
        text: The text to inspect.

    Returns:
        ``True`` if any known injection pattern matches.
    """
    if not isinstance(text, str) or not text.strip():
        return False

    candidates = {text, _normalize_unicode(text)}
    return any(p.search(c) for c in candidates for p in _INJECTION_PATTERNS)


class _RateLimiter:
    """Thread-safe sliding-window counter keyed by an arbitrary string."""

    def __init__(self) -> None:
        self._calls: dict[str, list[float]] = {}
        self._lock = threading.Lock()

    def allow(self, key: str, max_calls: int, window_sec: float) -> bool:
        if max_calls <= 0:
            return False
        now = time.monotonic()
        cutoff = now - window_sec
        with self._lock:
            timestamps = [t for t in self._calls.get(key, []) if t > cutoff]
            if len(timestamps) >= max_calls:
                self._calls[key] = timestamps
                return False
            timestamps.append(now)
            self._calls[key] = timestamps
            return True

    def reset(self, key: str | None = None) -> None:
        with self._lock:
            if key is None:
                self._calls.clear()
            else:
                self._calls.pop(key, None)


_LIMITER = _RateLimiter()


def rate_limit(key: str, max_calls: int, window_sec: float) -> bool:
    """Check and record a call against an in-memory sliding window.

    Call this before invoking the LLM so blocked requests cost no API credits.
    State is per-process and keys are retained for the life of the process, so
    a multi-worker or long-running deployment needs a shared backend with
    eviction (Phase 14).

    Args:
        key: Identifier to limit on, e.g. a session id or ``"global"``.
        max_calls: Maximum calls permitted within the window.
        window_sec: Window length in seconds.

    Returns:
        ``True`` if the call is allowed (and now counted), ``False`` if the
        caller has exhausted its quota.
    """
    return _LIMITER.allow(key, max_calls, window_sec)


def reset_rate_limits(key: str | None = None) -> None:
    """Clear rate-limit state for ``key``, or all keys when ``key`` is ``None``."""
    _LIMITER.reset(key)
