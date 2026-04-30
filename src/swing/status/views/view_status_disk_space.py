import shutil
from django.http import JsonResponse

def disk_space_status(request):
    total, used, free = shutil.disk_usage("/")
    free_gb = free / (2**30)
    
    if free_gb < 5:  # Let's say we trigger an alert if free space is below 5GB
        return JsonResponse({'status': 'WARNING', 'message': f'Low disk space: {free_gb:.2f} GB remaining'})
    else:
        return JsonResponse({'status': 'OK', 'message': f'Enough disk space: {free_gb:.2f} GB remaining'})