from django.http import HttpRequest, JsonResponse


def cpu_load_status(request: HttpRequest) -> JsonResponse:
    try:
        # Import | Libraries
        import psutil
    except ImportError as exc:
        return JsonResponse(
            {"status": "ERROR", "message": f"CPU integration unavailable: {exc}"},
            status=503,
        )

    load = psutil.cpu_percent(interval=1)

    if load > 80:  # Trigger an alert if CPU load is above 80%
        return JsonResponse(
            {"status": "WARNING", "message": f"High CPU load: {load:.2f}%"}
        )
    else:
        return JsonResponse(
            {"status": "OK", "message": f"CPU load is normal: {load:.2f}%"}
        )
