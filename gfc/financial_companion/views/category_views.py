from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from ..models import Category
from django.contrib.auth.decorators import login_required
from django.urls import reverse


@login_required     
def category_list_view(request: HttpRequest, search_name: str) -> HttpResponse:
    """View to view list of all existing categories"""

    if(search_name == 'all' or search_name == ''):
        categories = Category.objects.filter(user = request.user)
    else:
        categories = Category.objects.filter(user = request.user ).filter(name__icontains = search_name)

    return render(request, "pages/category_list.html", {"categories": categories})

@login_required
def filter_categories_request(request: HttpRequest):
    if request.method == 'POST':
        search_id  = request.POST.get('textfield', None)
        if(search_id == ''):
            return redirect(reverse('categories_list', kwargs={'search_name': "all"}))
        else:
            try:
                categories = Category.objects.filter(user_id = request.user ).filter(name__icontains = search_id)
                return redirect(reverse('categories_list', kwargs={'search_name': search_id}))
            except Category.DoesNotExist:
                return redirect(reverse('categories_list', kwargs={'search_name': "all"})) 

    