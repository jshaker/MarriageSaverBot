from django.test import TestCase
from django.urls import reverse
from django.test import Client
from urlservice.models import ItemQueries, Items, Queries

class ItemQueryViewTest(TestCase):
    def setUp(self):
        self.url = reverse('urlservice:itemquery')
    
    def test_get(self):
        """Get all URL's from the database"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)