from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from financial_companion.helpers import functions, paginate
from financial_companion.helpers import TransactionType
from financial_companion.helpers.enums import Timespan
from financial_companion.models import Transaction, Category, User
from financial_companion.forms import TimespanOptionsForm
from decimal import Decimal
from datetime import datetime
from ..models import Transaction
from json import dumps


@login_required
def spending_summary(request: HttpRequest) -> HttpResponse:
    time = Timespan.DAY
    if request.method == "POST":
        form = TimespanOptionsForm(request.POST)
        if form.is_valid():
            time = form.get_choice()
    total_spent = Transaction.calculate_total(
        Transaction.get_transactions_from_time_period(
            time, request.user, "sent"))
    total_received = Transaction.calculate_total(
        Transaction.get_transactions_from_time_period(
            time, request.user, "received"))
    categories = Transaction.get_category_splits(
        Transaction.get_transactions_from_time_period(
            time, request.user, "sent"))
    percentages = functions.calculate_percentages(categories, total_spent)
    percentages_list = list(percentages.values())
    labels = list(percentages.keys())
    form = TimespanOptionsForm()
    if percentages_list == []:
        percentages_list = None
    targets = list(filter(lambda target: time == target.timespan, request.user.get_all_targets()))
    list_of_targets = paginate(request.GET.get('page', 1), targets)
    return render(request, "pages/spending_summary.html", {'keyset': labels, 'dataset': percentages_list,
                  'form': form, 'money_in': total_received, 'money_out': total_spent, 'time': str(time).capitalize(), 'targets': list_of_targets})
