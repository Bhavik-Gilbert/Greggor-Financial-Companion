from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from financial_companion.forms import UserGroupForm
from django.contrib.auth.decorators import login_required
from ..models import UserGroup
from django.contrib import messages


@login_required
def create_user_group_view(request: HttpRequest) -> HttpResponse:
    """View to allow users to create a user group"""
    if request.method == 'POST':
        form = UserGroupForm(request.POST, request.FILES)
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
        form = UserGroupForm()
    return render(request, "pages/create_user_group.html",
                  {'form': form, 'form_toggle': True})


@login_required
def delete_user_group_view(request: HttpRequest, pk: int) -> HttpResponse:
    """View to allow users to delete a user group"""
    # check is id valid
    try:
        current_user_group: UserGroup = UserGroup.objects.get(
            id=pk, owner_email=request.user.email)
    except Exception:
        messages.add_message(
            request,
            messages.WARNING,
            "Failed to delete user group")
        return redirect("all_groups_redirect")

    current_user_group.delete()
    messages.add_message(
        request,
        messages.WARNING,
        "This user group has been deleted")
    return redirect("all_groups_redirect")


@login_required
def edit_user_group_view(request: HttpRequest, pk: int) -> HttpResponse:
    """View to allow users to edit a user group"""
    # check is id valid
    try:
        current_user_group: UserGroup = UserGroup.objects.get(
            id=pk, owner_email=request.user.email)
    except Exception:
        messages.add_message(
            request,
            messages.WARNING,
            "You do not have permission to edit this user group")
        return redirect("all_groups_redirect")

    if request.method == "POST":
        form = UserGroupForm(
            request.POST,
            request.FILES,
            instance=current_user_group)
        if form.is_valid():
            form.save(current_user=request.user, instance=current_user_group)
            messages.add_message(
                request,
                messages.SUCCESS,
                "Successfully edited user group")
            return redirect('individual_group_redirect',
                            pk=current_user_group.id)
    else:
        form = UserGroupForm(instance=current_user_group)

    return render(request, "pages/create_user_group.html",
                  {'form': form, 'form_toggle': False, 'pk': pk})
