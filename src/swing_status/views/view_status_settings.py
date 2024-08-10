from django.conf import settings
from django.http import JsonResponse

def settings_check(request):
    essential_settings = ['DEBUG', 'DATABASES', 'CACHES', 'ALLOWED_HOSTS']
    missing_settings = [s for s in essential_settings if not hasattr(settings, s)]
    
    if missing_settings:
        return JsonResponse({'status': 'ERROR', 'message': f'Missing essential settings: {", ".join(missing_settings)}'})
    else:
        return JsonResponse({'status': 'OK', 'message': 'All essential settings are configured'})