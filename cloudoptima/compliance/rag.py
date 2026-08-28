"""Compliance RAG — retrieve guidance for compliance edge cases (Phase 8.2).

Backend selection:
- With ``azure-search-documents`` installed: a real vector store with Hybrid Search 
  and semantic re-ranking.
- Without it: a deterministic keyword-overlap retriever over the same corpus.
"""

from __future__ import annotations

import base64
import logging
import os
import re
import threading
from collections.abc import Sequence
from typing import Any, Final, TYPE_CHECKING

from cloudoptima.sanitize import clean_output, detect_injection

if TYPE_CHECKING:
    from cloudoptima.config import Settings

_logger = logging.getLogger(__name__)

try:
    from azure.core.credentials import AzureKeyCredential
    from azure.search.documents import SearchClient
    from azure.search.documents.models import VectorizedQuery
    import openai
    AZURE_SEARCH_AVAILABLE = True
except ImportError:
    AZURE_SEARCH_AVAILABLE = False
    VectorizedQuery = None  # type: ignore

try:
    import chromadb
    from chromadb.config import Settings as ChromaSettings
    CHROMA_AVAILABLE = True
except ImportError:
    CHROMA_AVAILABLE = False


# Built-in compliance corpus
# Each entry: (doc_id, framework, guidance_text)
# This corpus is always available — no vector DB or external search required.
# The compliance agent RAG will use these as the default retrieval source.
BUILTIN_DOCS: Final[tuple[tuple[str, str, str], ...]] = (
    (
        "pdpl-art29-data-residency",
        "pdpl",
        "PDPL Article 29 — Data Residency: Personal data of Saudi nationals must be stored "
        "within KSA-approved geography. Azure UAE North and KSA Central are approved regions. "
        "Cross-border transfer requires controller notification to NCA and data subject consent. "
        "Use Azure Policy to enforce allowed regions. Enable geo-redundancy only within approved zones.",
    ),
    (
        "gdpr-art32-encryption-rest",
        "gdpr",
        "GDPR Article 32 — Encryption at Rest: All storage containing personal data must be "
        "encrypted with AES-256. On Azure: enable Azure Storage Service Encryption (SSE) by default, "
        "use Azure Disk Encryption for VMs, Azure SQL Transparent Data Encryption (TDE). "
        "Manage keys in Azure Key Vault with HSM-backed keys for sensitive data.",
    ),
    (
        "pci-dss-req4-encryption-transit",
        "pci-dss",
        "PCI-DSS Requirement 4 — Encryption in Transit: TLS 1.2 or higher is required for all "
        "cardholder data transmitted across open or public networks. Disable TLS 1.0 and 1.1 on "
        "all Azure App Services, API Gateways, and Load Balancers. Use Azure Front Door WAF with "
        "HTTPS redirect. Enforce HSTS headers. Certificate rotation must be automated.",
    ),
    (
        "soc2-cc61-access-control",
        "soc2",
        "SOC 2 CC6.1 — Logical Access Control: Restrict logical access using RBAC with least-privilege. "
        "On Azure: use Azure Active Directory with Conditional Access Policies, Privileged Identity "
        "Management (PIM) for just-in-time access, and Azure RBAC built-in roles. No shared accounts. "
        "All privileged access must use MFA and be time-limited via PIM.",
    ),
    (
        "hipaa-164312b-audit-logging",
        "hipaa",
        "HIPAA 164.312(b) — Audit Logging: Implement hardware, software, and procedural mechanisms "
        "to record and examine access to ePHI. On Azure: enable Azure Monitor and Diagnostic Logs for "
        "all resources, stream to Log Analytics Workspace, retain for 90 days minimum. "
        "Use Microsoft Defender for Cloud for threat detection. Enable immutable audit log storage.",
    ),
    (
        "gdpr-art5-data-retention",
        "gdpr",
        "GDPR Article 5(1)(e) — Data Retention (Storage Limitation): Personal data must not be "
        "kept longer than necessary for the specified purpose. Define data retention policies per "
        "data category. On Azure: use Azure Blob Lifecycle Management policies, Azure SQL retention "
        "policies, and Azure Purview for data governance. Document retention periods in a data map.",
    ),
    (
        "gdpr-art17-right-deletion",
        "gdpr",
        "GDPR Article 17 — Right to Erasure (Right to be Forgotten): Data subjects can request "
        "deletion of their personal data. Architecture must support deletion propagation across all "
        "systems including backups, caches, and audit logs. Implement soft-delete with scheduler, "
        "use Azure Cosmos DB's TTL feature, and document the deletion workflow.",
    ),
    (
        "gdpr-art33-breach-notification",
        "gdpr",
        "GDPR Article 33 — Breach Notification: Notify the supervisory authority within 72 hours "
        "of becoming aware of a personal data breach. Use Microsoft Defender for Cloud alerts for "
        "real-time breach detection. Maintain an incident response runbook. Document notification "
        "contacts, escalation paths, and communication templates.",
    ),
    (
        "soc2-cc73-incident-response",
        "soc2",
        "SOC 2 CC7.3 — Incident Response: Maintain a documented incident response plan covering "
        "detection, evaluation, response, and mitigation. Integrate with Azure Security Center "
        "and Microsoft Sentinel for SIEM. Define RTO/RPO targets. Run tabletop exercises quarterly. "
        "Incidents must be classified by severity (P1-P4) with defined SLA response times.",
    ),
    (
        "iso27001-a151-vendor-assessment",
        "iso27001",
        "ISO 27001 A.15.1.1 — Vendor Assessment: Information security policies for supplier "
        "relationships must be agreed and documented. Conduct vendor risk assessments before onboarding. "
        "Include security clauses in contracts. For Azure services: review Microsoft's compliance "
        "documentation, SLAs, and shared responsibility matrix. Maintain a vendor register.",
    ),
    (
        "iso27001-a821-data-classification",
        "iso27001",
        "ISO 27001 A.8.2.1 — Data Classification: Classify information based on legal requirements, "
        "value, criticality, and sensitivity (e.g. Public, Internal, Confidential, Restricted). "
        "Apply classification labels using Microsoft Purview Information Protection. "
        "Enforce DLP policies in Azure to prevent unauthorized data movement.",
    ),
    (
        "soc2-a12-backup-recovery",
        "soc2",
        "SOC 2 A1.2 — Backup and Recovery: Maintain regular backups with tested disaster recovery "
        "procedures. Define and meet RTO and RPO objectives. On Azure: use Azure Backup for VMs, "
        "Azure SQL geo-redundant backups, Azure Site Recovery for DR. Test restore procedures "
        "quarterly and document results. Store backups in a separate region.",
    ),
    (
        "iso27001-a1712-business-continuity",
        "iso27001",
        "ISO 27001 A.17.1.2 — Business Continuity: Implement and test Business Continuity Procedures. "
        "Perform BIA (Business Impact Analysis) to identify critical systems. Deploy Azure "
        "Availability Zones for multi-zone redundancy, Azure Traffic Manager for failover. "
        "Conduct annual BCP tests and document results with lessons learned.",
    ),
    (
        "pci-dss-req1-network-security",
        "pci-dss",
        "PCI-DSS Requirement 1 — Network Security: Install and maintain firewall configuration "
        "to protect cardholder data. On Azure: use Azure Firewall Premium for stateful inspection, "
        "NSGs for micro-segmentation, Azure DDoS Protection Standard, and Azure Web Application "
        "Firewall (WAF). Segregate cardholder data environment (CDE) from other networks.",
    ),
    (
        "pci-dss-req62-patch-management",
        "pci-dss",
        "PCI-DSS Requirement 6.2 — Patch Management: Install critical security patches within "
        "one month of release. Use Azure Update Manager for OS and software patching across VMs. "
        "Enable automatic patching for Azure SQL, App Services, and AKS. "
        "Maintain a patch compliance dashboard and remediate critical CVEs within 30 days.",
    ),
    (
        "nist-csf-prac1-identity-management",
        "nist-csf",
        "NIST CSF PR.AC-1 — Identity and Access Management: MFA and managed identities must be "
        "enforced for all privileged access. On Azure: use Azure AD MFA with Conditional Access, "
        "Azure Managed Identities for service-to-service auth (no secrets in code), "
        "Privileged Identity Management (PIM) for just-in-time admin access.",
    ),
    (
        "nist-csf-prds1-key-management",
        "nist-csf",
        "NIST CSF PR.DS-1 — Data Security / Key Management: Cryptographic keys must be managed "
        "securely. Use Azure Key Vault for secrets, keys, and certificates. For HSM-backed keys "
        "use Azure Dedicated HSM or Managed HSM. Rotate keys annually or on compromise. "
        "Never store keys in application code, config files, or environment variables.",
    ),
    (
        "iso27001-a1421-secure-development",
        "iso27001",
        "ISO 27001 A.14.2.1 — Secure Development: Follow a Secure SDLC with security reviews "
        "at each phase. Use Azure DevOps with GitHub Advanced Security for SAST/DAST scanning, "
        "secret scanning, and dependency vulnerability checks. Conduct threat modeling before "
        "architecture is finalized. Require security sign-off before production deployment.",
    ),
    (
        "pci-dss-req112-vulnerability-scanning",
        "pci-dss",
        "PCI-DSS Requirement 11.2 — Vulnerability Scanning: Perform internal and external "
        "vulnerability scans at least quarterly and after any significant change. Use Microsoft "
        "Defender Vulnerability Management for continuous scanning. Integrate with Azure Security "
        "Center. Remediate high/critical findings before next scan. Use an ASV for external scans.",
    ),
    (
        "hipaa-164308a5-staff-training",
        "hipaa",
        "HIPAA 164.308(a)(5) — Security Awareness and Training: Implement a security awareness "
        "training program for all workforce members. Training must cover phishing, social engineering, "
        "data handling, and incident reporting. Track completion and maintain training records. "
        "Annual refresher training is required; role-specific training for privileged users.",
    ),
    (
        "gdpr-art28-third-party",
        "gdpr",
        "GDPR Article 28 — Third-party Data Processing: Processing by a data processor must be "
        "governed by a binding contract (Data Processing Agreement / DPA). DPA must specify "
        "processing instructions, data categories, technical safeguards, and sub-processor rules. "
        "Review and update DPAs when processor changes their sub-processors.",
    ),
)


