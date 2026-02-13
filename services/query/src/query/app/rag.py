# Connect to existing Qdrant collection (`docs`)
# Set up `OllamaEmbedding` (same model as ingestion: `nomic-embed-text`)
# Set up `Ollama` LLM (`llama3.2:3b`, `request_timeout=120`)
# Create a `VectorStoreIndex.from_vector_store(...)` (loads existing index, no re-ingestion)
# Create a `query_engine` with `similarity_top_k=5`
# **Key insight:** The query engine embeds the question, finds the 5 most similar chunks, puts them in the prompt, and sends it to the LLM. Understand each step.
from anyio.functools import lru_cache

from qdrant_client import QdrantClient, AsyncQdrantClient
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.llms.ollama import Ollama

from query.app.config import settings
from query.app.prompts import qa_prompt


QDRANT_CLIENT = QdrantClient(url=settings.qdrant_url)
QDRANT_ACLIENT = AsyncQdrantClient(url=settings.qdrant_url)

@lru_cache()
def setup_query_engine():
    llm = Ollama(
        model=settings.model, 
        base_url=settings.ollama_url,
        request_timeout=120
    )

    ollama_embedding = OllamaEmbedding(
        model_name="nomic-embed-text",
        base_url=settings.ollama_url
    )

    vector_store = QdrantVectorStore(
        collection_name="docs",
        # client=QDRANT_CLIENT,
        aclient=QDRANT_ACLIENT,
        enable_hybrid=False,

    )

    index = VectorStoreIndex.from_vector_store(
        vector_store=vector_store,
        embed_model=ollama_embedding,
        )

    query_engine = index.as_query_engine(
        llm=llm,
        similarity_top_k=settings.match_amount
        
    )

    query_engine.update_prompts(
            {"response_synthesizer:text_qa_template": qa_prompt}
        )
    return query_engine


async def async_rag(query: str):

    engine = setup_query_engine()
    response = await engine.aquery(query)

    return response

if __name__ == "__main__":
    response = async_rag("tell me about the specs of the BF4M 2012C model, and mention the source file, create a table")
    print(response)
