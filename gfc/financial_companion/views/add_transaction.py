from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from financial_companion.forms import AddTransactionForm, AddTransactionsViaBankStatementForm
from financial_companion.models import Transaction, User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages


@login_required
def add_transaction_view(request: HttpRequest) -> HttpResponse:
    """View to record a transaction"""

    user: User = request.user
    if request.method == 'POST':
        form: AddTransactionForm = AddTransactionForm(
            user, request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                "Your transaction has been successfully added")
            return redirect('view_transactions', filter_type="all")
    else:
        form: AddTransactionForm = AddTransactionForm(user)
    return render(request, "pages/add_transaction.html",
                  {'form': form, 'edit': False})


@login_required
def edit_transaction_view(request: HttpRequest, pk) -> HttpResponse:
    """View to edit a transaction"""
    try:
        transaction: Transaction = Transaction.objects.get(id=pk)
        user: User = request.user
        if (transaction.receiver_account.user !=
                user and transaction.sender_account.user != user):
            return redirect('view_transactions', filter_type="all")
    except ObjectDoesNotExist:
        messages.add_message(
            request,
            messages.ERROR,
            "This transaction cannot be edited.")
        return redirect('view_transactions', filter_type="all")

    if request.method == 'POST':
        form: AddTransactionForm = AddTransactionForm(
            user, request.POST, request.FILES, instance=transaction)
        if form.is_valid():
            form.save(instance=transaction)
            messages.add_message(
                request,
                messages.SUCCESS,
                "This transaction has been successfully updated")
            return redirect('individual_transaction', pk=pk)
    else:
        form: AddTransactionForm = AddTransactionForm(
            user, instance=transaction)
    return render(request, "pages/add_transaction.html",
                  {'form': form, 'edit': True, 'pk': pk})


@login_required
def delete_transaction_view(request: HttpRequest, pk) -> HttpResponse:
    """View to delete a transaction"""
    try:
        transaction: Transaction = Transaction.objects.get(id=pk)
    except ObjectDoesNotExist:
        return redirect('dashboard')
    else:
        transaction.delete()
        messages.add_message(
            request,
            messages.WARNING,
            "The transaction has been deleted")
        return redirect('view_transactions', filter_type="all")


@login_required
def add_transactions_via_bank_statement(request: HttpRequest) -> HttpResponse:
    """View to add transactions via uploading a bank statement"""
    user: User = request.user

    if request.method == 'POST':
        form: AddTransactionsViaBankStatementForm = AddTransactionsViaBankStatementForm(
            request.POST, request.FILES, user=user)
        if form.is_valid():
            try:
                transactions: list[Transaction] = form.save()
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    f"{len(transactions)} new transactions added"
                )
                return redirect('view_transactions_redirect')
            except Exception:
                messages.add_message(
                    request,
                    messages.ERROR,
                    "Error scanning document, please ensure it is a valid bank statement"
                )
    else:
        form: AddTransactionsViaBankStatementForm = AddTransactionsViaBankStatementForm(
            user=user)
    return render(request, "pages/add_transactions_via_bank_statement_form.html",
                  {
                      'form': form
                  }
                  )
