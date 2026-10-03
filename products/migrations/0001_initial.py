from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [migrations.CreateModel(
        name="Product",
        fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("name", models.CharField(max_length=150, verbose_name="nombre")),
            ("presentation", models.CharField(max_length=150, verbose_name="presentación")),
            ("price", models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(0)], verbose_name="precio")),
            ("stock", models.PositiveIntegerField(default=0, verbose_name="unidades disponibles")),
            ("sale_condition", models.CharField(choices=[("OTC", "Venta sin receta"), ("RX", "Requiere receta")], max_length=3, verbose_name="condición de venta")),
            ("is_active", models.BooleanField(default=True, verbose_name="activo")),
            ("updated_at", models.DateTimeField(auto_now=True, verbose_name="actualizado")),
        ],
        options={"ordering": ["name"]},
    ), migrations.AddConstraint(model_name="product", constraint=models.UniqueConstraint(fields=("name", "presentation"), name="unique_product_presentation"))]
