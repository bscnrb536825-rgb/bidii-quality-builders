from django.shortcuts import render, redirect
from .models import Project
from customer_app.models import Customer

def add_project(request):
    customers = Customer.objects.all()

    if request.method == 'POST':
        customer = Customer.objects.get(id=request.POST.get('customer'))

        Project.objects.create(
            customer=customer,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
            status=request.POST.get('status'),
            start_date=request.POST.get('start_date'),
            end_date=request.POST.get('end_date'),
        )

        return redirect('customer_app:dashboard')

    return render(request, 'project_app/add_project.html', {
        'customers': customers
    })

def project_list(request):
    projects = Project.objects.all()
    return render(request, 'project_app/project_list.html', {
        'projects': projects
    })