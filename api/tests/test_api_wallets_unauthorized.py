from django.test import TestCase, RequestFactory
from rest_framework.test import APIClient
from decimal import Decimal

from rest_framework.test import force_authenticate
from django.db import transaction

from api.models import CreditCard, Wallet


class TestWalletsAPI_Unauthorized(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_GET_user_wallet_should_respond_unauthorized(self):
        response = self.client.get('/api/wallets/')

        self.assertEqual(response.status_code, 401)

    def create_post_request(self, username=None, email=None):
        dataJSON = {
                        "password": "test123",
                        "first_name": "test",
                        "last_name": "man"
                    }
        if username:
            dataJSON["username"] = username
        if email:
            dataJSON["email"] = email

        return self.client.post('/api/wallets/create/',
                                dataJSON,
                                format='json')

    def test_POST_create_wallet_should_count_more_1_in_DB(self):
        numberOfWalletsBefore = len(Wallet.objects.all())

        response = self.create_post_request("testman", "testman@mailinator.com")

        numberOfWalletsAfter = len(Wallet.objects.all())

        self.assertEqual(response.status_code, 200)
        self.assertTrue(numberOfWalletsAfter > numberOfWalletsBefore)
    
    def test_POST_create_wallet_missing_username_and_email_should_respond_400(self):
        numberOfWalletsBefore = len(Wallet.objects.all())

        response = self.create_post_request()

        numberOfWalletsAfter = len(Wallet.objects.all())

        self.assertEqual(response.status_code, 400)
        self.assertTrue(numberOfWalletsAfter == numberOfWalletsBefore)
    
    @transaction.atomic
    def test_POST_create_wallet_for_existing_user_should_respond_400(self):
        response = self.create_post_request("testman", "testman@mailinator.com")

        self.assertEqual(response.status_code, 200)
    
        response = self.create_post_request("testman", "testman@mailinator.com")
        
        self.assertEqual(response.status_code, 400)
        
