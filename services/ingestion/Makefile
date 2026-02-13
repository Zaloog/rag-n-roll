.Phony: all

qdrant:
	docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant

ingest:
	uvicorn ingestion.app.main:app --port 8001 --reload
