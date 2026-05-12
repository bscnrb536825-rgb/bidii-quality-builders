from django.urls import path
from . import views

app_name = 'customer_app'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.customer_list, name='customer_list'),
    path('add_customer/', views.add_customer, name='add_customer'),
    path('edit_customer/<int:id>/', views.edit_customer, name='edit_customer'),
    path('delete_customer/<int:id>/', views.delete_customer, name='delete_customer'),
    
]
