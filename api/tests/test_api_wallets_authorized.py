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

        self.creditcard1_u1 = CreditCard(number='000000001',
                                         due_date='2017-11-22',
                                         expiration_date='2017-11-25',
                                         cvv='123',
                                         limit=Decimal(1000),
                                         available_amount=Decimal(250),
                                         wallet=self.wallet1
                                         )
        self.creditcard1_u1.save()

        token = Token.objects.create(user=self.user1)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_GET_wallet_should_exist_url(self):
        response = self.client.get('/api/wallets/')

        self.assertEqual(response.status_code, 200)
    
    def test_GET_wallets_should_return_right_wallet(self):
        response = self.client.get('/api/wallets/')

        user = response.data["user"]
        available_credit = response.data["available_credit"]
        maximum_limit = response.data["maximum_limit"]
        chosen_limit = response.data["chosen_limit"]
        
        self.assertEqual(Decimal(available_credit), Decimal(250))
        self.assertEqual(Decimal(maximum_limit), Decimal(1000))
        self.assertEqual(Decimal(chosen_limit), self.wallet1.chosen_limit)
        self.assertEqual(user, str(self.wallet1.user))
    
    def test_POST_edit_chosen_limit_missing_data_should_respond_400(self):
        data = {}

        response = self.client.post('/api/wallets/', data, format='json')

        self.assertEqual(response.status_code, 400)
    
    def test_POST_edit_chosen_limit_wrong_data_should_respond_400(self):
        data = {'maximum_limit': 100}

        response = self.client.post('/api/wallets/', data, format='json')

        self.assertEqual(response.status_code, 400)
    
    def test_POST_edit_chosen_limit_to_100_should_respond_200(self):
        data = {'chosen_limit': 100}

        response = self.client.post('/api/wallets/', data, format='json')

        self.assertEqual(response.status_code, 200)
        
