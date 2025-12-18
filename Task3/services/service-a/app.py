import typing as t
from flask import Flask
import httpx
from opentelemetry import trace
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter


SERVICE_B_URL = "http://service-b:8080/"
OTEL_EXPORTER_OTLP_ENDPOINT = "http://simplest-collector:4317"

trace.set_tracer_provider(
    TracerProvider(resource=Resource.create({SERVICE_NAME: "service-a"}))
)
otlp_exporter = OTLPSpanExporter(endpoint=OTEL_EXPORTER_OTLP_ENDPOINT, insecure=True)
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(otlp_exporter))

app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()
tracer = trace.get_tracer(__name__)


@app.route("/")
def root() -> dict[str, t.Any]:
    with tracer.start_as_current_span("service-a-root") as span:
        span.set_attribute("component", "service-a")
        span.set_attribute("http.route", "/")

        with tracer.start_as_current_span("call-service-b") as call_span:
            call_span.set_attribute("http.url", SERVICE_B_URL)

            headers: dict[str, str] = {}

            with httpx.Client() as client:
                resp = client.get(SERVICE_B_URL, headers=headers, timeout=5.0)
                resp.raise_for_status()
                data = resp.json()

            return {
                "service": "a",
                "downstream": data,
            }
