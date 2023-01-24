from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login

from ..helpers import offline_required
from financial_companion.forms import UserSignUpForm

@offline_required
def sign_up_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserSignUpForm()
    return render(request, "pages/sign_up.html", {'form': form})
