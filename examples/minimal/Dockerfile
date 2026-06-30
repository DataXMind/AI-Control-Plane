FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md LICENSE ./
COPY src ./src
COPY tests/fixtures/config ./tests/fixtures/config

RUN pip install --no-cache-dir -e ".[redis]"

EXPOSE 8000

CMD ["uvicorn", "ai_control_plane.api.server:app", "--host", "0.0.0.0", "--port", "8000"]
