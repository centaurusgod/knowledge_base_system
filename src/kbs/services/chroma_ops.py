import logging
import uuid

from ..configs.chroma_db import chroma_client, get_or_create_chroma_collection

logger = logging.getLogger(__name__)
MAX_RECENT_ITEMS = 10


def remove_all_chroma_collections():
    """Remove all Chroma collections."""
    chroma_client.delete_collection(name="engineering_memories")


def add_to_chroma_collection(
    embeddings: list[list[float]], metadatas: list[dict], documents: list[str]
):

    logger.info(
        f"Adding to Chroma collection with {len(embeddings)} embeddings and {len(metadatas)} metadatas."
    )
    collection = get_or_create_chroma_collection()

    memory_id = str(uuid.uuid4())

    collection.add(
        ids=[memory_id], embeddings=embeddings, metadatas=metadatas, documents=documents
    )

    logger.info(f"Successfully added memory with ID {memory_id} to Chroma collection.")


def search_chroma_collection(query_embeddings: list[list[float]], most_recent: int):
    collection = get_or_create_chroma_collection()

    search_results = collection.query(
        query_embeddings=query_embeddings,
        n_results=min(most_recent, MAX_RECENT_ITEMS),
        include=["metadatas", "documents", "distances"],
    )

    formatted_results = []
    if (
        search_results
        and search_results.get("documents")
        and search_results["documents"][0]
    ):
        ids = search_results["ids"][0]
        documents = search_results["documents"][0]
        metadatas = search_results["metadatas"][0]
        distances = search_results["distances"][0]

        for doc_id, doc, meta, dist in zip(ids, documents, metadatas, distances):
            formatted_results.append(
                {
                    "id": doc_id,
                    "document": doc,
                    "metadata": meta,
                    "similarity_score": round(1.0 - dist, 4),
                }
            )

    return {"type": "semantic_search", "results": formatted_results}
