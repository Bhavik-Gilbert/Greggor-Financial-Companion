from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from ..models import Transaction, PotAccount
from django.http import HttpRequest, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse

@login_required
def view_users_transactions(request: HttpRequest, filter_type : str) -> HttpResponse:
    user = request.user
    user_accounts = PotAccount.objects.filter(user_id = user.id)
    transactions = []
    
    if filter_type == "all":
        transactions = []
        print("all")
        print(len(transactions))
        for account in user_accounts:
            transactions = [*transactions, *Transaction.objects.filter(sender_account=account)]
            transactions = [*transactions, *Transaction.objects.filter(receiver_account=account)]
    elif filter_type == "sent":
        transactions = []
        print("sent")
        print(len(transactions))
        for account in user_accounts:
            transactions = [*transactions, *Transaction.objects.filter(sender_account=account)]
    elif filter_type == "recieved":
        print("recieved")
        transactions = []
        print(len(transactions))
        for account in user_accounts:
            transactions = [*transactions, *Transaction.objects.filter(receiver_account=account)]
    else:
        return redirect('dashboard')
    
    print(len(transactions))
    page = request.GET.get('page', 1)
    paginator = Paginator(transactions, 10)
    try:
        listOfTransactions = paginator.page(page)
    except PageNotAnInteger:
        listOfTransactions = paginator.page(1)
    except EmptyPage:
        listOfTransactions = paginator.page(paginator.num_pages)
    
    return render(request, "pages/display_transactions.html", {'transactions': listOfTransactions})


def filter_request(request):
    if 'sent' in request.POST:
        return redirect(reverse('view_transactions', kwargs={'filter_type': "sent"}))
    elif 'recieved' in request.POST:
        return redirect(reverse('view_transactions', kwargs={'filter_type': "recieved"}))
    elif 'all' in request.POST:
        return redirect(reverse('view_transactions', kwargs={'filter_type': "all"}))
    else:
        return redirect('dashboard')



def reverse_with_next(url_name, next_url):
    url = reverse(url_name)
    url += f"?next={next_url}"
    return url
