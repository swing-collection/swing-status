from django.http import JsonResponse

def memory_usage_status(request):
    try:
        import psutil
    except ImportError as exc:
        return JsonResponse({'status': 'ERROR', 'message': f'Memory integration unavailable: {exc}'}, status=503)

    memory = psutil.virtual_memory()
    free_memory = memory.available / (1024 ** 3)
    
    if free_memory < 1:  # Trigger an alert if available memory is below 1GB
        return JsonResponse({'status': 'WARNING', 'message': f'Low memory: {free_memory:.2f} GB available'})
    else:
        return JsonResponse({'status': 'OK', 'message': f'Enough memory: {free_memory:.2f} GB available'})