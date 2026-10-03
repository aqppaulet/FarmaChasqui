"""Reglas transparentes para la primera atención; no son consejo clínico."""
import unicodedata

from products.models import Product


ESCALATION_TERMS = {
    "receta": "La venta requiere revisión de receta por el químico farmacéutico.",
    "dosis": "Las consultas de dosis deben ser atendidas por el químico farmacéutico.",
    "interaccion": "Las posibles interacciones necesitan evaluación profesional.",
    "alergia": "Las alergias requieren evaluación profesional.",
    "embarazo": "Las consultas durante el embarazo requieren evaluación profesional.",
    "sintoma": "La consulta describe síntomas y requiere evaluación profesional.",
    "dolor": "No podemos recomendar un tratamiento para síntomas; consulte al profesional.",
}


def normalize(value):
    return "".join(
        char for char in unicodedata.normalize("NFD", value.lower())
        if unicodedata.category(char) != "Mn"
    )


def escalation_reason(message):
    normalized = normalize(message)
    for term, reason in ESCALATION_TERMS.items():
        if term in normalized:
            return reason
    return None


def find_product(message):
    normalized_message = normalize(message)
    for product in Product.objects.filter(is_active=True):
        if normalize(product.name) in normalized_message:
            return product
    return None


def answer(message):
    """Retorna un resultado serializable para el canal web."""
    reason = escalation_reason(message)
    if reason:
        return {
            "type": "escalation",
            "message": f"{reason} No doy diagnósticos ni indicaciones. Te derivaré al químico farmacéutico.",
            "product": None,
        }

    product = find_product(message)
    if product is None:
        return {
            "type": "not_found",
            "message": "No identifiqué ese producto en el catálogo. Escribe el nombre comercial o consulta al personal de la botica.",
            "product": None,
        }
    if product.sale_condition == Product.SaleCondition.PRESCRIPTION:
        return {
            "type": "escalation",
            "message": f"{product.name} requiere receta y validación del químico farmacéutico. No puedo confirmar ni registrar este pedido.",
            "product": None,
        }
    if not product.available:
        return {
            "type": "out_of_stock",
            "message": f"{product.name} está temporalmente sin disponibilidad. El personal puede confirmar alternativas autorizadas.",
            "product": None,
        }
    return {
        "type": "product",
        "message": f"Encontré {product.name} ({product.presentation}). Precio referencial: S/ {product.price}. Disponible: sí.",
        "product": {"id": product.id, "name": product.name, "presentation": product.presentation, "price": str(product.price)},
    }
