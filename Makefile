.PHONY: all up down ingest forward-gateway forward-qdrant logs colima build-images push-images deploy aks-login

# ACR configuration
ACR_NAME ?= docassistservice
ACR_SERVER = $(ACR_NAME).azurecr.io
VERSION ?= v1

# Local development
up:
	docker compose up --build -d

down:
	docker compose down

ingest:
	curl -X POST http://localhost:8000/api/ingest

logs:
	docker compose logs -f

colima:
	colima start --cpu 4 --memory 24

# AKS deployment
aks-login:
	az acr login --name $(ACR_NAME)

build-images:
	@echo "Building images for linux/amd64..."
	docker build --platform linux/amd64 -t $(ACR_SERVER)/gateway:$(VERSION) services/gateway/
	docker build --platform linux/amd64 -t $(ACR_SERVER)/ingestion:$(VERSION) services/ingestion/
	docker build --platform linux/amd64 -t $(ACR_SERVER)/query:$(VERSION) services/query/

push-images: aks-login
	@echo "Pushing images to ACR..."
	docker push $(ACR_SERVER)/gateway:$(VERSION)
	docker push $(ACR_SERVER)/ingestion:$(VERSION)
	docker push $(ACR_SERVER)/query:$(VERSION)

deploy:
	@echo "Deploying to AKS..."
	kubectl apply -k k8s/overlays/aks/
	kubectl rollout status deployment/gateway-deployment -n doc-assist
	kubectl rollout status deployment/ingestion-deployment -n doc-assist
	kubectl rollout status deployment/query-deployment -n doc-assist

deploy-all: build-images push-images deploy
	@echo "Deployment complete!"

forward-gateway:
	kubectl port-forward -n doc-assist svc/gateway 8000:8000

forward-qdrant:
	kubectl port-forward -n doc-assist svc/qdrant 6333:6333
