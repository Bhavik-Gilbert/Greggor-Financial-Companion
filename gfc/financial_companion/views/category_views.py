from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from ..models import Category
from django.contrib.auth.decorators import login_required
from django.urls import reverse


@login_required     
def category_list_view(request: HttpRequest, filter_type: str) -> HttpResponse:
    """View to view list of all existing categories"""

    if(filter_type == 'all'):
        categories = Category.objects.filter(user_id = request.user)
    else:
        categories = Category.objects.filter(user_id = request.user ).filter(name = filter_type)

    return render(request, "pages/category_list.html", {"categories": categories})

@login_required
def filter_categories_request(request: HttpRequest):
    if request.method == 'POST':
        search_id  = request.POST.get('textfield', None)
        try:
            categories = Category.objects.filter(user_id = request.user ).filter(name = search_id)
            return redirect(reverse('categories_list', kwargs={'filter_type': search_id}))
        except Category.DoesNotExist:
            return redirect(reverse('categories_list', kwargs={'filter_type': "all"})) 

    print(request.POST)

    