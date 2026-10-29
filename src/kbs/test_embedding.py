import logging

from openai import OpenAI

logger = logging.getLogger(__name__)

client = OpenAI(
    base_url="http://127.0.0.1:52625/v1",
    api_key="flm",  # dummy key, FastFlowLM doesn't require auth
)

resp = client.embeddings.create(
    model="Embedding-Gemma-300M-NPU2",
    input="Universe is singing a song, universe is dancing along, Universe is singing in a day like this",
)

embedding = resp.data[0].embedding

print("embedding length:", len(embedding))
print("first 10 values:", embedding[:10])
