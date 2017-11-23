from django.test import TestCase, RequestFactory
from rest_framework.test import APIClient
from decimal import Decimal

from api.models import CreditCard, Wallet


class TestWalletsAPI(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.wallet1 = Wallet(owner_email='monteiro@mailinator.com', owner_name='monteiro', chosen_limit=Decimal(500))
        self.wallet1.save()
        self.wallet2 = Wallet(owner_email='david@mailinator.com', owner_name='david', chosen_limit=Decimal(450))
        self.wallet2.save()

    def test_GET_all_wallets_should_exist_url(self):
        response = self.client.get('/api/wallets/')

        self.assertEqual(response.status_code, 200)

    def test_GET_all_wallets_should_count_2_elements(self):
        response = self.client.get('/api/wallets/')

        self.assertTrue(len(response.data) > 0)
        self.assertEqual(response.status_code, 200)

    def test_GET_by_owner_email_should_exist_url(self):
        response = self.client.get('/api/wallets/david@mailinator.com/')

        self.assertEqual(response.status_code, 200)

    def test_GET_by_owner_email_should_count_1_element(self):
        response = self.client.get('/api/wallets/david@mailinator.com/')

        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, 200)
    
    def test_POST_create_wallet_should_count_more_1_in_DB(self):
        numberOfWalletsBefore = len(Wallet.objects.all())

        response = self.client.post('/api/wallets/',
                                    {'owner_email': 'mont@mailinator.com', 'owner_name': 'mont'},
                                    format='json')

        numberOfWalletsAfter = len(Wallet.objects.all())

        self.assertTrue(numberOfWalletsAfter > numberOfWalletsBefore)
        
