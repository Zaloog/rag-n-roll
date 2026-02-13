from pathlib import Path

from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.vector_stores.qdrant import QdrantVectorStore

from qdrant_client import QdrantClient, AsyncQdrantClient
from ingestion.app.config import settings

DATA_PATH = Path("/app/data")

QDRANT_CLIENT = QdrantClient(url=settings.qdrant_url)
QDRANT_ACLIENT = AsyncQdrantClient(url=settings.qdrant_url)

def process_files(data_path: Path): 
    reader = SimpleDirectoryReader(
        input_dir=data_path,
        recursive=True
    )

    documents = reader.load_data(show_progress=True)

    sentence_splitter = SentenceSplitter(
        chunk_size=256,
        chunk_overlap=25
    )

    ollama_embedding = OllamaEmbedding(
        model_name="nomic-embed-text",
        base_url=settings.ollama_url
    )

    vector_store = QdrantVectorStore(
        collection_name="docs",
        client=QDRANT_CLIENT,
        aclient=QDRANT_ACLIENT,
        enable_hybrid=False,

    )
    storage_context = StorageContext.from_defaults(
        vector_store=vector_store
    )

    index = VectorStoreIndex.from_documents(
        documents=documents,
        transformations=[sentence_splitter],
        embed_model=ollama_embedding,
        storage_context=storage_context,
        show_progress=True,
        num_workers=4,  # Process 4 chunks in parallel
        )

    return index, len(documents)


if __name__ == "__main__":
    process_files(DATA_PATH)
