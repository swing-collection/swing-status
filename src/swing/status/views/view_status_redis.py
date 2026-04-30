import redis
from django.conf import settings
from django.http import JsonResponse

def redis_status(request):
    try:
        r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)
        r.ping()
        return JsonResponse({'status': 'OK', 'message': 'Redis is operational'})
    except redis.ConnectionError:
        return JsonResponse({'status': 'ERROR', 'message': 'Redis is down'})