from elasticsearch import Elasticsearch
from django.conf import settings
from django.http import JsonResponse

def elasticsearch_status(request):
    es = Elasticsearch([{'host': settings.ELASTICSEARCH_HOST, 'port': settings.ELASTICSEARCH_PORT}])
    if es.ping():
        return JsonResponse({'status': 'OK', 'message': 'Elasticsearch is operational'})
    else:
        return JsonResponse({'status': 'ERROR', 'message': 'Elasticsearch is down'})