from django.core.validators import MinValueValidator
from django.db import models


class Product(models.Model):
    class SaleCondition(models.TextChoices):
        OTC = "OTC", "Venta sin receta"
        PRESCRIPTION = "RX", "Requiere receta"

    name = models.CharField("nombre", max_length=150)
    presentation = models.CharField("presentación", max_length=150)
    price = models.DecimalField("precio", max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    stock = models.PositiveIntegerField("unidades disponibles", default=0)
    sale_condition = models.CharField("condición de venta", max_length=3, choices=SaleCondition.choices)
    is_active = models.BooleanField("activo", default=True)
    updated_at = models.DateTimeField("actualizado", auto_now=True)

    class Meta:
        ordering = ["name"]
        constraints = [models.UniqueConstraint(fields=["name", "presentation"], name="unique_product_presentation")]

    @property
    def available(self):
        return self.stock > 0 and self.is_active

    def __str__(self):
        return f"{self.name} - {self.presentation}"
