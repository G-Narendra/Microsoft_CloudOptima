"""Azure AI Content Safety + Prompt Shields (issue #2) — optional ML layer.

The regex defense in :mod:`cloudoptima.sanitize` is the first line of defense;
this module adds Microsoft's ML-based moderation on top, following the same
graceful-degradation contract as the live pricing module: when the Azure
resource (endpoint + key) is missing, disabled, or the call fails, we return a
"no verdict" result and the regex layer keeps enforcing. The app never breaks
without the Azure resource.

Layer 1.5 (always on, no credentials): an offline deterministic floor
(:func:`_offline_harm_scan` / :func:`_offline_indirect_scan`) flags the most
obvious harm phrases ("kill all users", "attack the server") and soft-tone
indirect attacks ("from now on you are...", "ignore previous instructions")
that regex alone misses. The curated lists are deliberately explicit phrases,
not single words, so legitimate engineering language ("kill the process") is
never flagged. When the floor fires the verdict source is ``"offline"`` — the
caller still has a real signal to act on even in degraded mode.

Two capabilities, mirroring the Azure AI Content Safety service:

- :func:`moderate_text` — harm categories (Hate / SelfHarm / Sexual / Violence)
  with severity 0-6; blocked when any category reaches the configured
  threshold (default 4 = Medium and above).
- :func:`shield_prompt` — Prompt Shields: detects **user-prompt attacks** and
  **document / indirect attacks** (the exact vector our RAG filter hardens in
  ``compliance/rag.py``).

Typical usage:
    >>> verdict = moderate_text(\"I hate you\", settings)
    >>> verdict.source
    'disabled'   # no endpoint configured — regex layer still enforces
"""

from __future__ import annotations

import logging
import threading
from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Any, Final

from cloudoptima.config import Settings

_logger = logging.getLogger(__name__)

# Guarded import: azure-ai-contentsafety is an optional dependency (extra
# `safety`). Everything in this module works without it — verdicts degrade to
# "offline"/"disabled" and callers fall back to the regex layer.
try:  # pragma: no cover - exercised only when azure-ai-contentsafety is installed
    from azure.ai.contentsafety import ContentSafetyClient

    CONTENT_SAFETY_AVAILABLE = True
except Exception:  # pragma: no cover - exercised only when the package is missing
    CONTENT_SAFETY_AVAILABLE = False

#: Block severity threshold when none is configured explicitly (0-6; 4 = Medium).
DEFAULT_THRESHOLD: Final[int] = 4

#: The four harm categories the moderation API scores.
_CATEGORIES: Final[tuple[str, ...]] = ("Hate", "SelfHarm", "Sexual", "Violence")

#: Always-on offline floor (layer 1.5) — blatant harm phrases flagged with no
#: Azure resource configured. Deliberately explicit phrases, not single words:
#: "kill the process" is legitimate ops language, "kill all users" is not.
#: Severity 6 (High) is assigned so any non-zero threshold blocks.
_OFFLINE_HARM_PHRASES: Final[dict[str, tuple[str, ...]]] = {
    "Violence": (
        "kill all users",
        "kill everyone",
        "kill them all",
        "bomb the",
        "attack the server",
        "attack this server",
        "hack the server",
        "launch a ddos",
        "ddos the",
        "steal credentials",
    ),
    "SelfHarm": (
        "kill myself",
        "kill yourself",
        "end my life",
        "commit suicide",
    ),
}

#: Always-on offline floor — soft-tone direct/indirect attack phrases the regex
#: layer cannot reliably catch (the ML Prompt Shield's job when configured).
_OFFLINE_INDIRECT_PHRASES: Final[tuple[str, ...]] = (
    "ignore previous instructions",
    "ignore all previous",
    "disregard all prior",
    "forget your instructions",
    "from now on you are",
    "you are now a",
    "always approve",
    "always accept",
    "never reject",
    "mark every compliance rule as pass",
    "reveal your system prompt",
    "jailbreak",
    "developer mode",
)


@dataclass(frozen=True)
class SafetyVerdict:
    """Outcome of :func:`moderate_text`.

    Attributes:
        categories: category name -> severity (0-6). Empty when the ML layer
            was not available or not configured.
        blocked:    True when any severity >= the configured threshold.
        source:     ``\"azure\"`` when the API answered, ``\"offline\"`` when the
            deterministic floor flagged obvious harm or the API was
            unreachable, ``\"disabled\"`` when no endpoint/key was set and the
            floor did not fire.
    """

    categories: dict[str, int] = field(default_factory=dict)
    blocked: bool = False
    source: str = "disabled"


