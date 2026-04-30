
from django.shortcuts import render

def status_dashboard(request):
    return render(request, 'swing_status/status.html')