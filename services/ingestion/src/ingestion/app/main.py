import logging

from pydantic import BaseModel
from fastapi import FastAPI
from ingestion.app.pipeline import process_files, DATA_PATH

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI()

class IngestResponse(BaseModel):
    status: str
    collection_name: str
    documents_processed: int


@app.post("/ingest", response_model=IngestResponse)
def ingest_doc():
    index, doc_count = process_files(data_path=DATA_PATH)

    logger.info(f"Ingesting {doc_count} files")
 
    return IngestResponse(
        status="success",
        collection_name="docs",
        documents_processed=doc_count
    )

@app.get("/health")
def check_health():
    return {"status": "ok"}
