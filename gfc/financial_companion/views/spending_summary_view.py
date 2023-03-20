from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from financial_companion.helpers import functions, paginate
from financial_companion.helpers.enums import Timespan
from financial_companion.models import Transaction
from financial_companion.forms import TimespanOptionsForm
from ..models import Transaction
from json import dumps
from django.core.paginator import Page


@login_required
def spending_summary(request: HttpRequest) -> HttpResponse:
    time: Timespan = Timespan.DAY
    user: User = request.user
    if request.method == "POST":
        form: TimespanOptionsForm = TimespanOptionsForm(request.POST)
        if form.is_valid():
            time: str = form.get_choice()
    total_spent: int = sum(transaction.amount for transaction in
                           Transaction.get_transactions_from_time_period(
                               time, request.user, "sent"))
    total_received: int = sum(transaction.amount for transaction in
                              Transaction.get_transactions_from_time_period(
                                  time, request.user, "received"))
    categories: dict[str, float] = Transaction.get_category_splits(
        Transaction.get_transactions_from_time_period(
            time, request.user, "sent"), user)
    percentages: dict[str, float] = functions.calculate_percentages(
        categories, total_spent)
    percentages_list: list[float] = list(percentages.values())
    labels: list[str] = list(percentages.keys())
    form: TimespanOptionsForm = TimespanOptionsForm()
    if percentages_list == []:
        percentages_list: list[float] = None
    targets: list[AbstractTarget] = list(
        filter(
            lambda target: time == target.timespan,
            request.user.get_all_targets()))
    list_of_targets: Page = paginate(request.GET.get('page', 1), targets)
    return render(request, "pages/spending_summary.html", {'keyset': labels, 'dataset': percentages_list,
                  'form': form, 'money_in': total_received, 'money_out': total_spent, 'time': str(time).capitalize(), 'targets': list_of_targets})
