from fastapi import FastAPI
import httpx
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource


app = FastAPI()

trace.set_tracer_provider(TracerProvider(
    resource=Resource.create({"service.name": "app_a"}) 
))
span_processor = BatchSpanProcessor(OTLPSpanExporter(endpoint="http://otel-collector:4318/v1/traces"))
trace.get_tracer_provider().add_span_processor(span_processor)

FastAPIInstrumentor.instrument_app(app)
RequestsInstrumentor().instrument()




@app.get("/send")
def send_message():
    message = {"sender": "App A", "text": "Hello from App A!"}
    response = httpx.post("http://app_b:8000/receive", json=message)
    return {"app_b_response": response.json()}
