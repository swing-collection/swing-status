from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def status_dashboard(request: HttpRequest) -> HttpResponse:
    return render(request, "swing/status/status.html")
