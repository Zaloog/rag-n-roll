# Rag-n-Roll
This is a simple test project to get familiar with

- RAG, via qdrant Vector database + ollama models
- fastapi as backend
- Docker + Kubernetes to deploy the services locally/remote
- Terraform/Opentofu for provisioning ressources in the Azure cloud


# Project Structure

## Services
This project is composed of 5 different services in total
1. [qdrant] for the vector database
2. [ollama] for local language model + embeddings (`llama3.2:1b` is used here and `nomic-embed-text` embeddings)
3. ingestion service ([fastapi]) for ingesting new data into the vector database
4. query service ([fastapi]) for querying the vectorDB and providing the interaction with the LLM
5. gateway service ([fastapi]) as an entrypoint to interact with the `query` and `ingestion` service via a simple Webpage

## K8S
[minikube] is used to run a local Kubernetes cluster to provision the whole infrastructure.
The services can also be used via [docker-compose].

## Infrastructure
[opentofu] is used to provision required resources and build the infrastructure in [azure].

<!-- Links -->
[qdrant]: https://qdrant.tech/
[ollama]: https://ollama.com/
[fastapi]: https://fastapi.tiangolo.com/
[minikube]: https://minikube.sigs.k8s.io/docs/
[docker-compose]: https://docs.docker.com/compose/
[opentofu]: https://opentofu.org/
[azure]: https://azure.microsoft.com/en-us
