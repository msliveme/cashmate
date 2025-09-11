# core/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum
from decimal import Decimal
from .models import Transaction, Category, Debt
from .forms import TransactionForm, CategoryForm, DebtForm, UserRegisterForm

# Homepage / Landing Page View
def landing_page(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'core/landing_page.html')

import logging

logger = logging.getLogger(__name__)

# ... (other imports)

# User Registration View
def register_view(request):
    try:
        if request.user.is_authenticated:
            return redirect('dashboard')
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect('dashboard')
        else:
            form = UserRegisterForm()
        return render(request, 'registration/register.html', {'form': form})
    except Exception as e:
        logger.error(f"Error in register_view: {e}")
        raise

# User Login View
def login_view(request):
    try:
        if request.user.is_authenticated:
            return redirect('dashboard')
        if request.method == 'POST':
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('dashboard')
        else:
            form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})
    except Exception as e:
        logger.error(f"Error in login_view: {e}")
        raise

# User Logout View
def logout_view(request):
    logout(request)
    return redirect('landing_page')

# Dashboard View (Updated and Fixed)
@login_required
def dashboard_view(request):
    # বর্তমান ইউজারের সব লেনদেন নিয়ে আসা
    transactions = Transaction.objects.filter(user=request.user)

    # মোট আয় হিসাব করা
    income_result = transactions.filter(transaction_type='INCOME').aggregate(Sum('amount'))
    total_income = income_result['amount__sum'] or Decimal('0.0')

    # মোট ব্যয় হিসাব করা
    expense_result = transactions.filter(transaction_type='EXPENSE').aggregate(Sum('amount'))
    total_expense = expense_result['amount__sum'] or Decimal('0.0')
    
    # বর্তমান ব্যালেন্স হিসাব করা
    current_balance = total_income - total_expense

    # সাম্প্রতিক ১০টি লেনদেন
    recent_transactions = transactions.order_by('-date')[:10]
    
    context = {
        'total_income': total_income,
        'total_expense': total_expense,
        'current_balance': current_balance,
        'transactions': recent_transactions,
    }
    return render(request, 'core/dashboard.html', context)

# Add Transaction View
@login_required
def add_transaction_view(request):
    # Temporary workaround: get the user's first account
    try:
        account = request.user.account_set.first()
    except AttributeError:
        # Handle case where user has no accounts
        account = None

    if request.method == 'POST':
        form = TransactionForm(request.POST, user=request.user)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.account = account
            transaction.save()
            return redirect('dashboard')
    else:
        form = TransactionForm(user=request.user)
    
    return render(request, 'core/add_transaction.html', {'form': form, 'account': account})

# Manage Categories View
@login_required
def manage_categories_view(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, user=request.user)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect('manage_categories') 

    form = CategoryForm(user=request.user)
    categories = Category.objects.filter(user=request.user, parent=None).order_by('name')
    context = {
        'form': form,
        'categories': categories
    }
    return render(request, 'core/manage_categories.html', context)

# Loan Management View
@login_required
def manage_loans_view(request):
    if request.method == 'POST':
        form = DebtForm(request.POST)
        if form.is_valid():
            loan = form.save(commit=False)
            loan.user = request.user
            loan.save()
            return redirect('manage_loans')

    form = DebtForm()
    loans = Debt.objects.filter(user=request.user).order_by('is_settled', '-due_date')
    
    context = {
        'form': form,
        'loans': loans
    }
    return render(request, 'core/manage_loans.html', context)

# Mark Loan as Repaid View
@login_required
def mark_loan_as_repaid_view(request, pk):
    loan = get_object_or_404(Debt, pk=pk, user=request.user)
    
    if request.method == 'POST':
        loan.is_settled = True
        loan.date_repaid = timezone.now().date()
        loan.save()
    
    return redirect('manage_loans')