@dataclass(frozen=True)
class ShieldVerdict:
    """Outcome of :func:`shield_prompt`.

    Attributes:
        user_prompt_attack: True when the user prompt itself carries an attack.
        documents_attack:   Per-document attack flags (same order as input).
        source:             ``\"azure\"`` when the API answered, ``\"offline\"``
            when the deterministic floor flagged an attack, ``\"disabled\"``
            otherwise.
    """

    user_prompt_attack: bool = False
    documents_attack: list[bool] = field(default_factory=list)
    source: str = "disabled"


# ── Client management ────────────────────────────────────────────────────
_client: ContentSafetyClient | None = None
_client_lock = threading.Lock()


def configure(endpoint: str, key: str) -> None:
    """Create the shared Content Safety client from explicit credentials.

    Also called internally from :func:`_get_client` with the settings values.
    A missing/blank endpoint or key resets the client to ``None``.
    """
    global _client
    with _client_lock:
        if not endpoint or not key or not CONTENT_SAFETY_AVAILABLE:
            _client = None
            return
        try:
            from azure.core.credentials import AzureKeyCredential

            _client = ContentSafetyClient(endpoint, AzureKeyCredential(key))
        except Exception:
            _logger.warning("Content Safety client creation failed", exc_info=True)
            _client = None


def _get_client(settings: Settings | None) -> ContentSafetyClient | None:
    """Return the shared client, lazily built from ``settings`` when present."""
    if _client is None:
        if settings is None:
            return None
        configure(
            settings.content_safety_endpoint,
            settings.content_safety_api_key.get_secret_value(),
        )
    return _client


def _is_enabled(settings: Settings | None) -> bool:
    """True when the feature is on AND credentials exist."""
    if settings is None or not settings.content_safety_enabled:
        return False
    return bool(
        settings.content_safety_endpoint
        and settings.content_safety_api_key.get_secret_value()
    )


def _threshold(settings: Settings | None) -> int:
    """Effective severity threshold from settings (or the default)."""
    if settings is None:
        return DEFAULT_THRESHOLD
    return settings.content_safety_threshold


# ── Public API ────────────────────────────────────────────────────────────

def moderate_text(
    text: object,
    settings: Settings | None = None,
) -> SafetyVerdict:
    """Score ``text`` for harmful content with Azure AI Content Safety.

    Never raises and never blocks on its own — it *reports*. Callers decide
    what to do with a ``blocked`` verdict (replace the field, reject the
    input, log it).

    Args:
        text:     The text to moderate.
        settings: App settings; when disabled or credential-less the verdict
            is ``source=\"disabled\"`` and the regex layer keeps enforcing.

    Returns:
        A :class:`SafetyVerdict` with per-category severities. Empty
        categories + ``source=\"disabled\"/\"offline\"`` mean "no ML verdict".
    """
    verdict = SafetyVerdict()
    if not isinstance(text, str) or not text.strip():
        return verdict

    # Layer 1.5 — always-on deterministic floor: blatant harm phrases are
    # flagged even with no Azure resource, so degraded mode still blocks the
    # obvious cases and the regex layer handles the technical ones. Base64-
    # encoded threats are decoded and re-scanned (a PyRIT-campaign finding).
    from cloudoptima.sanitize import decode_base64_tokens

    offline = _offline_harm_scan(text)
    for candidate in decode_base64_tokens(text):
        offline = offline or _offline_harm_scan(candidate)
        if offline:
            break
    if offline:
        return SafetyVerdict(categories=offline, blocked=True, source="offline")

    if not _is_enabled(settings):
        return verdict
    client = _get_client(settings)
    if client is None:
        return verdict

    try:
        response = client.analyze_text(_moderate_options(text))
        severities: dict[str, int] = {}
        for analysis in response.categories_analysis:
            category = str(getattr(analysis.category, "value", analysis.category))
            severity = int(getattr(analysis, "severity", 0) or 0)
            severities[category] = severity
        blocked = max(severities.values(), default=0) >= _threshold(settings)
        return SafetyVerdict(
            categories=severities,
            blocked=blocked,
            source="azure",
        )
    except Exception as exc:  # network, auth, throttling — degrade, never raise
        _logger.warning("Content Safety moderation failed — degrading to offline: %s", exc)
        return SafetyVerdict(source="offline")


