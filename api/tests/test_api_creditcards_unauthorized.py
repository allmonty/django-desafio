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
    
    def test_POST_create_creditcard_should_respond_unauthorized(self):
        data = {
            'number'            : '123987654',
            'due_date'          : '2018-12-22',
            'expiration_date'   : '2018-12-28',
            'cvv'               : '435',
            'limit'             : 1550,
            'available_amount'  : 1250
            }

        response = self.client.post('/api/credit-cards/', data, format='json')

        self.assertEqual(response.status_code, 401)
    
    def test_POST_edit_creditcard_should_respond_unauthorized(self):
        data = {
            'number': '123987654',
            'due_date': '2018-12-22',
            'expiration_date': '2018-12-28',
            'cvv': '435',
            'limit': 1550,
            'available_amount': 1250
        }

        response = self.client.post('/api/credit-cards/1239876542/', data, format='json')

        self.assertEqual(response.status_code, 401)
    
    def test_DELETE_creditcard_should_respond_unauthorized(self):

        response = self.client.delete('/api/credit-cards/123987654/')

        self.assertEqual(response.status_code, 401)
