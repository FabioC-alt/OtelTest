FROM python:3.11-slim
WORKDIR /app
COPY frontend.py .
RUN pip install flask requests
RUN pip install opentelemetry-api
RUN pip install opentelemetry-sdk
RUN pip install opentelemetry-exporter-jaeger
RUN pip install deprecated
CMD ["python", "frontend.py"]