def shield_prompt(
    user_prompt: str,
    documents: Sequence[object] | None = None,
    settings: Settings | None = None,
) -> ShieldVerdict:
    """Run Prompt Shields over a user prompt and/or untrusted documents.

    The document shield is the ML counterpart of the RAG injection filter:
    hostile passage content (\"ignore previous instructions...\") that slips
    past regexes still trips the shield, so it is dropped before it can reach
    an LLM prompt.

    Args:
        user_prompt: The user-facing prompt text (may be empty).
        documents:   Untrusted document/passage texts to scan for indirect
            attacks.
        settings:    App settings (see :func:`moderate_text`).

    Returns:
        A :class:`ShieldVerdict`; empty lists + ``source=\"disabled\"`` mean
        no ML verdict was produced.
    """
    docs = [str(d) for d in (documents or []) if isinstance(d, str) and d.strip()]
    user_prompt_text = str(user_prompt or "")

    # Layer 1.5 — always-on deterministic floor: direct and indirect attacks
    # the regex layer misses are flagged here, no credentials needed. The ML
    # shield adds ML-grade detection on top when Content Safety is configured.
    # Base64-encoded attacks are decoded and re-scanned (PyRIT finding).
    from cloudoptima.sanitize import decode_base64_tokens

    def _scan(text: str) -> bool:
        return _offline_indirect_scan(text) or any(
            _offline_indirect_scan(candidate)
            for candidate in decode_base64_tokens(text)
        )

    user_hit = _scan(user_prompt_text)
    doc_hits = [_scan(d) for d in docs]
    if user_hit or any(doc_hits):
        return ShieldVerdict(
            user_prompt_attack=user_hit,
            documents_attack=doc_hits,
            source="offline",
        )

    if settings is None or not _is_enabled(settings):
        return ShieldVerdict(source="disabled")
    if not user_prompt_text.strip() and not docs:
        return ShieldVerdict(source="disabled")

    # ML Prompt Shields — SDK path first when the installed build exposes the
    # shield fields (capability-gated via _shield_supported).
    client = _get_client(settings)
    if client is not None and _shield_supported():
        try:
            response = client.analyze_text(_shield_options(user_prompt_text, docs))
            prompt_analysis = getattr(response, "user_prompt_analysis", None)
            user_attack = bool(getattr(prompt_analysis, "attack_detected", False))
            doc_attacks: list[bool] = []
            for analysis in getattr(response, "documents_analysis", None) or []:
                doc_attacks.append(bool(getattr(analysis, "attack_detected", False)))
            return ShieldVerdict(
                user_prompt_attack=user_attack,
                documents_attack=doc_attacks,
                source="azure",
            )
        except Exception as exc:
            _logger.warning(
                "Prompt Shields SDK call failed — trying the REST endpoint: %s", exc
            )

    # The 1.x SDK ships text moderation only; Prompt Shields (user-prompt +
    # document/indirect attack detection) live behind the REST API. Call the
    # real Azure endpoint when the resource is configured.
    rest = _shield_prompt_rest(settings, user_prompt_text, docs)
    if rest is not None:
        return rest
    return ShieldVerdict(source="offline")


def _offline_harm_scan(text: str) -> dict[str, int]:
    """Flag blatant harm phrases with no Azure resource (severity 6 each).

    Returns an empty dict when the text is clean. Callers treat a hit as a
    ``blocked`` verdict with ``source=\"offline\"``.
    """
    lowered = text.lower()
    hits: dict[str, int] = {}
    for category, phrases in _OFFLINE_HARM_PHRASES.items():
        if any(phrase in lowered for phrase in phrases):
            hits[category] = 6
    return hits


def _offline_indirect_scan(text: str) -> bool:
    """True when ``text`` carries an obvious direct/indirect attack phrase.

    The phrases mirror what the ML Prompt Shield looks for (user-prompt and
    document attacks) but work offline — deterministic and dependency-free.
    """
    lowered = text.lower()
    return any(phrase in lowered for phrase in _OFFLINE_INDIRECT_PHRASES)


def _moderate_options(text: str) -> Any:
    """Build moderation SDK options without a hard module-level dependency.

    ``azure-ai-contentsafety`` is optional; when it is missing (offline
    installs, tests) we pass a plain dict and let the (fake or real) client
    handle it. The real client only ever receives the typed object because it
    only exists when the package is installed.
    """
    try:
        from azure.ai.contentsafety.models import AnalyzeTextOptions

        return AnalyzeTextOptions(text=text)
    except Exception:  # pragma: no cover - exercised only when the package is missing
        return {"text": text}


