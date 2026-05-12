from django.db import models
from customer_app.models import Customer
from project_app.models import Project  
from django.utils import timezone   


from django.db import models
from django.utils import timezone
from customer_app.models import Customer
from project_app.models import Project


class Invoice(models.Model):
    """
    Invoice generated at the end of a project.
    Customer is expected to pay within 30 days.
    """

    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='invoices'
    )

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='invoices'
    )

    invoice_number = models.CharField(
        max_length=50,
        unique=True
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    # 🔹 EXISTING FIELD (kept)
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    # 🔹 NEW but NON-BREAKING (nullable)
    due_date = models.DateField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    def is_overdue(self):
        """
        Calculated, not stored → Lean & safe.
        """
        if not self.due_date:
            return False
        return (
            self.status == 'Pending'
            and timezone.now().date() > self.due_date
        )

    def __str__(self):
        return self.invoice_number