from fastapi import FastAPI
from pydantic import BaseModel
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource


app = FastAPI()

trace.set_tracer_provider(TracerProvider(
    resource=Resource.create({"service.name": "app_b"}) 
))
span_processor = BatchSpanProcessor(OTLPSpanExporter(endpoint="http://otel-collector:4318/v1/traces"))
trace.get_tracer_provider().add_span_processor(span_processor)

FastAPIInstrumentor.instrument_app(app)
RequestsInstrumentor().instrument()




class Message(BaseModel):
    sender: str
    text: str

@app.post("/receive")
def receive_message(msg: Message):
    print(f"Received message from {msg.sender}: {msg.text}")
    return {"status": "received", "echo": msg.text}
