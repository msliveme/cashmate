# core/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Transaction, Category, Loan
from .forms import TransactionForm, CategoryForm, LoanForm

# Homepage / Landing Page View
def landing_page(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'core/landing_page.html')

# User Registration View
def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'core/registration/register.html', {'form': form})

# User Login View
def login_view(request):
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
    return render(request, 'core/registration/login.html', {'form': form})

# User Logout View
def logout_view(request):
    logout(request)
    return redirect('landing_page')

# Dashboard View
@login_required
def dashboard_view(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')[:10]
    context = {
        'transactions': transactions
    }
    return render(request, 'core/dashboard.html', context)

# Add Transaction View
@login_required
def add_transaction_view(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST, user=request.user)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('dashboard')
    else:
        form = TransactionForm(user=request.user)
    
    return render(request, 'core/add_transaction.html', {'form': form})

# Manage Categories View
@login_required
def manage_categories_view(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect('manage_categories') 

    form = CategoryForm()
    categories = Category.objects.filter(user=request.user).order_by('name')
    context = {
        'form': form,
        'categories': categories
    }
    return render(request, 'core/manage_categories.html', context)

# --- নতুন দুটি View ফাংশন নিচে যোগ করা হয়েছে ---

# ১. লোন ম্যানেজমেন্টের মূল পেজ
@login_required
def manage_loans_view(request):
    # নতুন লোন যোগ করার ফর্ম হ্যান্ডেল করা
    if request.method == 'POST':
        form = LoanForm(request.POST)
        if form.is_valid():
            loan = form.save(commit=False)
            loan.user = request.user
            loan.save()
            return redirect('manage_loans')

    # GET রিকোয়েস্টের জন্য (পেজটি প্রথমবার লোড হলে)
    form = LoanForm()
    # বর্তমান ইউজারের সব লোন ডেটাবেস থেকে নিয়ে আসা
    # যেগুলো ফেরত হয়নি (unrepaid) সেগুলো আগে দেখাবে
    loans = Loan.objects.filter(user=request.user).order_by('is_repaid', '-date_lent')
    
    context = {
        'form': form,
        'loans': loans
    }
    return render(request, 'core/manage_loans.html', context)

# ২. লোনকে "Repaid" হিসেবে মার্ক করার জন্য
@login_required
def mark_loan_as_repaid_view(request, pk):
    # নির্দিষ্ট লোনটি খুঁজে বের করা এবং নিশ্চিত করা যে এটি বর্তমান ইউজারেরই
    loan = get_object_or_404(Loan, pk=pk, user=request.user)
    
    # শুধুমাত্র POST রিকোয়েস্ট গ্রহণ করা হবে নিরাপত্তার জন্য
    if request.method == 'POST':
        loan.is_repaid = True
        loan.date_repaid = timezone.now().date() # আজকের তারিখে ফেরত হিসেবে ধরা হবে
        loan.save()
    
    return redirect('manage_loans') # আগের পেজে ফেরত পাঠানো