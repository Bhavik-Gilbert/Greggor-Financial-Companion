from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from financial_companion.helpers import functions, paginate
from financial_companion.helpers.enums import (
    Timespan, FilterTransactionType,
    CurrencyType
)
from financial_companion.models import Transaction
from financial_companion.forms import TimespanCurrencyOptionsForm
from ..models import Transaction, User, AbstractTarget
from django.core.paginator import Page


@login_required
def spending_summary(request: HttpRequest,
                     time: Timespan = Timespan.DAY,
                     currency: CurrencyType = CurrencyType.GBP) -> HttpResponse:
    if time not in Timespan:
        return redirect("spending_summary")
    user: User = request.user
    form: TimespanCurrencyOptionsForm = TimespanCurrencyOptionsForm()
    if request.method == "POST":
        form: TimespanCurrencyOptionsForm = TimespanCurrencyOptionsForm(
            request.POST)
        if form.is_valid():
            time: str = form.get_timespan()
            currency: str = form.get_currency()
            return redirect("spending_summary", time=time, currency=currency)

    total_spent: float = Transaction.calculate_total_amount_from_transactions(
        Transaction.get_transactions_from_time_period(
            time, request.user, FilterTransactionType.SENT
        ), currency
    )
    total_received: float = Transaction.calculate_total_amount_from_transactions(
        Transaction.get_transactions_from_time_period(
            time, request.user, FilterTransactionType.RECEIVED
        ), currency
    )
    category_amounts: dict[str, float] = Transaction.get_category_splits(
        Transaction.get_transactions_from_time_period(
            time, request.user, FilterTransactionType.SENT), user)
    percentages: dict[str, float] = functions.calculate_split_percentages(
        category_amounts)
    percentages_list: list[float] = list(percentages.values())
    labels: list[str] = list(percentages.keys())
    if percentages_list == []:
        percentages_list: list[float] = None
    targets: list[AbstractTarget] = list(
        filter(
            lambda target: time == target.timespan,
            request.user.get_all_targets()))
    list_of_targets: Page = paginate(request.GET.get('page', 1), targets)
    return render(request, "pages/spending_summary.html",
                  {
                      'keyset': labels, 'dataset': percentages_list,
                      'form': form, 'money_in': total_received, 'money_out': total_spent,
                      'time': str(time).capitalize(), 'targets': list_of_targets,
                      'currency': currency
                  }
                  )
