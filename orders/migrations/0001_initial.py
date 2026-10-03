from django.db import migrations, models
import django.core.validators
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = [("products", "0001_initial")]
    operations = [migrations.CreateModel(
        name="CustomerRequest",
        fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("customer_name", models.CharField(max_length=100, verbose_name="nombre")),
            ("contact_phone", models.CharField(max_length=20, verbose_name="teléfono")),
            ("quantity", models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)], verbose_name="cantidad")),
            ("status", models.CharField(choices=[("PENDING", "Pendiente"), ("CONTACTED", "Contactado"), ("CANCELLED", "Cancelado")], default="PENDING", max_length=12, verbose_name="estado")),
            ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="creado")),
            ("product", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="requests", to="products.product")),
        ], options={"ordering": ["-created_at"]},
    )]
