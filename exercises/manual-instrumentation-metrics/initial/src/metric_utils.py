from opentelemetry.sdk.metrics.export import (
    ConsoleMetricExporter,
    PeriodicExportingMetricReader,
    MetricReader
)
from opentelemetry import metrics as metric_api
from opentelemetry.metrics import Counter, Histogram, ObservableGauge
from opentelemetry.sdk.metrics import MeterProvider

def create_metric_pipeline(export_interval: int) -> MetricReader:
    console_exporter = ConsoleMetricExporter()
    reader = PeriodicExportingMetricReader(
        exporter=console_exporter,
        export_interval_millis=export_interval
    )
    return reader

def create_meter(name: str, version: str) -> metric_api.Meter:
    # configure provider
    metric_reader = create_metric_pipeline(5000)
    provider = MeterProvider(
        metric_readers=[metric_reader]
    )

    # obtain meter
    metric_api.set_meter_provider(provider)
    meter = metric_api.get_meter(name, version)
    return meter

def create_request_instruments(meter: metric_api.Meter) -> dict[str, metric_api.Instrument]:
    index_counter = meter.create_counter(
        name="index_called",
        unit="request",
        description="Total amount request to /"
    )
    instruments = {
        "index_counter": index_counter
    }
    return instruments