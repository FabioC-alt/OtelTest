from flask import Flask, jsonify
import requests
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter

resource = Resource(attributes={
    "service.name": "frontend"
})

provider = TracerProvider(resource=resource)

jaeger_exporter = JaegerExporter(
    collector_endpoint="http://jaeger.observability.svc.cluster.local:14268/api/traces",
)

span_processor = BatchSpanProcessor(jaeger_exporter)
provider.add_span_processor(span_processor)

trace.set_tracer_provider(provider)
tracer = trace.get_tracer("my.tracer.name")

app = Flask(__name__)

@app.route("/api/forward")
def forward_request():
    with tracer.start_as_current_span("forward-request") as span:
        try:
            backend_response = requests.get("http://backend-service:5000/api/data")
            backend_json = backend_response.json()
            return jsonify(backend_json)
        except Exception as e:
            return jsonify(error=str(e)), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

