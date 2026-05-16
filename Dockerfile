# Sauti ya Mwananchi — Production Dockerfile
FROM python:3.12-slim AS builder

WORKDIR /build
RUN apt-get update && apt-get install -y --no-install-recommends gcc && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.12-slim AS runtime
RUN groupadd -r appuser && useradd -r -g appuser -s /bin/false appuser
WORKDIR /app
COPY --from=builder /install /usr/local
COPY src/ ./src/
COPY data/ ./data/
RUN chown -R appuser:appuser /app
USER appuser

ENV PORT=8080 \
    PYTHONUNBUFFERED=1
EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health')" || exit 1

CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
