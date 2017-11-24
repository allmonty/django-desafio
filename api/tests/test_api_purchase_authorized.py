from django.test import TestCase, RequestFactory
from rest_framework.test import APIClient
from decimal import Decimal

from rest_framework.test import force_authenticate

from django.contrib.auth.models import User, Group
from rest_framework.authtoken.models import Token
from api.models import CreditCard, Wallet


class TestPurchaseAPI_Authorized(TestCase):
    def setUp(self):
        self.user1 = User(username="testman1",
                          password="test123",
                          email="testman1@mailinator.com",
                          first_name="test1",
                          last_name="man")
        self.user1.save()
        self.wallet1 = Wallet(user=self.user1)
        self.wallet1.save()

        self.user2 = User(username="testman2",
                          password="test123",
                          email="testman2@mailinator.com",
                          first_name="test2",
                          last_name="man")
        self.user2.save()
        self.wallet2 = Wallet(user=self.user2)
        self.wallet2.save()

        self.user3 = User(username="testman3",
                          password="test123",
                          email="testman3@mailinator.com",
                          first_name="test3",
                          last_name="man")
        self.user3.save()
        self.wallet3 = Wallet(user=self.user3)
        self.wallet3.save()

        self.creditcard1_u1 = CreditCard(number='000000001',
                                         due_date='2017-11-22',
                                         expiration_date='2017-11-25',
                                         cvv='123',
                                         limit=Decimal(1000),
                                         available_amount=Decimal(500),
                                         wallet=self.wallet1
                                         )
        self.creditcard1_u1.save()
        self.creditcard2_u1 = CreditCard(number='000000002',
                                         due_date='2017-11-25',
                                         expiration_date='2017-11-25',
                                         cvv='123',
                                         limit=Decimal(1000),
                                         available_amount=Decimal(300),
                                         wallet=self.wallet1
                                         )
        self.creditcard2_u1.save()
        self.creditcard1_u2 = CreditCard(number='000000003',
                                         due_date='2017-11-22',
                                         expiration_date='2017-11-25',
                                         cvv='123',
                                         limit=Decimal(1000),
                                         available_amount=Decimal(350),
                                         wallet=self.wallet2
                                         )
        self.creditcard1_u2.save()

        self.client = APIClient()
    
    def test_POST_purchase_missing_value_user1_should_respond_400(self):
        token = Token.objects.create(user=self.user1)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        # data = {"value":0}

        response = self.client.post('/api/purchase/', {}, format='json')

        self.assertEqual(response.status_code, 400)
    
    def test_POST_purchase_more_than_available_credit_user1_should_respond_400(self):
        token = Token.objects.create(user=self.user1)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        value = self.creditcard1_u1.available_amount + self.creditcard2_u1.available_amount
        data = {"value":value}

        response = self.client.post('/api/purchase/', data, format='json')

        self.assertEqual(response.status_code, 400)
    
    def test_POST_purchase_valid_vale_user1_has_2_cards_should_respond_200(self):
        token = Token.objects.create(user=self.user1)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        self.wallet1.chosen_limit = 100
        self.wallet1.save()

        value = 50
        data = {"value":value}

        response = self.client.post('/api/purchase/', data, format='json')

        self.assertEqual(response.status_code, 200)
    
    def test_POST_purchase_valid_vale_user2_has_1_card_should_respond_200(self):
        token = Token.objects.create(user=self.user2)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        self.wallet2.chosen_limit = 100
        self.wallet2.save()

        value = 50
        data = {"value": value}

        response = self.client.post('/api/purchase/', data, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['value'], 50)
        self.assertEqual(response.data['wallet']['chosen_limit'], 100)
        self.assertEqual(response.data['wallet']['available_credit'], 300)
    
    def test_POST_purchase_valid_vale_user3_has_0_card_should_respond_400(self):
        token = Token.objects.create(user=self.user3)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        self.wallet3.chosen_limit = 100
        self.wallet3.save()

        value = 50
        data = {"value": value}

        response = self.client.post('/api/purchase/', data, format='json')

        self.assertEqual(response.status_code, 400)
        
