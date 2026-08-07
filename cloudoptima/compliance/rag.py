"""Compliance RAG — retrieve guidance for compliance edge cases (Phase 8.2).

The compliance officer judges against the 21 hardcoded rules
(:mod:`cloudoptima.compliance.rules`). For the edge cases those rules don't
spell out — say, PDPL's cross-border transfer consent — this module pulls the
relevant passages from a small built-in corpus and hands them to the prompt so
the LLM can cite chapter and verse.

Backend selection:
- With ``chromadb`` installed: a real vector store (persisted under
  ``persist_dir``) with embedding-based similarity.
- Without it (e.g. Windows boxes where the ``chroma-hnswlib`` wheel needs a
  C++ toolchain): a deterministic keyword-overlap retriever over the same
  corpus. The public API is identical either way.

Security (BUILD_CHECKLIST Phase 8.2): results are treated as untrusted
document data — every passage passes through :func:`clean_output` before it
can reach an LLM prompt or the UI.
"""

from __future__ import annotations

import logging
import re
import threading
from collections.abc import Sequence
from typing import Any, Final

from cloudoptima.sanitize import clean_output

_logger = logging.getLogger(__name__)

try:  # pragma: no cover - exercised only when chromadb is installed
    import chromadb

    CHROMADB_AVAILABLE = True
except Exception:  # pragma: no cover - exercised only when chromadb is missing
    chromadb = None
    CHROMADB_AVAILABLE = False

# ── Built-in compliance corpus ───────────────────────────────────────────
# (id, framework, passage). Framework is one of pdpl/hipaa/soc2/iso27001/gdpr.
# These are the edge cases the 21 generic rules do not fully express.
BUILTIN_DOCS: Final[tuple[tuple[str, str, str], ...]] = (
    (
        "pdpl-1",
        "pdpl",
        "PDPL data residency: personal data of Saudi residents must be stored "
        "and processed within the Kingdom of Saudi Arabia; cross-border "
        "transfer requires explicit consent and documented legal basis.",
    ),
    (
        "pdpl-2",
        "pdpl",
        "PDPL breach notification: controllers must notify the authority of a "
        "personal-data breach without undue delay and no later than 72 hours "
        "after becoming aware, where feasible.",
    ),
    (
        "pdpl-3",
        "pdpl",
        "PDPL consent: processing of personal data requires freely given, "
        "specific, informed, and unambiguous consent that can be withdrawn at "
        "any time as easily as it was given.",
    ),
    (
        "hipaa-1",
        "hipaa",
        "HIPAA BAA: a Business Associate Agreement is mandatory with every "
        "cloud provider, subcontractor, or vendor that touches protected "
        "health information (PHI).",
    ),
    (
        "hipaa-2",
        "hipaa",
        "HIPAA audit controls: hardware, software, and procedural mechanisms "
        "must record and examine access and other activity in information "
        "systems that contain or use ePHI.",
    ),
    (
        "hipaa-3",
        "hipaa",
        "HIPAA integrity controls: ePHI must not be improperly altered or "
        "destroyed; integrity policies and procedures are required, including "
        "backup and disaster recovery.",
    ),
    (
        "soc2-1",
        "soc2",
        "SOC 2 CC6: logical and physical access controls must restrict access "
        "to system resources to authorized personnel, with least privilege and "
        "periodic access reviews.",
    ),
    (
        "soc2-2",
        "soc2",
        "SOC 2 CC7: the system must be monitored to identify deviations from "
        "expected operation, including intrusion detection, log review, and "
        "incident response procedures.",
    ),
    (
        "soc2-3",
        "soc2",
        "SOC 2 A1: availability commitments require redundant infrastructure, "
        "capacity planning, and documented recovery objectives (RTO/RPO).",
    ),
    (
        "iso-1",
        "iso27001",
        "ISO 27001 A.8: asset management requires an inventory of information "
        "assets and owners, with classification by confidentiality, integrity, "
        "and availability.",
    ),
    (
        "iso-2",
        "iso27001",
        "ISO 27001 A.12: operational security covers change management, "
        "capacity management, malware protection, and secure logging.",
    ),
    (
        "iso-3",
        "iso27001",
        "ISO 27001 A.18: compliance requires identification of applicable "
        "legislation, regular compliance reviews, and independent audit of the "
        "information security management system.",
    ),
    (
        "gdpr-1",
        "gdpr",
        "GDPR Article 25: data protection by design and by default — technical "
        "and organizational measures must implement data-protection principles "
        "from the design stage.",
    ),
    (
        "gdpr-2",
        "gdpr",
        "GDPR Article 32: security of processing requires encryption, "
        "confidentiality/integrity/availability measures, regular testing, and "
        "pseudonymization where appropriate.",
    ),
    (
        "gdpr-3",
        "gdpr",
        "GDPR data transfer: transfers outside the EEA require adequacy "
        "decisions, SCCs, or binding corporate rules; Standard Contractual "
        "Clauses are the common fallback.",
    ),
)

