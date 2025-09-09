from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from django.db.models import Sum, DecimalField

def index(request):
    return redirect('dashboard')

@login_required
def dashboard(request):
    accounts = Account.objects.filter(user=request.user)
    accounts_with_balance = []
    for account in accounts:
        income = Transaction.objects.filter(account=account, transaction_type='INCOME').aggregate(total=Sum('amount', output_field=DecimalField()))['total'] or 0.00
        expense = Transaction.objects.filter(account=account, transaction_type='EXPENSE').aggregate(total=Sum('amount', output_field=DecimalField()))['total'] or 0.00
        balance = account.initial_balance + income - expense
        accounts_with_balance.append({'account': account, 'balance': balance})

    context = {
        'accounts_with_balance': accounts_with_balance,
    }
    return render(request, 'core/dashboard.html', context)

@login_required
def add_account(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        initial_balance = request.POST.get('initial_balance')
        Account.objects.create(
            user=request.user,
            name=name,
            initial_balance=initial_balance
        )
        return redirect('dashboard')
    return render(request, 'core/templates/core/add_account.html')
