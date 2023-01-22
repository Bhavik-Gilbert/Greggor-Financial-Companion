from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from ..helpers.decorators import offline_required

@offline_required
def home_view(request: HttpRequest) -> HttpResponse:
    """View for home page"""
    return render(request, "pages/index.html")
