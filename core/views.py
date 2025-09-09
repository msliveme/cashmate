from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Account, Transaction, Category
from django.db.models import Sum, DecimalField

def index(request):
    return render(request, 'core/landing_page.html')

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
    return render(request, 'core/add_account.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def view_transactions(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    context = {
        'account': account,
        'transactions': transactions
    }
    return render(request, 'core/view_transactions.html', context)

@login_required
def add_transaction(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)
    if request.method == 'POST':
        transaction_type = request.POST['transaction_type']
        amount = request.POST['amount']
        date = request.POST['date']
        category_id = request.POST['category']
        description = request.POST['description']

        category = get_object_or_404(Category, id=category_id, user=request.user) if category_id else None

        Transaction.objects.create(
            user=request.user,
            account=account,
            transaction_type=transaction_type,
            amount=amount,
            date=date,
            category=category,
            description=description
        )
        return redirect('view_transactions', account_id=account.id)
    
    categories = Category.objects.filter(user=request.user)
    context = {
        'account': account,
        'categories': categories
    }
    return render(request, 'core/add_transaction.html', context)
