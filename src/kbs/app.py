import logging

from fastapi import FastAPI, HTTPException, status

from .configs.logging_config import configure_logging
from .models.kbs_template import KnowledgeBaseTemplate
from .services.chroma_ops import add_to_chroma_collection, search_chroma_collection
from .services.embeddings import text_to_embedding

logger = logging.getLogger(__name__)
configure_logging()

app = FastAPI()


# Copilot sends a GET request to /search-memory with a query string to search the knowledge base
# Also support fetching n most recent memories, with a query string like /search-memory?recent=n
@app.get("/search-memory")
async def search_knowledge_base(query: str | None = None, recent: int = 2):

    if query is None:
        raise HTTPException(
            status_code=422,
            detail="Query parameter is required for searching the knowledge base.",
        )

    try:
        embeddings = text_to_embedding(query)

        results = search_chroma_collection(
            query_embeddings=[embeddings], most_recent=recent
        )

        return results
    except Exception as e:
        logger.error(f"An error occurred while searching the knowledge base: {e}")
        raise HTTPException(
            status_code=400, detail=f"Failed to search the knowledge base. {e!s}"
        )

# Copilot first searches the knowledge base, if no relevant information found, it will post the new information
# It may also add an additional row to new infromation, but with new date
@app.post("/add-memory", status_code=status.HTTP_201_CREATED)
async def add_knowledge_base(memory: KnowledgeBaseTemplate):

    searchable_text = (
        f"Tags: {memory.tag}\n"
        f"Repository: {memory.repository_name}\n"
        f"Problem: {memory.problem_description}\n"
        f"Solution: {memory.problem_solution}\n"
        f"Additional Context: {memory.new_information}"
    )
    try:
        embeddings = text_to_embedding(searchable_text)

        existing = search_chroma_collection(query_embeddings=[embeddings], most_recent=1)
        
        if existing["results"]:
            top_match = existing["results"][0]
            if top_match["similarity_score"] >= 0.90:
                return {
                    "status": "skipped",
                    "message": f"Similar memory already exists ({top_match['similarity_score'] * 100:.1f}% match).",
                    "existing_id": top_match["id"]
                }

        metadatas_dict = memory.model_dump()

        # Print first 5 elements of the embeddings for debugging
        logger.info(f"First 5 elements of embeddings: {embeddings[:5]}")

        add_to_chroma_collection(
            embeddings=[embeddings],
            metadatas=[metadatas_dict],
            documents=[searchable_text],
        )

        return {"message": "Memory added to the knowledge base successfully."}

    except Exception as e:
        logger.error(
            f"An error occurred while adding memory to the knowledge base: {e}"
        )
        raise HTTPException(
            status_code=400,
            detail=f"Failed to add memory to the knowledge base. {e!s}",
        )


@app.post("/remove-all-memories", status_code=status.HTTP_200_OK)
async def remove_all_memories():
    try:
        from .services.chroma_ops import remove_all_chroma_collections

        remove_all_chroma_collections()
        return {"message": "All memories removed from the knowledge base successfully."}
    except Exception as e:
        logger.error(
            f"An error occurred while removing all memories from the knowledge base: {e}"
        )
        raise HTTPException(
            status_code=400,
            detail=f"Failed to remove all memories from the knowledge base. {e!s}",
        )
