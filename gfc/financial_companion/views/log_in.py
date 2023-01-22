from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from financial_companion.forms import UserLogInForm

def log_in_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = UserLogInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
        messages.add_message(request, messages.ERROR, "The credentials provided are invalid!")
    form = UserLogInForm()
    return render(request, 'pages/log_in.html', {'form': form})
