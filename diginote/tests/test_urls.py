from django.test import TestCase
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch

class TestUrls(TestCase):

    def test_signup_url(self):
        try:
            url = reverse('signup')
        except NoReverseMatch:
            url = None
        self.assertNotEqual(url, None)

    def test_home_url(self):
        try:
            url = reverse('home')
        except NoReverseMatch:
            url = None
        self.assertNotEqual(url, None)

