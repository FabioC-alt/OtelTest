FROM python:3.11-slim

WORKDIR /app

COPY frontend.py .

# Install your app dependencies + OpenTelemetry SDK + OTLP exporter
RUN pip install flask requests \
    opentelemetry-distro \
    opentelemetry-exporter-otlp \
    opentelemetry-instrument \
 && opentelemetry-bootstrap -a install

# Use OpenTelemetry to run the app with auto-instrumentation
CMD ["opentelemetry-instrument", "python", "frontend.py"]

