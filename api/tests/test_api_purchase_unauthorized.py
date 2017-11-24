from django.test import TestCase, RequestFactory
from rest_framework.test import APIClient
from decimal import Decimal

from rest_framework.test import force_authenticate
from django.db import transaction

from api.models import CreditCard, Wallet


class TestPurchaseAPI_Unauthorized(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_POST_should_respond_unauthorized(self):
        dataJSON = {}

        response = self.client.post('/api/purchase/',
                                dataJSON,
                                format='json')
        
        self.assertEqual(response.status_code, 401)