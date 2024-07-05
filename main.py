# This is a sample Python script for send trace data to xtrace

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

# coding=utf-8
from opentelemetry.sdk.resources import Resource, SERVICE_NAME, SERVICE_VERSION
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter as OTLPSpanHttpExporter
from opentelemetry import trace

resource = Resource(
    attributes={
        SERVICE_NAME: 'aliyun_trace_demo',
        SERVICE_VERSION: '0.0.1',
        "source": "python agent",
    }
)
# 填写xtrace的地址
trace_endpoint = "http://xxx.aliyuncs.com/"
span_exporter = BatchSpanProcessor(OTLPSpanHttpExporter(
    endpoint=trace_endpoint,
))
provider = TracerProvider(resource=resource)

provider.add_span_processor(span_exporter)
provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))  # 在控制台输出Trace
trace.set_tracer_provider(provider)

if __name__ == '__main__':
    tracer_provider = trace.get_tracer_provider()
    _tracer = trace.get_tracer(__name__, tracer_provider=tracer_provider)
    with _tracer.start_as_current_span("test_span") as test_span:
        # add custome attribute
        test_span.set_attribute("test.attribute", "test.value")
        test_span.set_attribute("test.attribute1", "test.value1")
