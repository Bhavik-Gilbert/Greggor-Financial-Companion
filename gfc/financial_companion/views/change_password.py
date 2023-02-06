from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from financial_companion.forms import UserChangePasswordForm
from django.contrib.auth.decorators import login_required

@login_required
def change_password_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = UserChangePasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            new_password = form.cleaned_data.get('new_password')
            user = authenticate(username=request.user.username, password=password)
            if user is not None:
                form.save(instance=request.user)
                messages.add_message(request, messages.SUCCESS, "Password successfully changed")
                return redirect('dashboard')
        messages.add_message(request, messages.ERROR, "The password provided is incorrect")
    form = UserChangePasswordForm()
    return render(request, 'pages/change_password.html', {'form': form})
