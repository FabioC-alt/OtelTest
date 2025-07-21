import logging
from flask import Flask, jsonify, request

from opentelemetry import trace
from opentelemetry.propagate import extract
from opentelemetry.instrumentation.flask import FlaskInstrumentor

from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define service name for Jaeger
resource = Resource(attributes={"service.name": "backend"})

# Setup tracer
provider = TracerProvider(resource=resource)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer("my.tracer.name")

# Setup Jaeger exporter
jaeger_exporter = JaegerExporter(
    collector_endpoint="http://jaeger.observability.svc.cluster.local:14268/api/traces"
)

# Add span processor
span_processor = BatchSpanProcessor(jaeger_exporter)
provider.add_span_processor(span_processor)

# Flask app
app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)  # ✅ Instrument Flask

@app.route("/api/data")
def get_data():
    context = extract(request.headers)  # ✅ Extract parent context from incoming request
    with tracer.start_as_current_span("backend-request", context=context):
        logger.info("Serving data to frontend.")
        return jsonify(message="Hello from the backend!")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

