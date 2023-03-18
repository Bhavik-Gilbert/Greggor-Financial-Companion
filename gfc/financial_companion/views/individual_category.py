from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from financial_companion.helpers import paginate
from ..models import Category, Transaction, User, CategoryTarget
from financial_companion.helpers import FilterTransactionType
from django.core.paginator import Page


@login_required
def individual_category_view(
        request: HttpRequest, pk: int, filter_type: str = FilterTransactionType.ALL) -> HttpResponse:
    """View to see information on individual categories"""
    user: User = request.user

    try:
        category: Category = Category.objects.get(id=pk, user=user)
    except Category.DoesNotExist:
        return redirect("dashboard")

    category_targets: CategoryTarget = CategoryTarget.objects.filter(
        category=category).filter()

    if not (filter_type in FilterTransactionType.get_send_list()
            or filter_type in FilterTransactionType.get_received_list()):
        return redirect('dashboard')

    transactions: list[Transaction] = category.get_category_transactions(
        filter_type)

    list_of_transactions: Page = paginate(
        request.GET.get('page', 1), transactions)

    return render(request, "pages/individual_category.html", {
        "category": category,
        "category_targets": category_targets,
        "transactions": list_of_transactions
    })
