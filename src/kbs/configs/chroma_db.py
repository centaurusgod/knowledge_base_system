import logging

import chromadb

logger = logging.getLogger(__name__)

chroma_client = chromadb.PersistentClient(path="./dev_brain_db")


# Set default name as engineering_memories
def get_or_create_chroma_collection(collection_name: str = "engineering_memories"):
    """Get or create a Chroma collection."""
    return chroma_client.get_or_create_collection(name=collection_name)
