from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from financial_companion.forms import UserSignUpForm

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
