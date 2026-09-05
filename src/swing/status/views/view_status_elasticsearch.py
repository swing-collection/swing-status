from django.conf import settings
from django.http import HttpRequest, JsonResponse


def elasticsearch_status(request: HttpRequest) -> JsonResponse:
    try:
        # Import | Libraries
        from elasticsearch import Elasticsearch
    except ImportError as exc:
        return JsonResponse(
            {
                "status": "ERROR",
                "message": f"Elasticsearch integration unavailable: {exc}",
            },
            status=503,
        )

    es = Elasticsearch(
        [{"host": settings.ELASTICSEARCH_HOST, "port": settings.ELASTICSEARCH_PORT}]
    )
    if es.ping():
        return JsonResponse({"status": "OK", "message": "Elasticsearch is operational"})
    else:
        return JsonResponse({"status": "ERROR", "message": "Elasticsearch is down"})
