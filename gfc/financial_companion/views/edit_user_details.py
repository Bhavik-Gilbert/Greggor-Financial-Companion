from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django import forms

from ..forms import EditUserDetailsForm
from ..models import User


@login_required
def edit_user_details_view(request):
    user = User.objects.get(id=request.user.id)
    if request.method == "POST":
        form = EditUserDetailsForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
        else:
            return redirect('edit_user_details')
    else:
        form = EditUserDetailsForm(instance=user)
        return render(request, 'pages/edit_user_details.html', {'form': form})
