from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from ..models import Transaction, User, RecurringTransaction
from financial_companion.helpers import TransactionType
from django.http import HttpRequest, HttpResponse
from django.urls import reverse
from financial_companion.helpers import paginate


@login_required
def view_users_recurring_transactions(request: HttpRequest,
                            filter_type= str('all')) -> HttpResponse:
    user: User = request.user

    if not (filter_type in TransactionType.get_send_list()
            or filter_type in TransactionType.get_received_list()):
        return redirect('dashboard')

    transactions: list[RecurringTransaction] = user.get_user_recurring_transactions()

    list_of_transactions = paginate(request.GET.get('page', 1), transactions)

    return render(request, "pages/view_recurring_transactions.html",
                  {'transactions': list_of_transactions})

