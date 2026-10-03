from django.test import TestCase
from django.urls import reverse


class HomeTests(TestCase):
    def test_home_page_loads(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, "FarmaChasqui")
