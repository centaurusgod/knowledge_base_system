import logging
from functools import lru_cache

from openai import OpenAI

logger = logging.getLogger(__name__)

EMBEDDING_MODEL_NAME = "embed-gemma"


@lru_cache(maxsize=1)
def get_embedding_client() -> tuple[str, OpenAI]:
    """Initializes and caches the OpenAI client instance on first call."""
    return EMBEDDING_MODEL_NAME, OpenAI(
        base_url="http://127.0.0.1:52625/v1",
        api_key="flm",
    )
