from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from ..models import Category
        
def category_list_view(request: HttpRequest) -> HttpResponse:
    """View to view list of all existing categories"""

    categories = Category.objects.all
    return render(request, "pages/category_list.html", {"categories": categories})

