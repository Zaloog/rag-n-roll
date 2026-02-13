FROM python:3.13-slim-trixie

# Copy uv binary
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Copy dependency files first for caching
COPY pyproject.toml uv.lock README.md ./

# Disable development dependencies
ENV UV_NO_DEV=1

# Install dependencies
RUN uv sync --locked --no-install-project

# Copy source code
COPY src ./src

# Install the project
RUN uv sync --locked

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "gateway.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
