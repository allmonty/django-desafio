from django.test import TestCase, RequestFactory
from rest_framework.test import APIClient
from decimal import Decimal

from rest_framework.test import force_authenticate

from django.contrib.auth.models import User, Group
from rest_framework.authtoken.models import Token
from api.models import CreditCard, Wallet


class TestWalletsAPI_Authorized(TestCase):
    def setUp(self):
        self.user1 = User(username="testman",
                          password="test123",
                          email="testman@mailinator.com",
                          first_name="test",
                          last_name="man")
        self.user1.save()

        self.wallet1 = Wallet(user=self.user1, chosen_limit=Decimal(500))
        self.wallet1.save()

        token = Token.objects.create(user=self.user1)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_GET_wallet_should_exist_url(self):
        response = self.client.get('/api/wallets/')

        self.assertEqual(response.status_code, 200)
    
    def test_GET_wallets_should_return_right_wallet(self):
        response = self.client.get('/api/wallets/')

        chosen_limit = response.data[0]["fields"]["chosen_limit"]
        user = response.data[0]["fields"]["user"]
        
        self.assertEqual(Decimal(chosen_limit), self.wallet1.chosen_limit)
        self.assertEqual(user, self.wallet1.user.pk)
        
