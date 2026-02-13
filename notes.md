# Questions
- Does llama3.2:3b use the nomic-embed-text?

# Ollama
- use `ollama serve` to start
- use `ollama list` to show models
- Allows running LLMs locally

## Needs two models for ollama
- Embedding Model: nomic-embed-text
    - link: https://ollama.com/library/nomic-embed-text
    - info link: https://www.cloudflare.com/learning/ai/what-are-embeddings/
    - embeds text -> representation, to make the text understandable for the model (vector)
    by transforming it into a mathematical form
    - They enable machine learning models to find similar objects
- LLM: llama3.2:3b
    - link: https://ollama.com/library/llama3.2:3b
    - Meta's Llama 3.2 goes small with 1B and 3B models.

# Qdrant
- run with: `docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant`
then visit: http://localhost:6333/dashboard
- port 6333 for the http API
- port 6334 for the gRPC(Google remote procedure Call,
calling a subroutine in a different adress space) API
- port 6335 for distributed deployment

## Qdrant Concepts
- Collections are a set of searchable points
- Points are records of a vector and optional payload
- Payload describes information that you can store with vectors

- Inference: process of creating embeddings from text/image
- Optimizer rebuilds database structure for faster search, including
a vacuum, a merge and an indexing optimizer

# Rag Part
- Prompt is build with context_str and query_str placeholders
- Prompt uses the query_str and fills the context_str with the top k matches from the index,
After that its forwarded to the llm

# Gateway
- Acts as a single entrypoint to all services, routed via async client
- Services that must run
    - gateway service at port 8000
    - ingest service at port 8001
    - query service at port 8002
    - qdrant container for vector db
    - ollama server for llm

# HTML
- <head> holds meta information for the page
- Semantic HTML5 Elements
    - to communicate meaning better, instead of <div>, <span> semantic elements like
    <section>, <nav>, <header>, <article> are used
    - <section>: "A section is a thematic grouping of content, typically with a heading"
    - <article>: "Specifies independent, self-contained content"
    - <header>: "Introductory content or set of navigational links"
    - <footer>: "footer for document or section, for e.g. authorship information"
    - <nav>: set of navigational links
