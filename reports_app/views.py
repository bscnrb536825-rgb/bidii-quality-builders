from django.shortcuts import render, get_object_or_404
from customer_app.models import Customer
from project_app.models import Project
from invoice_app.models import Invoice

from django.db.models import Sum
from django.http import HttpResponse

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

from datetime import datetime
# =========================
# REPORTS DASHBOARD
# =========================
def reports_dashboard(request):

    invoices = Invoice.objects.all()

    # ===== FILTERS =====
    month = request.GET.get('month')
    year = request.GET.get('year')
    date = request.GET.get('date')

    if month:
        invoices = invoices.filter(created_at__month=month)

    if year:
        invoices = invoices.filter(created_at__year=year)

    if date:
        invoices = invoices.filter(created_at__date=date)

    # ===== COUNTS =====
    total_customers = Customer.objects.count()
    total_projects = Project.objects.count()
    total_invoices = invoices.count()

    paid_invoices = invoices.filter(status='Paid').count()
    pending_invoices = invoices.filter(status='Pending').count()

    total_paid_amount = (
        invoices.filter(status='Paid')
        .aggregate(Sum('amount'))['amount__sum'] or 0
    )

    total_pending_amount = (
        invoices.filter(status='Pending')
        .aggregate(Sum('amount'))['amount__sum'] or 0
    )

    context = {
        'total_customers': total_customers,
        'total_projects': total_projects,
        'total_invoices': total_invoices,
        'paid_invoices': paid_invoices,
        'pending_invoices': pending_invoices,
        'total_paid_amount': total_paid_amount,
        'total_pending_amount': total_pending_amount,
    }

    return render(
        request,
        'reports_app/reports_dashboard.html',
        context
    )


# =========================
# EXPORT SUMMARY PDF
# =========================
def export_reports_pdf(request):

    total_customers = Customer.objects.count()
    total_projects = Project.objects.count()
    total_invoices = Invoice.objects.count()

    total_paid_amount = (
        Invoice.objects.filter(status='Paid')
        .aggregate(Sum('amount'))['amount__sum'] or 0
    )

    total_pending_amount = (
        Invoice.objects.filter(status='Pending')
        .aggregate(Sum('amount'))['amount__sum'] or 0
    )

    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = (
        'attachment; filename="reports.pdf"'
    )

    p = canvas.Canvas(response, pagesize=A4)

    width, height = A4

    # ===== TITLE =====
    p.setFont("Helvetica-Bold", 18)
    p.drawCentredString(
        width / 2,
        height - 2 * cm,
        "Bidii Quality Builders"
    )

    p.setFont("Helvetica", 14)
    p.drawCentredString(
        width / 2,
        height - 3 * cm,
        "Reports Summary"
    )

    # ===== DATE =====
    p.setFont("Helvetica", 10)

    p.drawRightString(
        width - 2 * cm,
        height - 4 * cm,
        f"Generated on: {datetime.now().strftime('%d %B %Y')}"
    )

    # ===== CONTENT =====
    y = height - 6 * cm

    p.setFont("Helvetica", 12)

    p.drawString(3 * cm, y, f"Total Customers: {total_customers}")
    y -= 1 * cm

    p.drawString(3 * cm, y, f"Total Projects: {total_projects}")
    y -= 1 * cm

    p.drawString(3 * cm, y, f"Total Invoices: {total_invoices}")
    y -= 1 * cm

    p.drawString(
        3 * cm,
        y,
        f"Total Paid Amount: KES {total_paid_amount}"
    )
    y -= 1 * cm

    p.drawString(
        3 * cm,
        y,
        f"Total Pending Amount: KES {total_pending_amount}"
    )

    p.showPage()
    p.save()

    return response


# =========================
# CUSTOMER REPORT PDF
# =========================
def customer_report_pdf(request, customer_id):

    customer = get_object_or_404(Customer, id=customer_id)

    invoices = Invoice.objects.filter(customer=customer)

    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = (
        f'attachment; filename="{customer.first_name}_report.pdf"'
    )

    p = canvas.Canvas(response, pagesize=A4)

    width, height = A4

    y = height - 2 * cm

    # ===== TITLE =====
    p.setFont("Helvetica-Bold", 18)
    p.drawString(2 * cm, y, "Customer Report")

    y -= 2 * cm

    # ===== CUSTOMER INFO =====
    p.setFont("Helvetica", 12)

    p.drawString(
        2 * cm,
        y,
        f"Customer: {customer.first_name} {customer.last_name}"
    )

    y -= 2 * cm

    # ===== INVOICES =====
    for invoice in invoices:

        p.drawString(
            2 * cm,
            y,
            f"Invoice #{invoice.id} | "
            f"{invoice.status} | "
            f"KES {invoice.amount}"
        )

        y -= 1 * cm

        # Prevent text from going off page
        if y < 2 * cm:
            p.showPage()
            y = height - 2 * cm

    p.showPage()
    p.save()

    return response