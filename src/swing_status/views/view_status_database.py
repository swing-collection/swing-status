from django.http import JsonResponse
from django.db import connections
from django.db.utils import OperationalError

def database_status(request):
    db_conn = connections['default']
    try:
        db_conn.cursor()
        return JsonResponse({'status': 'OK', 'message': 'Database is operational'})
    except OperationalError:
        return JsonResponse({'status': 'ERROR', 'message': 'Database is down'})