from django.urls import path
from . import views

app_name = 'reports_app'

urlpatterns = [
    path('', views.reports_dashboard, name='reports_dashboard'),    
    path('export-pdf/', views.export_reports_pdf, name='export_reports_pdf'),
        path('customer/<int:customer_id>/pdf/', views.customer_report_pdf, name='customer_report_pdf'),

]