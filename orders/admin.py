from django.contrib import admin
from .models import CustomerRequest


@admin.register(CustomerRequest)
class CustomerRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "customer_name", "product", "quantity", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("customer_name", "contact_phone", "product__name")
    readonly_fields = ("created_at",)
