FROM python:3.11-slim

WORKDIR /app
COPY frontend.py .

RUN pip install \
    flask \
    requests \
    opentelemetry-api \
    opentelemetry-sdk \
    opentelemetry-exporter-jaeger \
    opentelemetry-instrumentation-flask \
    opentelemetry-instrumentation-requests

CMD ["python", "frontend.py"]

