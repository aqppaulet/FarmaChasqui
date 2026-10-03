import json
from django.test import TestCase
from django.urls import reverse
from products.models import Product
from .models import CustomerRequest


class OrderRequestTests(TestCase):
    def setUp(self):
        self.otc = Product.objects.create(name="Paracetamol", presentation="500 mg", price="5.50", stock=2, sale_condition="OTC")
        self.rx = Product.objects.create(name="Amoxicilina", presentation="500 mg", price="24.00", stock=2, sale_condition="RX")

    def post(self, payload):
        return self.client.post(reverse("create_request"), data=json.dumps(payload), content_type="application/json")

    def test_creates_otc_request(self):
        response = self.post({"product_id": self.otc.id, "quantity": 1, "name": "Ana Ruiz", "phone": "999 111 222"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(CustomerRequest.objects.count(), 1)

    def test_rejects_prescription_product(self):
        response = self.post({"product_id": self.rx.id, "quantity": 1, "name": "Ana Ruiz", "phone": "999 111 222"})
        self.assertEqual(response.status_code, 403)
