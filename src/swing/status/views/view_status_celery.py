from django.http import JsonResponse

def celery_status(request):
    try:
        from celery.result import AsyncResult
        from swing_status.celery import app  # Assuming you have a celery app setup
    except ImportError as exc:
        return JsonResponse({'status': 'ERROR', 'message': f'Celery integration unavailable: {exc}'}, status=503)

    result = AsyncResult('some-task-id', app=app)

    if result.ready():
        return JsonResponse({'status': 'OK', 'message': 'Celery is operational'})
    else:
        return JsonResponse({'status': 'ERROR', 'message': 'Celery is not responding'})