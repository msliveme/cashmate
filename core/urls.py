# core/urls.py

from django.urls import path
from . import views

# এই ফাইলটি URL এবং View ফাংশনের মধ্যে সংযোগ স্থাপন করে
urlpatterns = [
    # --- সাধারণ পেজ ---
    path('', views.landing_page, name='landing_page'),
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # --- ইউজার অ্যাকাউন্ট সম্পর্কিত ---
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # --- লেনদেন (Transaction) সম্পর্কিত ---
    path('add-transaction/', views.add_transaction_view, name='add_transaction'),

    # --- ক্যাটাগরি (Category) সম্পর্কিত ---
    path('categories/', views.manage_categories_view, name='manage_categories'),
    path('categories/edit/<int:pk>/', views.edit_category_view, name='edit_category'),

    # --- লোন (Loan) সম্পর্কিত ---
    path('loans/', views.manage_loans_view, name='manage_loans'),
    path('loans/<int:pk>/mark-repaid/', views.mark_loan_as_repaid_view, name='mark_loan_repaid'),

    # --- Account সম্পর্কিত ---
    path('add-account/', views.add_account_view, name='add_account'),
]