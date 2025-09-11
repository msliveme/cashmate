# core/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Transaction, Category, Debt, Account

class UserRegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'initial_balance']

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['transaction_type', 'amount', 'category', 'date', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'transaction_type': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 500.00'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'e.g., Monthly grocery shopping'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TransactionForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = Category.objects.filter(user=user)
            self.fields['category'].empty_label = "Select a category"

class CategoryForm(forms.ModelForm):
    parent = forms.ModelChoiceField(queryset=Category.objects.none(), required=False)

    class Meta:
        model = Category
        fields = ['name', 'parent']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Salary, Food, Transport'}),
            'parent': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(CategoryForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['parent'].queryset = Category.objects.filter(user=user, parent=None)

class DebtForm(forms.ModelForm):
    class Meta:
        model = Debt
        fields = ['person_name', 'amount', 'debt_type', 'due_date']
        widgets = {
            'person_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Person's Name"}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Loan Amount'}),
            'debt_type': forms.Select(attrs={'class': 'form-control'}),
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }