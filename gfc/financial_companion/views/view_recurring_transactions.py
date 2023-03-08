from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from ..models import Transaction, User, RecurringTransaction
from financial_companion.helpers import TransactionType
from django.http import HttpRequest, HttpResponse
from django.urls import reverse
from financial_companion.helpers import paginate


@login_required
def view_users_recurring_transactions(request: HttpRequest) -> HttpResponse:
    user: User = request.user

    transactions: list[RecurringTransaction] = user.get_user_recurring_transactions()

    list_of_transactions = paginate(request.GET.get('page', 1), transactions)

    return render(request, "pages/view_recurring_transactions.html",
                  {'transactions': list_of_transactions})

@login_required
def filter_recurring_transaction_request(request, redirect_name: str):
    if 'inactive' in request.POST:
        return redirect(reverse(redirect_name, kwargs={'filter_type': "inactive"}))
    elif 'active' in request.POST:
        return redirect(reverse(redirect_name, kwargs={
                        'filter_type': "active"}))
    elif 'all' in request.POST:
        return redirect(reverse(redirect_name, kwargs={'filter_type': "all"}))
    else:
        return redirect('dashboard')


