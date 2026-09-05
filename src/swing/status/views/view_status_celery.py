from django.http import HttpRequest, JsonResponse


def celery_status(request: HttpRequest) -> JsonResponse:
    try:
        # Import | Libraries
        from celery import current_app
        from celery.result import AsyncResult
    except ImportError as exc:
        return JsonResponse(
            {"status": "ERROR", "message": f"Celery integration unavailable: {exc}"},
            status=503,
        )

    result = AsyncResult("some-task-id", app=current_app)

    if result.ready():
        return JsonResponse({"status": "OK", "message": "Celery is operational"})
    else:
        return JsonResponse({"status": "ERROR", "message": "Celery is not responding"})
