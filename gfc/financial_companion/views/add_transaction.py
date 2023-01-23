from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from financial_companion.forms import AddTransactionForm

def add_transaction_view(request: HttpRequest) -> HttpResponse:
    """View to record a transaction made"""

    if request.method == 'POST':
        form = AddTransactionForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('dashboard')
    else:
        form = AddTransactionForm()
    return render(request, "pages/add_transaction.html", {'form': form})
