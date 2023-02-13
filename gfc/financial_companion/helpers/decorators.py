"""Custom django decorators"""
from django.conf import settings
from django.shortcuts import redirect

def offline_required(view_function):
    """
    Decorator to require a user to be signed out to access this view.
    """

    def modified_function(request):
        if request.user.is_authenticated:
            return redirect(settings.LOGGED_IN_URL)
        else:
            return view_function(request)

    return modified_function