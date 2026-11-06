from django.test import TestCase
from django.urls import reverse


class HomepageIsWorkingTests(TestCase):
    def test_homepage_returns_200(self):
        response = self.client.get(reverse("homepage:home"))
        self.assertEqual(response.status_code, 200)
