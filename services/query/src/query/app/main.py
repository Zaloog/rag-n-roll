import logging

from pydantic import BaseModel

from fastapi import FastAPI
from query.app.rag import async_rag

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
)

class Query(BaseModel):
    question: str

class RagResponse(BaseModel):
    answer: str
    sources: list[dict]

@app.get("/health")
def check_status():
    return {"status": "ok"}

@app.post("/query", response_model=RagResponse)
async def query_index(query: Query):

    logger.info(f"Processing query: {query.question}")

    response = await async_rag(query.question)
    answer = response.response or ""
    sources = []
    for node in response.source_nodes:
        source = {
            "score": node.score,
            "file_name": node.node.metadata.get("file_name"),
            "page_label": node.metadata.get("page_label")
        }
        sources.append(source)

    return RagResponse(answer=answer, sources=sources)
