from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from ..models import Category
from django.contrib.auth.decorators import login_required

@login_required     
def category_list_view(request: HttpRequest) -> HttpResponse:
    """View to view list of all existing categories"""

    categories = Category.objects.filter(user_id = request.user)
    return render(request, "pages/category_list.html", {"categories": categories})

