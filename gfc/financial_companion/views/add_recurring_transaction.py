from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from financial_companion.forms import AddRecurringTransactionForm, EditRecurringTransactionForm
from financial_companion.models import Transaction, PotAccount, BankAccount, Account, Category, User, RecurringTransaction
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from typing import Any


@login_required
def add_recurring_transaction_view(request: HttpRequest) -> HttpResponse:
    """View to record a recurring transaction"""

    user = request.user
    categories = Category.objects.filter(user=user.id)

    if request.method == 'POST':
        form = AddRecurringTransactionForm(user, request.POST, request.FILES)
        form.fields['category'].queryset = categories
        if form.is_valid():
            form.save()
            messages.add_message(
            request,
            messages.WARNING,
            "New recurring transaction has been added.")
            return redirect('view_recurring_transactions')
    else:
        form = AddRecurringTransactionForm(user)
        form.fields['category'].queryset = categories
    return render(request, "pages/add_recurring_transaction.html",
                  {'form': form, 'edit': False})


@login_required
def edit_recurring_transaction_view(request: HttpRequest, pk) -> HttpResponse:
    try:
        transaction = RecurringTransaction.objects.get(id=pk)
    except ObjectDoesNotExist:
        return redirect('view_recurring_transactions')
    else:
        user = request.user
        categories = Category.objects.filter(user=user.id)
        if request.method == 'POST':
            form = EditRecurringTransactionForm(
                user, request.POST, request.FILES, instance=transaction)
            form.fields['category'].queryset = categories
            if form.is_valid():
                form.save(instance=transaction)
                messages.add_message(
                request,
                messages.WARNING,
                "The recurring transaction has been updated")
                return redirect('view_recurring_transactions')
        form = EditRecurringTransactionForm(user, instance=transaction)
        form.fields['category'].queryset = categories
        return render(request, "pages/add_recurring_transaction.html",
                      {'form': form, 'edit': True, 'pk': pk})


@login_required
def delete_recurring_transaction_view(request: HttpRequest, pk) -> HttpResponse:
    try:
        transaction = RecurringTransaction.objects.get(id=pk)
    except ObjectDoesNotExist:
        return redirect('dashboard')
    else:
        transaction.delete()
        messages.add_message(
            request,
            messages.WARNING,
            "The recurring transaction has been deleted")
        return redirect('dashboard')

