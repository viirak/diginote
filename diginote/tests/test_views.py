from django.test import TestCase
from django.urls import reverse

class TestViews(TestCase):

    def test_signup_page(self):
        respone = self.client.get(reverse('signup'))
        self.assertEqual(respone.status_code, 200)

    def test_home_page(self):
        respone = self.client.get(reverse('home'))
        self.assertEqual(respone.status_code, 200)