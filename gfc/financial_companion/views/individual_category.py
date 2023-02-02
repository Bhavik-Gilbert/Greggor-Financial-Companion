from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from ..models import Category, Transaction, User, CategoryTarget, PotAccount

@login_required
def individual_category_view(request: HttpRequest, pk: int, filter_type: str) -> HttpResponse:
    """View to see information on individual categories"""
    user: User = request.user
    user_accounts = PotAccount.objects.filter(user = user.id)

    try:
        category: Category = Category.objects.get(id=pk, user=user)
    except Category.DoesNotExist:
        return redirect("dashboard")

    category_targets: CategoryTarget = CategoryTarget.objects.filter(category=category)

    transactions: list[Transaction] = []
    category_transactions: list[Transaction] = Transaction.objects.filter(category=category)

    filter_send_types = ["sent", "all"]
    filter_receive_types = ["all", "received"]
    
    if not(filter_type in filter_send_types or filter_type in filter_receive_types):
        return redirect('dashboard')

    for account in user_accounts:
        if filter_type in filter_send_types:
            transactions = [*transactions, *Transaction.objects.filter(sender_account=account)]
        if filter_type in filter_receive_types:
            transactions = [*transactions, *Transaction.objects.filter(receiver_account=account)]
    
    # print([*set(transactions) & set(category_transactions)])
    transactions = list(set(transactions) & set(category_transactions))

    page: HttpRequest = request.GET.get('page', settings.NUMBER_OF_TRANSACTIONS)
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
def individual_category_redirect(request: HttpRequest, pk: int) -> HttpResponse:
    """View to redirect to see information on individual categories with base inputs"""

    return redirect('individual_category', pk=pk, filter_type="all")