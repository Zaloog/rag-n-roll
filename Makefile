.Phony: all

up:
	docker compose up --build -d

down:
	docker compose down

ingest:
	curl -X POST http://localhost:8000/api/ingest

# forward port to access qdrant and gateway from minikube cluster
forward:
	kubectl port-forward -n doc-assist svc/gateway 8000:8000
	# kubectl port-forward -n doc-assist svc/qdrant 6333:6333

logs:
	docker compose logs -f

# start bigger colima instance
colima:
	colima start --cpu 4 --memory 24
