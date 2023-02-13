from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from ..helpers import offline_required, GreggorTypes

@offline_required
def home_view(request: HttpRequest) -> HttpResponse:
    """View for home page"""

    return render(request, "pages/index.html", {"logo_types": [choice for choice in GreggorTypes]})