try:
    from rank_bm25 import BM25Okapi
    from sentence_transformers import CrossEncoder
    import numpy as np
    RANK_AVAILABLE = True
except ImportError:
    RANK_AVAILABLE = False

_WORD_RE: Final[re.Pattern[str]] = re.compile(r"[a-z0-9]+")

def _tokenize(text: str) -> list[str]:
    return _WORD_RE.findall(text.lower())

class _KeywordRetriever:
    """Offline retriever using BM25 for sparse keyword search."""

    def __init__(self, docs: Sequence[tuple[str, str, str]]) -> None:
        self._docs: list[tuple[str, str, str]] = list(docs)
        if not self._docs:
            self._bm25 = None
            return
            
        tokenized_corpus = [_tokenize(text) for _, _, text in self._docs]
        if RANK_AVAILABLE:
            self._bm25 = BM25Okapi(tokenized_corpus)
        else:
            self._bm25 = None

    def query(
        self, query: str, framework: list[str] | str = "", top_k: int = 3
    ) -> list[tuple[str, str]]:
        if not self._bm25 or not query:
            return []
            
        tokenized_query = _tokenize(query)
        doc_scores = self._bm25.get_scores(tokenized_query)
        
        # Normalize framework to list
        if isinstance(framework, str):
            frameworks = [framework] if framework else []
        else:
            frameworks = framework

        # Filter by framework and score > 0
        scored = []
        for i, (doc_id, doc_framework, text) in enumerate(self._docs):
            if frameworks and doc_framework not in frameworks:
                continue
            if doc_scores[i] > 0:
                scored.append((doc_scores[i], doc_id, text))
                
        scored.sort(key=lambda item: (-item[0], item[1]))
        return [(doc_id, text) for _, doc_id, text in scored[:top_k]]


