from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

def home_view(request: HttpRequest) -> HttpResponse:
    """View for home page"""
    return render(request, "pages/index.html")