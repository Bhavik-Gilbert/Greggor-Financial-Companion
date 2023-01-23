from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

def dashboard_view(request: HttpRequest) -> HttpResponse:
    return render(request, "pages/dashboard.html")
