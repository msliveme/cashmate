from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-account/', views.add_account, name='add_account'),
    path('register/', views.register, name='register'),
]
