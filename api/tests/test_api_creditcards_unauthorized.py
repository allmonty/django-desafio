from django.test import TestCase, RequestFactory
from rest_framework.test import APIClient
from decimal import Decimal

from api.models import CreditCard, Wallet


class TestCreditCardsAPI_Unauthorized(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_GET_user_all_creditcards_should_respond_unauthorized(self):
        response = self.client.get('/api/credit-cards/')

        self.assertEqual(response.status_code, 401)
    
    def test_GET_user_specific_creditcards_should_respond_unauthorized(self):
        response = self.client.get('/api/credit-cards/234135/')

        self.assertEqual(response.status_code, 401)
