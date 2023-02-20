from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from financial_companion.forms import AddTransactionForm
from ..models import Transaction, PotAccount, BankAccount, Account, Category
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

@login_required
def add_transaction_view(request: HttpRequest) -> HttpResponse:
    """View to record a transaction made"""

    user = request.user
    user_accounts = []
    user_accounts = PotAccount.objects.filter(user = user.id)
    sent_or_received_accounts= set()
    ids = []
    ids2 = set()
    transactions = set()

    for account in user_accounts:
        transactions.update(Transaction.objects.filter(sender_account=account))
        transactions.update(Transaction.objects.filter(receiver_account=account))
        sent_or_received_accounts.add(account)
        ids.append(account.id)

    for transaction in transactions:
        ids2.add(transaction.sender_account.id)
        ids2.add(transaction.receiver_account.id)
        if ids.count(transaction.sender_account.id) == 0:
            sent_or_received_accounts.add(transaction.sender_account)
        if ids.count(transaction.receiver_account.id) == 0:
            sent_or_received_accounts.add(transaction.receiver_account)

    categories = Category.objects.filter(user = user.id)

    if request.method == 'POST':
        form = AddTransactionForm(request.POST, request.FILES)
        form.fields['category'].queryset = categories
        form.fields['sender_account'].queryset = user_accounts
        # form.fields['receiver_account'].queryset = user_accounts
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = AddTransactionForm()
        form.fields['category'].queryset = categories
        form.fields['sender_account'].queryset = user_accounts
        # form.fields['receiver_account'].queryset = user_accounts
    return render(request, "pages/add_transaction.html", {'form': form, 'edit': False, 'sent_or_received_accounts': sent_or_received_accounts, 'categories': categories})

@login_required
def edit_transaction_view(request: HttpRequest, pk) -> HttpResponse:
    try:
        transaction = Transaction.objects.get(id=pk)
    except ObjectDoesNotExist:
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            print(request.POST)
            form = AddTransactionForm(request.POST,request.FILES, instance=transaction)
            if form.is_valid():
                form.save(instance=transaction)
                return redirect('dashboard')
        form = AddTransactionForm(instance=transaction)
        return render(request, "pages/add_transaction.html", {'form': form, 'edit': True, 'pk':pk})

@login_required
def delete_transaction_view(request: HttpRequest, pk) -> HttpResponse:
    try:
        transaction = Transaction.objects.get(id=pk)
    except ObjectDoesNotExist:
        return redirect('dashboard')
    else:
        transaction.delete()
        messages.add_message(request, messages.WARNING, "The transaction has been deleted")
        return redirect('dashboard')
