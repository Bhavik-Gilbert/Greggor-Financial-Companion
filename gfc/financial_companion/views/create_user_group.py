from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from financial_companion.forms import CreateUserGroupForm
from django.contrib.auth.decorators import login_required
from ..models import UserGroup
from django.contrib import messages


@login_required
def create_user_group_view(request: HttpRequest) -> HttpResponse:
    """View to allow users to create a user group"""
    if request.method == 'POST':
        form = CreateUserGroupForm(request.POST, request.FILES)
        if form.is_valid():
            user = request.user
            user_group: UserGroup = form.save(user)
            user_group.add_member(user)
            messages.add_message(
            request,
            messages.SUCCESS,
            "You have successfully made a group")
            return redirect('all_groups_redirect')
    else:
        form = CreateUserGroupForm()
    return render(request, "pages/create_user_group.html",
                  {'form': form })