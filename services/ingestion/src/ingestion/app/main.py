import logging
import shutil
from pathlib import Path
from typing import List

from pydantic import BaseModel
from fastapi import FastAPI, UploadFile, File, HTTPException
from ingestion.app.pipeline import process_files, DATA_PATH, process_uploaded_files

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI()

# Temporary upload directory
UPLOAD_DIR = Path("/tmp/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

class IngestResponse(BaseModel):
    status: str
    collection_name: str
    documents_processed: int


@app.post("/ingest", response_model=IngestResponse)
def ingest_doc():
    """Ingest documents from the mounted /app/data directory"""
    index, doc_count = process_files(data_path=DATA_PATH)

    logger.info(f"Ingesting {doc_count} files")
 
    return IngestResponse(
        status="success",
        collection_name="docs",
        documents_processed=doc_count
    )


@app.post("/upload", response_model=IngestResponse)
async def upload_and_ingest(files: List[UploadFile] = File(...)):
    """Upload and ingest documents from user file selection"""
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")
    
    # Create a temporary directory for this upload batch
    import uuid
    batch_id = uuid.uuid4().hex
    batch_dir = UPLOAD_DIR / batch_id
    batch_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        # Save uploaded files to temporary directory
        saved_files = []
        for upload_file in files:
            file_path = batch_dir / upload_file.filename
            
            logger.info(f"Saving uploaded file: {upload_file.filename}")
            
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(upload_file.file, buffer)
            
            saved_files.append(file_path)
        
        logger.info(f"Processing {len(saved_files)} uploaded files from batch {batch_id}")
        
        # Process the uploaded files
        index, doc_count = process_uploaded_files(file_paths=saved_files)
        
        logger.info(f"Successfully ingested {doc_count} uploaded documents")
        
        return IngestResponse(
            status="success",
            collection_name="docs",
            documents_processed=doc_count
        )
    
    except Exception as e:
        logger.error(f"Error processing uploaded files: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to process files: {str(e)}")
    
    finally:
        # Clean up temporary files
        try:
            if batch_dir.exists():
                shutil.rmtree(batch_dir)
                logger.info(f"Cleaned up temporary directory: {batch_id}")
        except Exception as e:
            logger.warning(f"Failed to clean up temporary directory {batch_id}: {str(e)}")


@app.get("/health")
def check_health():
    return {"status": "ok"}
