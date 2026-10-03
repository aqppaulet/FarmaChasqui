from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "presentation", "price", "stock", "sale_condition", "is_active", "updated_at")
    list_filter = ("sale_condition", "is_active")
    search_fields = ("name", "presentation")
