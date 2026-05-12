from django.shortcuts import render, redirect
from .models import Customer
from .forms import CustomerForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from project_app.models import Project
from invoice_app.models import Invoice
from django.contrib import messages
from django.shortcuts import render,redirect, get_object_or_404
from django.core.paginator import Paginator
#dashboard view
@login_required
def dashboard(request):
        total_customers = Customer.objects.count()
        total_projects = Project.objects.count()
        total_invoices = Invoice.objects.count()

        #Active_projects
        #active_projects = Project.objects.count() 
        active_projects = Project.objects.filter(status='ongoing').count()

        #recent customers
        recent_customers = Customer.objects.order_by('id')[:5]


     
        context={
            'total_customers': total_customers,
            'total_projects': total_projects,
            'pending_invoices': total_invoices,
            'active_projects': active_projects,
            'recent_customers': recent_customers,

        }
        return render(request, 'customer_app/dashboard.html', context)

#add project view
def add_project(request):
    return render(request, 'customer_app/add_project.html')
    

# List of views for the customer app
@login_required
def customer_list(request):
    customers = Customer.objects.all().order_by('-id')

    paginator = Paginator(customers, 4)  # 4 customers per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
    }
    return render(request, 'customer_app/customer_list.html', context)    

#add new customer view
@login_required
def add_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer added successfully!')
            return redirect('customer_app:add_customer')
    else:
        form = CustomerForm()
    return render(request, 'customer_app/add_customer.html', {'form': form})

#edit customer view
@login_required
def edit_customer(request, id):
    customer = get_object_or_404(Customer, pk=id)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer updated successfully!')
            return redirect('customer_app:customer_list')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'customer_app/edit_customer.html', {'form': form})

#delete customer view
@login_required
def delete_customer(request, id):

    if request.method != "POST":
        return redirect('customer_app:customer_list')

    customer = get_object_or_404(Customer, pk=id)

    customer.delete()

    messages.success(request, 'Customer deleted successfully!')

    return redirect('customer_app:customer_list')    
#search customers view

@login_required
def customer_list(request):
    customers = Customer.objects.all().order_by('-id')

    paginator = Paginator(customers, 5)   # 5 customers per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'customer_app/customer_list.html', {
        'page_obj': page_obj
    })