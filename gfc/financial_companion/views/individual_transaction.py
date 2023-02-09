from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.urls import reverse
from django.conf import settings
from ..models import Transaction, User


@login_required
def individual_transaction_view(request: HttpRequest, pk: int) -> HttpResponse:
    """View to see information on individual transactions"""
    try:
        transaction: Transaction = Transaction.objects.get(id=pk)
    except Transaction.DoesNotExist:
        return redirect("dashboard")
    else:
        return render(request, "pages/individual_transaction.html",
                      {"transaction": transaction})
