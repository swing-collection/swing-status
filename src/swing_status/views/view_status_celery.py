from django.http import JsonResponse
from celery.result import AsyncResult
from swing_status.celery import app  # Assuming you have a celery app setup

def celery_status(request):

    result = AsyncResult('some-task-id', app=app)

    if result.ready():
        return JsonResponse({'status': 'OK', 'message': 'Celery is operational'})
    else:
        return JsonResponse({'status': 'ERROR', 'message': 'Celery is not responding'})