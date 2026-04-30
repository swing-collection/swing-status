from django.urls import path
from .views import database_status, celery_status

urlpatterns = [
    path('status/dashboard/', status_dashboard, name='status_dashboard'),
    path('status/database/', database_status, name='database_status'),
    path('status/celery/', celery_status, name='celery_status'),
]

from django.urls import path
from .views import (
    database_status, celery_status, redis_status, elasticsearch_status,
    external_api_status, disk_space_status, memory_usage_status, 
    cpu_load_status, settings_check, email_server_status
)

urlpatterns = [
    path('status/database/', database_status, name='database_status'),
    path('status/celery/', celery_status, name='celery_status'),
    path('status/redis/', redis_status, name='redis_status'),
    path('status/elasticsearch/', elasticsearch_status, name='elasticsearch_status'),
    path('status/external-api/', external_api_status, name='external_api_status'),
    path('status/disk-space/', disk_space_status, name='disk_space_status'),
    path('status/memory-usage/', memory_usage_status, name='memory_usage_status'),
    path('status/cpu-load/', cpu_load_status, name='cpu_load_status'),
    path('status/settings/', settings_check, name='settings_check'),
    path('status/email-server/', email_server_status, name='email_server_status'),
]