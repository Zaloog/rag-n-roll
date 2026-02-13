# - [ ] `POST /api/query` — proxies to the query service using `httpx.AsyncClient`
# - [ ] `POST /api/ingest` — proxies to the ingestion service using `httpx.AsyncClient`
# - [ ] `GET /health` — returns own health + checks downstream services
# - [ ] Serve static files from the `static/` directory
# - [ ] Use `config.py` for service URLs (INGESTION_URL, QUERY_URL)
from fastapi.responses import FileResponse
from pathlib import Path

from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from httpx import AsyncClient

from gateway.app.config import settings
# Get the static directory path (relative to this file)
STATIC_DIR = Path(__file__).parent.parent / "static"

# Mount static files
app = FastAPI(
)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

class Query(BaseModel):
    question: str

@app.get("/")
def home():
    return FileResponse(STATIC_DIR/"index.html")

@app.get("/health")
def check_status():
    return {"status": "ok"}


# curl -X POST http://localhost:8000/api/query \
#   -H "Content-Type: application/json" \
#   -d '{"question": "What is the recommended oil type for the engine?"}'



@app.post("/api/query")
async def post_query(query: Query):
    client = AsyncClient(base_url=settings.query_url, timeout=120)
    async with client:
        response = await client.post("/query", json={"question": query.question})
    return response.json()

@app.post("/api/ingest")
async def post_ingest():
    client = AsyncClient(base_url=settings.ingestion_url, timeout=120)
    async with client:
        response = await client.post("/ingest")
    return response.json()
