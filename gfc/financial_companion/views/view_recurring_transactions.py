from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from ..models import Transaction, User, RecurringTransaction
from financial_companion.helpers import TransactionType
from django.http import HttpRequest, HttpResponse
from django.urls import reverse
from financial_companion.helpers import paginate
from django.core.paginator import Page

@login_required
def view_users_recurring_transactions(request: HttpRequest) -> HttpResponse:
    """View to see a list of the user's recurring transactions"""
    user: User = request.user

    transactions: list[RecurringTransaction] = user.get_user_recurring_transactions()

    list_of_transactions: Page = paginate(request.GET.get('page', 1), transactions)

    return render(request, "pages/view_recurring_transactions.html",
                  {'transactions': list_of_transactions})
