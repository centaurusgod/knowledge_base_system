import logging

from ..configs.embedding_model_config import get_embedding_client

logger = logging.getLogger(__name__)


def text_to_embedding(text: str) -> list[float]:
    model, client = get_embedding_client()
    response = client.embeddings.create(model=model, input=text)
    logger.info(f"Generated embedding for text: {text[:30]}...")
    return response.data[0].embedding
