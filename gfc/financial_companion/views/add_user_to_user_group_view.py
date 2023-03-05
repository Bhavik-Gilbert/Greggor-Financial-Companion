from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from financial_companion.forms import AddUserToUserGroupForm
from django.contrib.auth.decorators import login_required
from ..models import UserGroup, User

@login_required
def add_user_to_user_group_view(request: HttpRequest, group_pk: int) -> HttpResponse:
    if request.method == 'POST':
        form = AddUserToUserGroupForm(request.POST)
        try:
            current_user_group: UserGroup = UserGroup.objects.get(
                id=group_pk)
        except Exception:
            messages.add_message(
                request,
                messages.WARNING,
                "Failed to identify user group")
            return redirect("all_groups_redirect")
        if form.is_valid():
            user_email = form.cleaned_data.get('user_email')
            try:
                user: User = User.objects.get(
                    email=user_email)
            except Exception:
                messages.add_message(
                    request,
                    messages.WARNING,
                    "Failed to identify user")
                return redirect('individual_group',
                                    pk=current_user_group.id)
            
            if(not current_user_group.members.contains(user)):
                current_user_group.add_member(user)
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    "Successfully added user to user group")
                return redirect('individual_group',
                                    pk=current_user_group.id)
            else:
                messages.add_message(
                    request,
                    messages.WARNING,
                    "This user is currently a member of this group")
                return redirect('individual_group',
                                    pk=current_user_group.id)
        else:
            messages.add_message(
                    request,
                    messages.WARNING,
                    "Please enter a valid email address")
            return redirect('individual_group',
                                pk=current_user_group.id)
    else:
        return redirect('individual_group',
                                    pk=current_user_group.id)
            