class _ChromaRetriever:
    """Local vector retriever using persistent ChromaDB."""

    def __init__(self, docs: Sequence[tuple[str, str, str]] = None) -> None:
        # Connect to persistent local database
        db_path = "cloudoptima/db"
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(
            name="compliance_corpus",
            metadata={"hnsw:space": "cosine"}
        )
        if docs:
            self.seed(docs)
            
    def get_all_docs(self) -> list[tuple[str, str, str]]:
        """Fetch all documents from Chroma for BM25 initialization."""
        try:
            results = self.collection.get()
            docs = []
            for i in range(len(results["ids"])):
                doc_id = results["ids"][i]
                text = results["documents"][i]
                framework = results["metadatas"][i].get("framework", "") if results["metadatas"] else ""
                docs.append((doc_id, framework, text))
            return docs
        except Exception:
            return []
        
    def seed(self, docs: Sequence[tuple[str, str, str]]) -> int:
        if not docs:
            return 0
        ids = [doc[0] for doc in docs]
        metadatas = [{"framework": doc[1]} for doc in docs]
        documents = [doc[2] for doc in docs]
        
        # Batch insert
        batch_size = 500
        for i in range(0, len(docs), batch_size):
            self.collection.upsert(
                documents=documents[i:i+batch_size],
                metadatas=metadatas[i:i+batch_size],
                ids=ids[i:i+batch_size]
            )
        return len(docs)
        
    def query(
        self, query: str, framework: list[str] | str = "", top_k: int = 3
    ) -> list[tuple[str, str]]:
        if not query:
            return []
        
        where = None
        if isinstance(framework, str) and framework:
            where = {"framework": framework}
        elif isinstance(framework, list) and framework:
            if len(framework) == 1:
                where = {"framework": framework[0]}
            else:
                where = {"framework": {"$in": framework}}
        
        results = self.collection.query(
            query_texts=[query],
            n_results=top_k,
            where=where
        )
        
        if not results or not results["ids"] or not results["ids"][0]:
            return []
            
        ret = []
        for i in range(len(results["ids"][0])):
            doc_id = results["ids"][0][i]
            text = results["documents"][0][i]
            ret.append((doc_id, text))
        return ret


