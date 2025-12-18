from flask import Flask

from opentelemetry import trace
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

OTEL_EXPORTER_OTLP_ENDPOINT = "http://simplest-collector:4317"

trace.set_tracer_provider(
    TracerProvider(resource=Resource.create({SERVICE_NAME: "service-b"}))
)
otlp_exporter = OTLPSpanExporter(endpoint=OTEL_EXPORTER_OTLP_ENDPOINT, insecure=True)
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(otlp_exporter))

app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()
tracer = trace.get_tracer(__name__)


@app.route("/")
def state():
    with tracer.start_as_current_span("service-b-handler") as span:
        span.set_attribute("component", "service-b")
        span.set_attribute("http.route", "/")
        return {
            "service": "b",
            "message": "ok",
        }
