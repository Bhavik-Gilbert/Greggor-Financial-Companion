from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from ..models import RecurringTransaction
from financial_companion.helpers import paginate


@login_required
def individual_recurring_transaction_view(request: HttpRequest, pk: int) -> HttpResponse:
    """View to see information on individual recurring transactions"""
    try:
        transaction: RecurringTransaction = RecurringTransaction.objects.get(id=pk)
        user = request.user
        # TODO: Add once changes to account are added
        # if(transaction.receiver_account.user != user and transaction.sender_account.user != user):
        #     return redirect("dashboard")
    except RecurringTransaction.DoesNotExist:
        return redirect("dashboard")
    else:
        transactionslist = paginate(request.GET.get('page', 1), transaction.transactions.all(), 9)
        return render(request, "pages/individual_recurring_transaction.html",
                      {"transaction": transaction, "transactionslist": transactionslist})