class ComplianceRAG:
    """Compliance passage retriever with an Azure AI Search backend and fallback.

    Args:
        settings: Application Settings containing Azure endpoints and keys.
    """

    def __init__(self, settings: Settings) -> None:
        self.backend: str = "keyword"
        self._lock = threading.Lock()
        self._keyword = _KeywordRetriever(BUILTIN_DOCS)
        self._chroma: Any = None
        self._search_client: Any = None
        self._oai_client: Any = None
        self._embedding_deployment: str = settings.azure_openai_embedding_deployment

        # Only attempt to initialize if the credentials exist and SDK is available
        if AZURE_SEARCH_AVAILABLE and settings.azure_search_endpoint and settings.azure_search_api_key.get_secret_value():
            try:
                self._search_client = SearchClient(
                    endpoint=settings.azure_search_endpoint,
                    index_name=settings.azure_search_index_name,
                    credential=AzureKeyCredential(settings.azure_search_api_key.get_secret_value()),
                )
                if settings.azure_openai_api_key.get_secret_value() and settings.azure_openai_endpoint:
                    self._oai_client = openai.AzureOpenAI(
                        api_key=settings.azure_openai_api_key.get_secret_value(),
                        api_version="2023-05-15",
                        azure_endpoint=settings.azure_openai_endpoint
                    )
                self.backend = "azure-search"
                # Note: Index creation/population is typically handled externally for Azure AI Search,
                # but we will support local seeding using seed_docs() just like we did with Chroma.
            except Exception:
                _logger.warning("Compliance RAG: Azure AI Search init failed — degrading to offline keyword retriever", exc_info=True)
                self._search_client = None
                
        if self.backend == "keyword" and CHROMA_AVAILABLE:
            try:
                self._chroma = _ChromaRetriever()
                db_docs = self._chroma.get_all_docs()
                if db_docs:
                    # Use the docs already stored in Chroma for BM25 as well
                    self._keyword = _KeywordRetriever(db_docs)
                else:
                    # DB is empty (e.g. vector DB was deleted) — seed it with
                    # the built-in regulatory corpus so the agent is not blind.
                    _logger.info(
                        "Compliance RAG: ChromaDB is empty — seeding with %d built-in docs",
                        len(BUILTIN_DOCS),
                    )
                    self._chroma.seed(BUILTIN_DOCS)
                    # Keep the BUILTIN_DOCS keyword retriever already set in __init__

                self.backend = "hybrid"
                if RANK_AVAILABLE:
                    self._cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
            except Exception:
                _logger.warning(
                    "Compliance RAG: Chroma init failed — using built-in keyword retriever",
                    exc_info=True,
                )


    @property
    def available(self) -> bool:
        """True when a usable retrieval backend is present."""
        return self.backend in ("azure-search", "hybrid") or self._keyword is not None

    def seed_docs(self, docs: Sequence[tuple[str, str, str]] | None = None) -> int:
        extra = list(docs) if docs is not None else []
        chunked_extra = self._semantic_chunk(extra) if extra else []
        if self.backend == "azure-search":
            return self._seed_azure(chunked_extra)
        if self.backend == "hybrid":
            c = self._chroma.seed(chunked_extra)
            self._seed_keyword(chunked_extra)
            return c
        return self._seed_keyword(chunked_extra)

    def _semantic_chunk(
        self, docs: Sequence[tuple[str, str, str]], max_len: int = 800
    ) -> list[tuple[str, str, str]]:
        """Semantic chunking (Phase 9 P1) by paragraph boundaries."""
        chunked = []
        for doc_id, framework, text in docs:
            paragraphs = text.split("\n\n")
            current_chunk = ""
            chunk_idx = 0
            
            for p in paragraphs:
                p = p.strip()
                if not p:
                    continue
                if len(current_chunk) + len(p) < max_len:
                    current_chunk += p + "\n\n"
                else:
                    if current_chunk:
                        chunked.append((f"{doc_id}-{chunk_idx}", framework, current_chunk.strip()))
                        chunk_idx += 1
                    current_chunk = p + "\n\n"
            if current_chunk:
                chunked.append((f"{doc_id}-{chunk_idx}", framework, current_chunk.strip()))
        return chunked

    def _seed_keyword(self, extra: Sequence[tuple[str, str, str]]) -> int:
        docs = [doc for doc in extra if self._clean_doc(doc) is not None]
        if docs:
            self._keyword = _KeywordRetriever(list(BUILTIN_DOCS) + docs)
        return len(docs)

    def _seed_azure(self, extra: Sequence[tuple[str, str, str]]) -> int:
        if self._search_client is None or self._oai_client is None:
            return 0
        docs = [doc for doc in extra if self._clean_doc(doc) is not None]
        
        azure_docs = []
        for doc in docs:
            # Generate embedding
            response = self._oai_client.embeddings.create(
                input=doc[2],
                model=self._embedding_deployment
            )
            embedding = response.data[0].embedding
            safe_id = base64.urlsafe_b64encode(doc[0].encode("utf-8")).decode("utf-8")
            azure_docs.append({
                "id": safe_id,
                "framework": doc[1],
                "text": doc[2],
                "text_vector": embedding
            })
        
        try:
            batch_size = 100
            for i in range(0, len(azure_docs), batch_size):
                self._search_client.upload_documents(documents=azure_docs[i:i + batch_size])
            return len(azure_docs)
        except Exception:
            _logger.exception("Compliance RAG: Failed to seed Azure Search docs")
            return 0

    @staticmethod
    def _clean_doc(doc: tuple[str, str, str]) -> tuple[str, str, str] | None:
        doc_id, framework, text = doc
        cleaned = clean_output(text)
        if not cleaned:
            return None
        if detect_injection(cleaned):
            _logger.warning("Compliance RAG: dropping doc %r — injection pattern detected", doc_id)
            return None
        return doc_id, framework, cleaned

    def rewrite_query(self, raw_prompt: str, oai_client: Any) -> str:
        """Rewrite raw architecture prompt into compliance keywords using LLM."""
        if not raw_prompt or not oai_client:
            return raw_prompt
            
        system_prompt = (
            "You are a compliance RAG query generator. Extract 3-5 core compliance or "
            "security concepts from the user's architecture description to form a focused "
            "search query (e.g., 'data residency encryption at rest RBAC audit logging'). "
            "Output ONLY the query string, nothing else."
        )
        try:
            response = oai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": raw_prompt}
                ],
                temperature=0.0,
                max_tokens=30,
            )
            return response.choices[0].message.content.strip()
        except Exception:
            _logger.warning("Compliance RAG: Query rewrite failed, using raw prompt")
            return raw_prompt

    def query_rag(self, query: str, framework: list[str] | str = "", top_k: int = 3) -> list[str]:
        if top_k < 1:
            raise ValueError(f"top_k must be positive, got {top_k}")
        query = clean_output(query)
        if not query:
            return []
        with self._lock:
            if self.backend == "azure-search":
                return self._query_azure(query, framework, top_k)
            if self.backend == "hybrid":
                return self._query_hybrid(query, framework, top_k)
            return self._query_keyword(query, framework, top_k)

    def _query_hybrid(self, query: str, framework: list[str] | str, top_k: int) -> list[str]:
        # Fetch top K from both keyword and dense search
        kw_results = self._keyword.query(query, framework, top_k=top_k*2)
        vc_results = self._chroma.query(query, framework, top_k=top_k*2)
        
        combined_docs = {}
        for doc_id, text in kw_results + vc_results:
            if doc_id not in combined_docs:
                combined_docs[doc_id] = text
                
        if not combined_docs:
            return []
            
        doc_ids = list(combined_docs.keys())
        texts = list(combined_docs.values())
        
        if RANK_AVAILABLE and hasattr(self, "_cross_encoder"):
            # Cross-Encoder re-ranking
            pairs = [[query, txt] for txt in texts]
            scores = self._cross_encoder.predict(pairs)
            
            # Sort descending
            ranked_indices = np.argsort(scores)[::-1]
            ranked_texts = [texts[i] for i in ranked_indices]
        else:
            ranked_texts = texts
        
        results = [clean_output(text) for text in ranked_texts[:top_k]]
        return [text for text in results if not detect_injection(text)]

    def _query_keyword(self, query: str, framework: list[str] | str, top_k: int) -> list[str]:
        results = [clean_output(text) for _, text in self._keyword.query(query, framework, top_k)]
        return [text for text in results if not detect_injection(text)]

    def _query_azure(self, query: str, framework: list[str] | str, top_k: int) -> list[str]:
        if self._search_client is None:
            return []
        try:
            # Generate query embedding
            vector_query = None
            if self._oai_client:
                response = self._oai_client.embeddings.create(
                    input=query,
                    model=self._embedding_deployment
                )
                query_vector = response.data[0].embedding
                vector_query = VectorizedQuery(vector=query_vector, k_nearest_neighbors=top_k, fields="text_vector")

            filter_str = None
            if isinstance(framework, str) and framework:
                filter_str = f"framework eq '{framework}'"
            elif isinstance(framework, list) and framework:
                fw_list = ",".join([f"'{f}'" for f in framework])
                filter_str = f"search.in(framework, '{fw_list}', ',')"
            
            # Hybrid search with Semantic Ranking
            results = list(self._search_client.search(
                search_text=query,
                vector_queries=[vector_query] if vector_query else None,
                filter=filter_str,
                top=top_k,
                query_type="semantic",
                semantic_configuration_name="default",
            ))
            
            # Auto-seed if index is empty but we haven't filtered too aggressively
            if not results and not filter_str:
                _logger.info("Compliance RAG: Azure AI Search returned 0 results. Attempting to seed index...")
                seeded = self.seed_docs()
                if seeded > 0:
                    results = list(self._search_client.search(
                        search_text=query,
                        vector_queries=[vector_query] if vector_query else None,
                        filter=filter_str,
                        top=top_k,
                        query_type="semantic",
                        semantic_configuration_name="default",
                    ))
            
            documents = []
            for result in results:
                documents.append(result["text"])
                
            cleaned = [clean_output(text) for text in documents]
            return [text for text in cleaned if not detect_injection(text)]
        except Exception:
            _logger.warning("Compliance RAG: Azure Search query failed — degrading to empty", exc_info=True)
            return []
