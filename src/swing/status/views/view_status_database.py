from django.db import connections
from django.db.utils import OperationalError
from django.http import HttpRequest, JsonResponse


def database_status(request: HttpRequest) -> JsonResponse:
    db_conn = connections["default"]
    try:
        db_conn.cursor()
        return JsonResponse({"status": "OK", "message": "Database is operational"})
    except OperationalError:
        return JsonResponse({"status": "ERROR", "message": "Database is down"})
