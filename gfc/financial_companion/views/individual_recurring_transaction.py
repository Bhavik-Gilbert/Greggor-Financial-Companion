from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.urls import reverse
from django.conf import settings
from ..models import RecurringTransaction
from financial_companion.helpers import paginate


@login_required
def individual_recurring_transaction_view(request: HttpRequest, pk: int) -> HttpResponse:
    """View to see information on individual recurring transactions"""
    try:
        transaction: RecurringTransaction = RecurringTransaction.objects.get(id=pk)
    except RecurringTransaction.DoesNotExist:
        return redirect("dashboard")
    else:
        transactionslist= paginate(request.GET.get('page', 1), transaction.transactions.all())
        return render(request, "pages/individual_recurring_transaction.html",
                      {"transaction": transaction, "transactionslist": transactionslist})
