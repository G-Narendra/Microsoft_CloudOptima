"""
Ingest corpus documents into local ChromaDB for Compliance RAG.

Splits markdown files by headings to preserve semantic context and creates
a persistent ChromaDB collection for fast and offline dense retrieval.
"""

import os
import re
from pathlib import Path
import chromadb
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ingest")

def chunk_markdown(content: str, source: str, framework: str) -> list[dict]:
    """Split markdown text by level-1 and level-2 headers."""
    chunks = []
    # Split using regex that matches headers, keeping the header in the chunk
    sections = re.split(r'(?=^#{1,2}\s+)', content, flags=re.MULTILINE)
    
    for i, sec in enumerate(sections):
        text = sec.strip()
        if not text:
            continue
            
        chunks.append({
            "text": text,
            "metadata": {
                "source": source,
                "framework": framework,
                "chunk_id": f"{framework}_{i}"
            }
        })
    return chunks

def map_filename_to_framework(filename: str) -> str:
    """Map raw filenames to the strict framework metadata tags."""
    lower_name = filename.lower()
    if "gdpr" in lower_name: return "gdpr"
    if "hipaa" in lower_name: return "hipaa"
    if "soc 2" in lower_name or "soc2" in lower_name: return "soc2"
    if "iso" in lower_name and "27001" in lower_name: return "iso27001"
    if "pdpl" in lower_name: return "pdpl"
    if "nist" in lower_name: return "nistcsf"
    if "pci" in lower_name: return "pcidss"
    return "unknown"

def main():
    corpus_dir = Path(os.path.join(os.path.dirname(__file__), "..", "corpus"))
    db_dir = Path(os.path.join(os.path.dirname(__file__), "..", "cloudoptima", "db"))
    
    if not corpus_dir.exists():
        logger.error(f"Corpus directory not found: {corpus_dir.absolute()}")
        return
        
    db_dir.mkdir(parents=True, exist_ok=True)
    
    client = chromadb.PersistentClient(path=str(db_dir))
    
    try:
        collection = client.get_or_create_collection(
            name="compliance_corpus",
            metadata={"hnsw:space": "cosine"}
        )
    except Exception as e:
        logger.error(f"Error creating collection: {e}")
        return

    docs = []
    metadatas = []
    ids = []
    
    for file in corpus_dir.glob("*.md"):
        framework = map_filename_to_framework(file.name)
        if framework == "unknown":
            continue
            
        logger.info(f"Processing {file.name} for framework {framework}...")
        content = file.read_text(encoding="utf-8")
        chunks = chunk_markdown(content, file.name, framework)
        
        for c in chunks:
            docs.append(c["text"])
            metadatas.append(c["metadata"])
            ids.append(c["metadata"]["chunk_id"])
            
    if docs:
        batch_size = 500
        for i in range(0, len(docs), batch_size):
            collection.upsert(
                documents=docs[i:i+batch_size],
                metadatas=metadatas[i:i+batch_size],
                ids=ids[i:i+batch_size]
            )
            logger.info(f"Upserted {i + len(docs[i:i+batch_size])}/{len(docs)} chunks.")
            
        logger.info(f"Ingestion complete! Database saved to {db_dir}")
    else:
        logger.warning("No markdown documents found or chunks generated.")

if __name__ == "__main__":
    main()
