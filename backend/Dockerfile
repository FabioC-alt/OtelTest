FROM python:3.11-slim

WORKDIR /app
COPY backend.py .

RUN pip install \
    flask \
    opentelemetry-api \
    opentelemetry-sdk \
    opentelemetry-exporter-jaeger \
    opentelemetry-instrumentation-flask

CMD ["python", "backend.py"]

