from django.core.validators import MinValueValidator
from django.db import models
from products.models import Product


class CustomerRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pendiente"
        CONTACTED = "CONTACTED", "Contactado"
        CANCELLED = "CANCELLED", "Cancelado"

    customer_name = models.CharField("nombre", max_length=100)
    contact_phone = models.CharField("teléfono", max_length=20)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="requests")
    quantity = models.PositiveIntegerField("cantidad", validators=[MinValueValidator(1)], default=1)
    status = models.CharField("estado", max_length=12, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField("creado", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Solicitud #{self.pk} - {self.product.name}"