_WORD_RE: Final[re.Pattern[str]] = re.compile(r"[a-z0-9]+")


def _tokenize(text: str) -> set[str]:
    """Lowercase word set of a passage or query (fallback retriever)."""
    return set(_WORD_RE.findall(text.lower()))


class _KeywordRetriever:
    """Deterministic offline retriever — overlap of query words with passages."""

    def __init__(self, docs: Sequence[tuple[str, str, str]]) -> None:
        self._docs: list[tuple[str, str, str]] = list(docs)
        self._tokens: list[set[str]] = [_tokenize(text) for _, _, text in docs]

    def query(
        self, query: str, framework: str = "", top_k: int = 3
    ) -> list[tuple[str, str]]:
        """Return ``(doc_id, text)`` passages ranked by word overlap."""
        q_tokens = _tokenize(query)
        if not q_tokens:
            return []
        scored: list[tuple[float, str, str]] = []
        for (doc_id, doc_framework, text), tokens in zip(self._docs, self._tokens, strict=True):
            if framework and doc_framework != framework:
                continue
            overlap = len(q_tokens & tokens)
            if overlap > 0:
                scored.append((overlap, doc_id, text))
        scored.sort(key=lambda item: (-item[0], item[1]))
        return [(doc_id, text) for _, doc_id, text in scored[:top_k]]


