import requests
from django.http import JsonResponse

def external_api_status(request):
    url = "https://api.example.com/health"  # Replace with the actual API endpoint
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return JsonResponse({'status': 'OK', 'message': 'External API is operational'})
        else:
            return JsonResponse({'status': 'ERROR', 'message': 'External API is down or not responding correctly'})
    except requests.exceptions.RequestException as e:
        return JsonResponse({'status': 'ERROR', 'message': f'External API error: {str(e)}'})