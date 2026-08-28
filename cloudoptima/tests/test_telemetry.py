"""Tests for OpenTelemetry tracing and fallback mechanisms."""

import sys
from unittest.mock import MagicMock

import cloudoptima.telemetry


def test_telemetry_unavailable():
    """Test telemetry fallback when OTEL is missing."""
    old_avail = cloudoptima.telemetry._OTEL_AVAILABLE
    cloudoptima.telemetry._OTEL_AVAILABLE = False
    
    try:
        tracer = cloudoptima.telemetry.init_tracer()
        with tracer.start_as_current_span("test"):
            pass
            
        assert cloudoptima.telemetry.get_tracer() is not None
    finally:
        cloudoptima.telemetry._OTEL_AVAILABLE = old_avail


def test_telemetry_available():
    """Test telemetry when OTEL is available."""
    mock_trace = MagicMock()
    mock_jaeger = MagicMock()
    mock_resources = MagicMock()
    mock_sdk_trace = MagicMock()
    mock_sdk_export = MagicMock()
    
    sys.modules["opentelemetry"] = MagicMock()
    sys.modules["opentelemetry.trace"] = mock_trace
    sys.modules["opentelemetry.exporter"] = MagicMock()
    sys.modules["opentelemetry.exporter.jaeger"] = MagicMock()
    sys.modules["opentelemetry.exporter.jaeger.thrift"] = mock_jaeger
    sys.modules["opentelemetry.sdk"] = MagicMock()
    sys.modules["opentelemetry.sdk.resources"] = mock_resources
    sys.modules["opentelemetry.sdk.trace"] = mock_sdk_trace
    sys.modules["opentelemetry.sdk.trace.export"] = mock_sdk_export
    
    old_avail = cloudoptima.telemetry._OTEL_AVAILABLE
    cloudoptima.telemetry._OTEL_AVAILABLE = True
    
    cloudoptima.telemetry.trace = mock_trace
    cloudoptima.telemetry.JaegerExporter = mock_jaeger.JaegerExporter
    cloudoptima.telemetry.Resource = mock_resources.Resource
    cloudoptima.telemetry.SERVICE_NAME = "service.name"
    cloudoptima.telemetry.TracerProvider = mock_sdk_trace.TracerProvider
    cloudoptima.telemetry.BatchSpanProcessor = mock_sdk_export.BatchSpanProcessor
    
    try:
        mock_tracer = MagicMock()
        mock_trace.get_tracer.return_value = mock_tracer
        mock_trace.set_tracer_provider = MagicMock()
        tracer = cloudoptima.telemetry.init_tracer("test_service")
        assert mock_trace.set_tracer_provider.called
        assert mock_trace.get_tracer.called
    finally:
        cloudoptima.telemetry._OTEL_AVAILABLE = old_avail


def test_telemetry_jaeger_exception():
    """Test telemetry fallback when Jaeger exporter throws an exception."""
    mock_trace = MagicMock()
    mock_jaeger = MagicMock()
    mock_resources = MagicMock()
    mock_sdk_trace = MagicMock()
    mock_sdk_export = MagicMock()
    
    old_avail = cloudoptima.telemetry._OTEL_AVAILABLE
    cloudoptima.telemetry._OTEL_AVAILABLE = True
    
    cloudoptima.telemetry.trace = mock_trace
    mock_jaeger.JaegerExporter.side_effect = Exception("Jaeger down")
    
    cloudoptima.telemetry.JaegerExporter = mock_jaeger.JaegerExporter
    cloudoptima.telemetry.Resource = mock_resources.Resource
    cloudoptima.telemetry.SERVICE_NAME = "service.name"
    cloudoptima.telemetry.TracerProvider = mock_sdk_trace.TracerProvider
    cloudoptima.telemetry.BatchSpanProcessor = mock_sdk_export.BatchSpanProcessor
    
    try:
        tracer = cloudoptima.telemetry.init_tracer("test_service")
        assert mock_trace.NoOpTracer.called
    finally:
        cloudoptima.telemetry._OTEL_AVAILABLE = old_avail
