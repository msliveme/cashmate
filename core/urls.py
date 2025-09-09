from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-account/', views.add_account, name='add_account'),
    path('register/', views.register, name='register'),
    path('account/<int:account_id>/transactions/', views.view_transactions, name='view_transactions'),
    path('account/<int:account_id>/add_transaction/', views.add_transaction, name='add_transaction'),
]
