import json

from django.test import TestCase
from django.urls import reverse
from products.models import Product
from .services import answer


class ChatRulesTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.otc = Product.objects.create(name="Paracetamol", presentation="500 mg", price="5.50", stock=5, sale_condition="OTC")
        Product.objects.create(name="Amoxicilina", presentation="500 mg", price="24.00", stock=5, sale_condition="RX")

    def test_finds_available_otc_product(self):
        result = answer("¿Tienen paracetamol?")
        self.assertEqual(result["type"], "product")
        self.assertEqual(result["product"]["id"], self.otc.id)

    def test_prescription_product_is_escalated(self):
        self.assertEqual(answer("Busco amoxicilina")["type"], "escalation")

    def test_dosage_question_is_escalated(self):
        self.assertEqual(answer("¿Qué dosis tomo?")["type"], "escalation")

    def test_endpoint_returns_a_catalog_result(self):
        response = self.client.post(
            reverse("chat_message"),
            data=json.dumps({"message": "Busco paracetamol"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["type"], "product")
