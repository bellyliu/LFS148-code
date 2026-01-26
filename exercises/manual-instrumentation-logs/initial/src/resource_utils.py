# Add resource attributes
from opentelemetry.sdk.resources import Resource
from opentelemetry.semconv.resource import ResourceAttributes

def create_resource(name: str, version: str) -> Resource:
    svc_resource = Resource.create(
        {
            ResourceAttributes.SERVICE_NAME: name,
            ResourceAttributes.SERVICE_VERSION: version,
            "service.maintainer": "dbl",
            "k8s.pod_name": "pod-2131xasdf5",
            "k8s.cluster": "prod-sg-eks"
        }
    )
    return svc_resource