from flask import Flask, jsonify
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider    # Fixed: was TraceProvider typo
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter   # Fixed: was JeagerExporter typo


resource = Resource(attributes={
    "service.name": "backend"
})

provider = TracerProvider(resource=resource)    # Fixed typo TraceProvider -> TracerProvider

jaeger_exporter = JaegerExporter(              # Fixed typo JeagerExporter -> JaegerExporter
    collector_endpoint="http://jaeger.observability.svc.cluster.local:14268/api/traces",
)

span_processor = BatchSpanProcessor(jaeger_exporter)
provider.add_span_processor(span_processor)

trace.set_tracer_provider(provider)
tracer = trace.get_tracer("my.tracer.name")

app = Flask(__name__)

@app.route("/api/data")
def get_data():
    with tracer.start_as_current_span("backend-request") as span:
        return jsonify(message="Hello from the backend!")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

