# - [ ] `POST /api/query` — proxies to the query service using `httpx.AsyncClient`
# - [ ] `POST /api/ingest` — proxies to the ingestion service using `httpx.AsyncClient`
# - [ ] `GET /health` — returns own health + checks downstream services
# - [ ] Serve static files from the `static/` directory
# - [ ] Use `config.py` for service URLs (INGESTION_URL, QUERY_URL)
from fastapi.responses import FileResponse
from pathlib import Path
from typing import List

from pydantic import BaseModel
from fastapi import FastAPI, UploadFile, File
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

@app.post("/api/upload")
async def post_upload(files: List[UploadFile] = File(...)):
    """Proxy file uploads to the ingestion service"""
    client = AsyncClient(base_url=settings.ingestion_url, timeout=300)
    
    # Prepare files for multipart upload
    files_to_upload = []
    for file in files:
        # Read file content and prepare for forwarding
        content = await file.read()
        files_to_upload.append(
            ("files", (file.filename, content, file.content_type))
        )
    
    async with client:
        response = await client.post("/upload", files=files_to_upload)
    
    return response.json()
