from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
# from ..models import Group
from django.contrib.auth.decorators import login_required
from django.urls import reverse

@login_required
def all_groups_view(request: HttpRequest) -> HttpResponse:
    return render(request, "pages/all_groups.html", {"groups": None})
