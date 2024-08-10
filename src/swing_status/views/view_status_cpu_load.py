import psutil
from django.http import JsonResponse

def cpu_load_status(request):
    load = psutil.cpu_percent(interval=1)
    
    if load > 80:  # Trigger an alert if CPU load is above 80%
        return JsonResponse({'status': 'WARNING', 'message': f'High CPU load: {load:.2f}%'})
    else:
        return JsonResponse({'status': 'OK', 'message': f'CPU load is normal: {load:.2f}%'})