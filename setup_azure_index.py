import os
import sys
import logging
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SimpleField,
    SearchableField,
    SearchField,
    SearchFieldDataType,
    VectorSearch,
    HnswAlgorithmConfiguration,
    VectorSearchProfile,
)
from cloudoptima.config import Settings

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("azure_index")

def create_index():
    settings = Settings()
    
    if not settings.azure_search_endpoint or not settings.azure_search_api_key.get_secret_value():
        logger.error("Azure Search credentials missing in .env")
        sys.exit(1)

    index_name = settings.azure_search_index_name
    credential = AzureKeyCredential(settings.azure_search_api_key.get_secret_value())
    client = SearchIndexClient(endpoint=settings.azure_search_endpoint, credential=credential)

    logger.info(f"Checking if index '{index_name}' exists...")
    try:
        client.get_index(index_name)
        logger.warning(f"Index '{index_name}' already exists! Deleting it to fix the schema...")
        client.delete_index(index_name)
        logger.info("Deleted old index.")
    except Exception as e:
        logger.info("Index does not exist yet or could not be fetched.")

    # Define the fields. 
    # CRITICAL: text_vector MUST be Collection(Edm.Single), not a string!
    fields = [
        SimpleField(name="id", type=SearchFieldDataType.String, key=True),
        SearchableField(name="framework", type=SearchFieldDataType.String, filterable=True),
        SearchableField(name="text", type=SearchFieldDataType.String),
        SearchField(
            name="text_vector",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            searchable=True,
            vector_search_dimensions=3072,  # text-embedding-3-large is 3072 dims
            vector_search_profile_name="myHnswProfile"
        )
    ]

    # Configure Vector Search
    vector_search = VectorSearch(
        algorithms=[HnswAlgorithmConfiguration(name="myHnsw")],
        profiles=[VectorSearchProfile(name="myHnswProfile", algorithm_configuration_name="myHnsw")]
    )

    index = SearchIndex(name=index_name, fields=fields, vector_search=vector_search)
    
    logger.info(f"Creating index '{index_name}' with the correct schema...")
    client.create_index(index)
    logger.info("SUCCESS! Index created correctly. You can now run seed_azure.py")

if __name__ == "__main__":
    create_index()
