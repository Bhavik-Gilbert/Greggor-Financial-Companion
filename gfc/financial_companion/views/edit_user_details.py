from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..forms import EditUserDetailsForm
from ..models import User
from django.http import HttpResponse


@login_required
def edit_user_details_view(request) -> HttpResponse:
    """View to edit user profile details"""
    user: User = User.objects.get(id=request.user.id)
    if request.method == "POST":
        form: EditUserDetailsForm = EditUserDetailsForm(
            request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                "Your profile has been successfully updated!")
            return redirect('profile')

        else:
            return redirect('edit_user_details')
    else:
        form: EditUserDetailsForm = EditUserDetailsForm(instance=user)
        return render(request, 'pages/edit_user_details.html', {'form': form})
