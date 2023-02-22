from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from ..models import User
from django.contrib import messages


@login_required
def profile_view(request: HttpRequest) -> HttpResponse:
    user = request.user
    return render(request, 'pages/profile.html')

@login_required
def delete_profile_view(request: HttpRequest) -> HttpResponse:
    try:
        user = User.objects.get(id=request.user.id)
    except ObjectDoesNotExist:
        return redirect('dashboard')
    else:
        user.delete()
        messages.add_message(
            request,
            messages.WARNING,
            "Your profile has been deleted")
        return redirect('log_out')
