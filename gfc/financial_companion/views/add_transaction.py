from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from financial_companion.forms import AddTransactionForm
from ..models import Transaction
from django.contrib.auth.decorators import login_required

@login_required
def add_transaction_view(request: HttpRequest) -> HttpResponse:
    """View to record a transaction made"""

    if request.method == 'POST':
        form = AddTransactionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = AddTransactionForm()
    return render(request, "pages/add_transaction.html", {'form': form})
