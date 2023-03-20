from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..helpers import get_data_for_account_projection
from django.http import HttpRequest, HttpResponse


@login_required
def view_savings_accounts(request: HttpRequest) -> HttpResponse:
    """View to see all the user's saving's accounts"""
    context: dict[str, any] = get_data_for_account_projection(request.user)

    return render(request, "pages/view_savings_accounts.html", context)
