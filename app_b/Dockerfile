FROM python:3.10-slim

WORKDIR /app
COPY . .

RUN pip install fastapi uvicorn httpx \
    opentelemetry-sdk \
    opentelemetry-exporter-otlp \
    opentelemetry-instrumentation-fastapi \
    opentelemetry-instrumentation-requests

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
