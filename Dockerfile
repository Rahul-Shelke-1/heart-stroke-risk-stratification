FROM python:3.11.7-slim

# 1. Environment variables for uv
ENV UV_SYSTEM_PYTHON=1 \
    UV_NO_CACHE=1

WORKDIR /app

# 2. Install system dependencies + uv
RUN apt-get update && apt-get install -y --no-install-recommends curl && \
    curl -LsSf https://astral.sh/uv/install.sh | sh && \
    mv /root/.local/bin/uv /usr/local/bin/uv && \
    apt-get purge -y --auto-remove curl && \
    rm -rf /var/lib/apt/lists/*

# 3. Copy dependency files first (for caching)
COPY pyproject.toml uv.lock /app/

# 4. Install dependencies using uv (production only)
RUN uv sync --frozen --no-dev

# 5. Copy application code
COPY . /app/

# 6. Run application
CMD ["python3", "app.py"]
