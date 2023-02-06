from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

@login_required
def profile_view(request: HttpRequest) -> HttpResponse:
    try:
        user = request.user
        # print(user.profile_picture.url)
    except ObjectDoesNotExist:
        return redirect('dashboard')
    else:
        return render(request, 'pages/profile.html')
