"""OpenTelemetry integration for distributed tracing."""

from __future__ import annotations

from contextlib import contextmanager
import logging
from typing import Any

try:
    from opentelemetry import trace
    from opentelemetry.exporter.jaeger.thrift import JaegerExporter
    from opentelemetry.sdk.resources import SERVICE_NAME, Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    _OTEL_AVAILABLE = True
except ImportError:
    _OTEL_AVAILABLE = False

_logger = logging.getLogger(__name__)


class _DummySpan:
    def set_attribute(self, *args: Any, **kwargs: Any) -> None:
        pass

    def add_event(self, *args: Any, **kwargs: Any) -> None:
        pass

    def record_exception(self, *args: Any, **kwargs: Any) -> None:
        pass

    def set_status(self, *args: Any, **kwargs: Any) -> None:
        pass


class _DummyTracer:
    def start_as_current_span(self, name: str, *args: Any, **kwargs: Any) -> Any:
        @contextmanager
        def dummy_context():
            yield _DummySpan()
        return dummy_context()


def init_tracer(service_name: str = "cloudoptima") -> Any:
    """Initialize OpenTelemetry tracer or fallback to dummy tracer."""
    if not _OTEL_AVAILABLE:
        return _DummyTracer()

    resource = Resource(attributes={
        SERVICE_NAME: service_name
    })

    provider = TracerProvider(resource=resource)

    try:
        jaeger_exporter = JaegerExporter(
            agent_host_name="localhost",
            agent_port=6831,
        )
        processor = BatchSpanProcessor(jaeger_exporter)
        provider.add_span_processor(processor)
        trace.set_tracer_provider(provider)
        _logger.info("OpenTelemetry tracer initialized with Jaeger exporter")
    except Exception:
        _logger.warning("Failed to initialize Jaeger exporter, falling back to NoOp", exc_info=True)
        return trace.NoOpTracer()

    return trace.get_tracer(__name__)


# Global tracer instance
tracer = init_tracer()


def get_tracer() -> Any:
    """Return the global tracer instance."""
    return tracer