def _shield_prompt_rest(
    settings: Settings,
    user_prompt: str,
    documents: list[str],
) -> ShieldVerdict | None:
    """Call Azure AI Content Safety Prompt Shields over REST (issue #2).

    ``text:shieldPrompt`` returns per-input ``attackDetected`` flags for the
    user prompt (direct attacks) and each document (indirect / document
    attacks) — the exact ML defense our RAG filter hardens in
    ``compliance/rag.py``. ``httpx`` is a core dependency, so this needs no
    extra packages beyond the Content Safety resource itself.

    Args:
        settings:  App settings (endpoint + key, must be configured).
        user_prompt: The user-facing prompt text.
        documents:  Untrusted document/passage texts to scan.

    Returns:
        A :class:`ShieldVerdict` with ``source=\"azure\"`` on success, or
        ``None`` when the resource is missing or the call fails (caller
        degrades to the offline floor / regex layer).
    """
    endpoint = settings.content_safety_endpoint
    key = settings.content_safety_api_key.get_secret_value()
    if not (endpoint and key):
        return None
    try:
        import httpx

        url = (
            f"{endpoint.rstrip('/')}/contentsafety/text:shieldPrompt"
            "?api-version=2024-02-15-preview"
        )
        response = httpx.post(
            url,
            json={"userPrompt": user_prompt, "documents": documents},
            headers={"Ocp-Apim-Subscription-Key": key},
            timeout=10.0,
        )
        response.raise_for_status()
        data = response.json()
        user_attack = bool(
            (data.get("userPromptAnalysis") or {}).get("attackDetected", False)
        )
        doc_attacks = [
            bool(analysis.get("attackDetected", False))
            for analysis in (data.get("documentsAnalysis") or [])
        ]
        return ShieldVerdict(
            user_prompt_attack=user_attack,
            documents_attack=doc_attacks,
            source="azure",
        )
    except Exception as exc:
        _logger.warning("Prompt Shields REST call failed — degrading: %s", exc)
        return None


def _shield_options(user_prompt: str, documents: list[str]) -> Any:
    """Build Prompt Shields SDK options (see :func:`_moderate_options`).

    Uses the mapping constructor so a future SDK that supports shields can
    receive the fields; the current 1.x build is capability-gated out in
    :func:`shield_prompt` via :func:`_shield_supported`, so this path only
    runs against an SDK that accepts them.
    """
    try:
        from azure.ai.contentsafety.models import AnalyzeTextOptions

        return AnalyzeTextOptions(
            mapping={"user_prompt": user_prompt, "documents": documents}
        )
    except Exception:  # pragma: no cover - exercised only when the package is missing
        return {"user_prompt": user_prompt, "documents": documents}


def _shield_supported() -> bool:
    """True when the installed SDK build exposes the Prompt Shields fields.

    Prompt Shields arrived in the Content Safety SDK after text moderation;
    some 1.x builds ship moderation only. Capability-gating keeps
    :func:`shield_prompt` honest: with an SDK that cannot shield, the verdict
    is ``disabled`` and the regex + RAG filters remain the enforcement.
    """
    try:
        from azure.ai.contentsafety.models import AnalyzeTextResult

        return hasattr(AnalyzeTextResult, "user_prompt_analysis") and hasattr(
            AnalyzeTextResult, "documents_analysis"
        )
    except Exception:
        return False


def moderate_input_fields(
    fields: dict[str, Any],
    settings: Settings | None = None,
) -> tuple[dict[str, Any], list[str]]:
    """Moderate a dict of text fields; blank out the blocked ones.

    Convenience for the entry points (CLI and dashboard): run every string
    value through :func:`moderate_text` and replace blocked values with ``\"\"``
    so hostile content never reaches the session. Non-string values (enums,
    budget numbers) pass through untouched.

    Args:
        fields:   The session payload dict.
        settings: App settings.

    Returns:
        ``(cleaned_fields, blocked_field_names)``. When the ML layer is
        disabled this returns the input unchanged with an empty list.
    """
    cleaned = dict(fields)
    blocked_names: list[str] = []
    for name, value in cleaned.items():
        if not isinstance(value, str):
            continue
        verdict = moderate_text(value, settings)
        if verdict.blocked:
            _logger.warning("Content Safety blocked field %r (severity %s)",
                            name, max(verdict.categories.values(), default=0))
            cleaned[name] = ""
            blocked_names.append(str(name))
    return cleaned, blocked_names
