import json
import re

from django.http import JsonResponse
from django.views.decorators.http import require_POST

from products.models import Product
from .models import CustomerRequest


@require_POST
def create_request(request):
    try:
        payload = json.loads(request.body)
        product_id = int(payload.get("product_id"))
        quantity = int(payload.get("quantity", 1))
        name = str(payload.get("name", "")).strip()
        phone = str(payload.get("phone", "")).strip()
    except (TypeError, ValueError, json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"detail": "Datos de solicitud inválidos."}, status=400)

    if not (2 <= len(name) <= 100) or not re.fullmatch(r"[0-9+ ()-]{7,20}", phone) or quantity < 1:
        return JsonResponse({"detail": "Verifica tu nombre, teléfono y cantidad."}, status=400)
    try:
        product = Product.objects.get(pk=product_id, is_active=True)
    except Product.DoesNotExist:
        return JsonResponse({"detail": "El producto ya no está disponible."}, status=404)
    if product.sale_condition != Product.SaleCondition.OTC:
        return JsonResponse({"detail": "Los productos con receta deben ser validados por el químico farmacéutico."}, status=403)
    if product.stock < quantity:
        return JsonResponse({"detail": "No hay stock suficiente para esa cantidad."}, status=409)

    customer_request = CustomerRequest.objects.create(
        customer_name=name, contact_phone=phone, product=product, quantity=quantity,
    )
    return JsonResponse({"id": customer_request.id, "message": "Solicitud registrada. El personal confirmará la disponibilidad final."}, status=201)
