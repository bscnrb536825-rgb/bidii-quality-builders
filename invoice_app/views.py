from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from customer_app.models import Customer
from project_app.models import Project
from .models import Invoice


@login_required
def create_invoice(request):
    customers = Customer.objects.all()
    projects = Project.objects.all()

    if request.method == "POST":
        customer_id = request.POST.get('customer')
        project_id = request.POST.get('project')

        customer = get_object_or_404(Customer, id=customer_id)
        project = get_object_or_404(Project, id=project_id)

        Invoice.objects.create(
            customer=customer,
            project=project,
            invoice_number=request.POST.get('invoice_number'),
            amount=request.POST.get('amount'),
            due_date=request.POST.get('due_date'),
            status=request.POST.get('status'),
        )

        return redirect('invoice_app:invoice_list')

    return render(request, "invoice_app/add_invoice.html", {
        "customers": customers,
        "projects": projects,
    })


@login_required
def invoice_list(request):
    invoices = Invoice.objects.all().order_by('-id')

    return render(request, "invoice_app/invoice_list.html", {
        "invoices": invoices
    })