import sys
import logging
from cloudoptima.config import Settings
from cloudoptima.compliance.rag import ComplianceRAG

# Set up logging so we can see what's happening
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("seed")

def main():
    logger.info("Initializing configuration from .env...")
    settings = Settings()
    
    if not settings.azure_search_endpoint:
        logger.error("AZURE_SEARCH_ENDPOINT is missing from .env")
        sys.exit(1)
        
    logger.info(f"Targeting Azure Search: {settings.azure_search_endpoint}")
    logger.info("Initializing RAG engine (this will connect to Azure)...")
    
    rag = ComplianceRAG(settings)
    
    if rag.backend != "azure-search":
        logger.error(f"RAG initialized with backend '{rag.backend}', not 'azure-search'. Check your Azure Search and Azure OpenAI keys in .env.")
        sys.exit(1)
        
    logger.info("Connection successful! Pushing documents to Azure AI Search...")
    docs_pushed = rag.seed_docs()
    
    if docs_pushed > 0:
        logger.info(f"SUCCESS: Pushed {docs_pushed} document chunks to Azure AI Search.")
    else:
        logger.error("FAILED: 0 documents pushed. Check Azure Search index permissions or OpenAI rate limits.")

if __name__ == "__main__":
    main()
