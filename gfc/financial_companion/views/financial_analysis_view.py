from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from financial_companion.helpers import functions
from financial_companion.helpers.enums import Timespan 
from financial_companion.models import Transaction, Category, User
from decimal import Decimal
from datetime import datetime
from ..models import Transaction
from json import dumps

@login_required
def spending_summary(request: HttpRequest) -> HttpResponse:
    total = Transaction.calculate_total(Transaction.get_transactions_from_time_period(Timespan.WEEK, request.user))
    categories = Transaction.get_category_splits(Transaction.get_transactions_from_time_period(Timespan.WEEK, request.user))
    percentages = functions.calculate_percentages(categories, total)
    percentages_list = list(percentages.values())
    labels =list(percentages.keys())
    return render(request, "pages/spending_summary.html", {'keyset': labels, 'dataset': percentages_list})