.Phony: all

up:
	docker compose up --build -d

down:
	docker compose down

ingest:
	curl -X POST http://localhost:8000/api/ingest

query:
	interactive query (or a test query)

logs:
	docker compose logs -f

colima:
	colima start --cpu 4 --memory 24
