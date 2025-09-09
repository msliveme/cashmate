# core/forms.py

from django import forms
from .models import Transaction, Category

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['type', 'amount', 'category', 'date', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 500.00'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'e.g., Monthly grocery shopping'}),
        }
    
    # এই ফাংশনটি নিশ্চিত করে যে ব্যবহারকারী শুধুমাত্র তার নিজের তৈরি করা ক্যাটাগরিগুলোই দেখতে পাবে
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TransactionForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = Category.objects.filter(user=user)
            # যদি কোনো ক্যাটাগরি না থাকে, তাহলে একটি খালি অপশন দেখানোর ব্যবস্থা
            self.fields['category'].empty_label = "Select a category"

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Salary, Food, Transport'}),
        }

        # core/forms.py

# ... (আগের import গুলো থাকবে)
from .models import Transaction, Category, Loan # Loan মডেলটি import করুন

# ... (আগের TransactionForm এবং CategoryForm থাকবে) ...

# --- নতুন লোন ফর্মটি নিচে যোগ করুন ---
class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        # 'user' এবং 'is_repaid' ফিল্ড দুটি ফর্ম থেকে বাদ দেওয়া হয়েছে, কারণ এগুলো স্বয়ংক্রিয়ভাবে সেট হবে
        fields = ['person_name', 'amount', 'date_lent']
        widgets = {
            'person_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Person's Name"}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Loan Amount'}),
            'date_lent': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }