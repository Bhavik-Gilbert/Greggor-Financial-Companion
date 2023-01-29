from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django import forms

from ..forms import EditUserDetailsForm
from ..models import User

@login_required
def edit_user_details(request: HttpRequest) -> HttpResponse:
    try:
        user = User.objects.get(id=request.user.id)
    except ObjectDoesNotExist:
        return redirect('log_in')
    if request.method == "POST":
        form = EditUserDetailsForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            request.user.save()
            return redirect('dashboard')
    else:
        form = EditUserDetailsForm(instance=user)
        return render(request, 'pages/edit_user_details.html', {'form': form})