class ComplianceRAG:
    """Compliance passage retriever with a ChromaDB backend and fallback.

    Args:
        persist_dir: Directory for the Chroma persistent store (ignored by the
            offline fallback).

    Attributes:
        backend: ``"chroma"`` when the vector store is active, ``"keyword"``
            for the offline fallback — useful for diagnostics.
    """

    COLLECTION_NAME: Final[str] = "compliance_docs"

    def __init__(self, persist_dir: str = "data/compliance_rag") -> None:
        self.backend: str = "keyword"
        self._lock = threading.Lock()
        self._keyword = _KeywordRetriever(BUILTIN_DOCS)
        self._collection: Any = None
        self._chroma: Any = None
        if CHROMADB_AVAILABLE:
            try:  # pragma: no cover - depends on the installed backend
                self._chroma = chromadb.PersistentClient(path=persist_dir)
                self._collection = self._chroma.get_or_create_collection(
                    name=self.COLLECTION_NAME, metadata={"hnsw:space": "cosine"}
                )
                self.backend = "chroma"
                # Seed the built-in corpus so queries work immediately (the
                # keyword fallback preloads it in __init__; Chroma must be
                # populated explicitly or every query would return nothing).
                self._seed_chroma([])
            except Exception:
                # If Chroma cannot start (missing deps, corrupt store), fall
                # back silently — retrieval must never crash the pipeline.
                self._chroma = None
                self._collection = None

    @property
    def available(self) -> bool:
        """True when a usable retrieval backend is present."""
        return self.backend == "chroma" or self._keyword is not None

    def seed_docs(self, docs: Sequence[tuple[str, str, str]] | None = None) -> int:
        """Index the built-in corpus (plus any extra docs) for retrieval.

        Args:
            docs: Optional extra ``(doc_id, framework, text)`` tuples to index
                alongside the built-in corpus.

        Returns:
            The number of documents indexed in this call.

        Texts are cleaned with :func:`clean_output` before indexing, so hostile
        document content can't smuggle HTML or control characters into the store.
        """
        extra = list(docs or [])
        if self.backend == "chroma":
            return self._seed_chroma(extra)  # pragma: no cover - backend-gated
        return self._seed_keyword(extra)

    def _seed_keyword(self, extra: Sequence[tuple[str, str, str]]) -> int:
        docs = [doc for doc in extra if self._clean_doc(doc) is not None]
        if docs:
            self._keyword = _KeywordRetriever(list(BUILTIN_DOCS) + docs)
        return len(docs)

    def _seed_chroma(self, extra: Sequence[tuple[str, str, str]]) -> int:
        if self._collection is None:
            return 0  # pragma: no cover - defensive
        docs = [doc for doc in BUILTIN_DOCS + tuple(extra) if self._clean_doc(doc) is not None]
        ids = [doc[0] for doc in docs]
        docs_meta = [{"framework": doc[1]} for doc in docs]
        self._collection.upsert(
            ids=ids, documents=[doc[2] for doc in docs], metadatas=docs_meta
        )
        return len(ids)

    @staticmethod
    def _clean_doc(doc: tuple[str, str, str]) -> tuple[str, str, str] | None:
        doc_id, framework, text = doc
        cleaned = clean_output(text)
        if not cleaned:
            return None
        return doc_id, framework, cleaned

    def query_rag(self, query: str, framework: str = "", top_k: int = 3) -> list[str]:
        """Return the ``top_k`` passages most relevant to ``query``.

        Args:
            query: The compliance question (e.g. "cross-border data transfer").
            framework: Optional filter — ``pdpl``, ``hipaa``, ``soc2``,
                ``iso27001``, or ``gdpr``.
            top_k: Maximum number of passages to return.

        Returns:
            Cleaned passage texts (never raw documents); empty when nothing
            matches. Every result is treated as untrusted and passed through
            :func:`clean_output`.

        Raises:
            ValueError: If ``top_k`` is not positive.
        """
        if top_k < 1:
            raise ValueError(f"top_k must be positive, got {top_k}")
        query = clean_output(query)
        if not query:
            return []
        with self._lock:
            if self.backend == "chroma":
                return self._query_chroma(query, framework, top_k)  # pragma: no cover
            return self._query_keyword(query, framework, top_k)

    def _query_keyword(
        self, query: str, framework: str, top_k: int
    ) -> list[str]:
        return [clean_output(text) for _, text in self._keyword.query(query, framework, top_k)]

    def _query_chroma(
        self, query: str, framework: str, top_k: int
    ) -> list[str]:  # pragma: no cover - backend-gated
        """Query the Chroma store; on any backend error, degrade to empty.

        Chroma is optional infrastructure — a hiccup there must never break
        the compliance agent (it would otherwise become an error turn and
        silently disable compliance in the whole pipeline).
        """
        if self._collection is None:
            return []
        try:
            where: dict[str, Any] | None = {"framework": framework} if framework else None
            result = self._collection.query(
                query_texts=[query], n_results=top_k, where=where
            )
            documents = result.get("documents") or []
            if not documents:
                return []
            return [clean_output(text) for text in documents[0]]
        except Exception:  # pragma: no cover - backend-gated
            _logger.warning(
                "Compliance RAG: Chroma query failed — degrading to empty", exc_info=True
            )
            return []


# ── Module-level singleton + convenience functions ───────────────────────
_rag: ComplianceRAG | None = None
_rag_lock = threading.Lock()


def get_rag() -> ComplianceRAG:
    """Return the process-wide :class:`ComplianceRAG` singleton."""
    global _rag
    if _rag is None:
        with _rag_lock:
            if _rag is None:
                _rag = ComplianceRAG()
    return _rag


def seed_docs(docs: Sequence[tuple[str, str, str]] | None = None) -> int:
    """Convenience wrapper — index the built-in corpus (plus extras).

    See :meth:`ComplianceRAG.seed_docs`.
    """
    return get_rag().seed_docs(docs)


def query_rag(query: str, framework: str = "", top_k: int = 3) -> list[str]:
    """Convenience wrapper — retrieve relevant compliance passages.

    See :meth:`ComplianceRAG.query_rag`.
    """
    return get_rag().query_rag(query, framework, top_k)
