import json
from typing import Optional
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize the FastMCP server
mcp = FastMCP("DeveloperMemoryBridge")

FASTAPI_URL = "http://localhost:8000"
SEARCH_MEMORY_ENDPOINT = f"{FASTAPI_URL}/search-memory"
SAVE_MEMORY_ENDPOINT = f"{FASTAPI_URL}/add-memory"


@mcp.tool()
async def search_memory(query: str, recent: int = 3) -> str:
    """
    Search your digital memory knowledge base for past solutions, bugs, or repo discoveries.
    Always run this first when troubleshooting or investigating architecture questions.
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                SEARCH_MEMORY_ENDPOINT,
                params={"query": query, "recent": recent},
                timeout=10.0,
            )
            response.raise_for_status()
            return json.dumps(response.json(), indent=2)
        except Exception as e:
            return f"Error querying knowledge base: {str(e)}"


@mcp.tool()
async def save_memory(
    tag: str,
    repository_name: str,
    problem_description: str,
    problem_solution: str,
    new_information: str,
    date_added: str,
    version: Optional[str] = "1.0.0",
) -> str:
    """
    Save a new engineering solution, bug resolution, or repository discovery into the knowledge base.
    Call this when the user confirms they want to remember a resolution.
    """
    payload = {
        "tag": tag,
        "repository_name": repository_name,
        "version": version,
        "problem_description": problem_description,
        "problem_solution": problem_solution,
        "new_information": new_information,
        "date_added": date_added,
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                SAVE_MEMORY_ENDPOINT, json=payload, timeout=10.0
            )
            response.raise_for_status()
            return json.dumps(response.json(), indent=2)
        except Exception as e:
            return f"Error saving to knowledge base: {str(e)}"


if __name__ == "__main__":
    # Runs the stdio loop required by IDEs like VS Code / Copilot
    mcp.run(transport="stdio")