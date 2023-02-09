from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from ..models import Category, Transaction, User, CategoryTarget, PotAccount
from financial_companion.helpers import TransactionType


@login_required
def individual_category_view(
        request: HttpRequest, pk: int, filter_type: str) -> HttpResponse:
    """View to see information on individual categories"""
    user: User = request.user

    try:
        category: Category = Category.objects.get(id=pk, user=user)
    except Category.DoesNotExist:
        return redirect("dashboard")

    category_targets: CategoryTarget = CategoryTarget.objects.filter(
        category=category)

    if not (filter_type in TransactionType.get_send_list()
            or filter_type in TransactionType.get_received_list()):
        return redirect('dashboard')

    transactions: list[Transaction] = category.get_category_transactions(
        filter_type)

    page: HttpRequest = request.GET.get(
        'page', settings.NUMBER_OF_TRANSACTIONS)
    paginator: Paginator = Paginator(transactions, 10)
    try:
        list_of_transactions: list[Paginator] = paginator.page(page)
    except PageNotAnInteger:
        list_of_transactions = paginator.page(1)
    except EmptyPage:
        list_of_transactions = paginator.page(paginator.num_pages)

    return render(request, "pages/individual_category.html", {
        "category": category,
        "category_targets": category_targets,
        "transactions": list_of_transactions
    })


@login_required
def individual_category_redirect(
        request: HttpRequest, pk: int) -> HttpResponse:
    """View to redirect to see information on individual categories with base inputs"""

    return redirect('individual_category', pk=pk, filter_type="all")
