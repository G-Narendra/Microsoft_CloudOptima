# CloudOptima Regulatory Corpus

This directory is the staging area for raw regulatory documents (PDFs, Markdown, or Text) before they are ingested into the Azure AI Search vector database for the Compliance RAG Agent.

To build the corpus, download the official documents from the links below and place them in this folder. The ingestion script will parse, chunk, and vectorize them.

## Official Regulatory Documents & Download Links

| Framework / Regulation | Description | Official Source / Download Link |
|------------------------|-------------|---------------------------------|
| **GDPR** (General Data Protection Regulation) | EU privacy and security law. Critical for data residency and privacy controls. | [GDPR Official Text (EUR-Lex)](https://eur-lex.europa.eu/eli/reg/2016/679/oj) (Available in HTML/PDF) |
| **HIPAA** (Health Insurance Portability and Accountability Act) | US healthcare data protection standards (Security & Privacy Rules). | [HIPAA Combined Text (HHS.gov PDF)](https://www.hhs.gov/sites/default/files/ocr/privacy/hipaa/administrative/combined/hipaa-simplification-201303.pdf) |
| **SOC 2** (Service Organization Control 2) | AICPA Trust Services Criteria (Security, Availability, Processing Integrity, Confidentiality, Privacy). | *Proprietary standard.* Overviews available at [AICPA TSC](https://us.aicpa.org/content/dam/aicpa/interestareas/frc/assuranceadvisoryservices/downloadabledocuments/trust-services-criteria.pdf). (Requires licensed access for full audit criteria). |
| **ISO/IEC 27001:2022** | International standard for Information Security Management Systems (ISMS). | *Proprietary standard.* Purchased via [ISO Store](https://deingenieriaindustrial.com/en/integrated-management-system/iso-27001-2022-in-pdf-free-download/). (Guidance available via public frameworks). |
| **PDPL** (Personal Data Protection Law - KSA) | Saudi Arabia's data privacy legislation, critical for Middle East deployments. | [PDPL Official Text (SDAIA)](https://www.dlapiperdataprotection.com/?c=SA) |
| **NIST.CSWP.29** (Cybersecurity Framework) | US Federal framework for managing cybersecurity risk. | [NIST CSF 2.0 (NIST.gov)](https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf) |
| **PCI-DSS v4_0_1** (Payment Card Industry Data Security Standard) | Standard for systems handling credit card data. | [PCI-DSS Document Library](https://www.pcisecuritystandards.org/document_library/) (Search for PCI DSS v4.0) |

