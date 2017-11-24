from django.test import TestCase, RequestFactory
from rest_framework.test import APIClient
from decimal import Decimal

from django.contrib.auth.models import User, Group
from rest_framework.authtoken.models import Token
from api.models import CreditCard, Wallet
from api.wallet import Wallet_Manager


class TestCreditCardsAPI_Authorized(TestCase):
    def setUp(self):
        self.user1 = User(username="testman1",
                          password="test123",
                          email="testman1@mailinator.com",
                          first_name="test1",
                          last_name="man")
        self.user1.save()
        self.wallet1 = Wallet(user=self.user1, chosen_limit=Decimal(500))
        self.wallet1.save()

        self.user2 = User(username="testman2",
                          password="test123",
                          email="testman2@mailinator.com",
                          first_name="test2",
                          last_name="man")
        self.user2.save()
        self.wallet2 = Wallet(user=self.user2, chosen_limit=Decimal(1000))
        self.wallet2.save()

        self.user3 = User(username="testman3",
                          password="test123",
                          email="testman3@mailinator.com",
                          first_name="test3",
                          last_name="man")
        self.user3.save()
        self.wallet3 = Wallet(user=self.user3, chosen_limit=Decimal(1000))
        self.wallet3.save()

        self.creditcard1_u1 = CreditCard(number='000000001',
                                         due_date='2017-11-22',
                                         expiration_date='2017-11-25',
                                         cvv='123',
                                         limit=Decimal(1000),
                                         available_amount=Decimal(250),
                                         wallet=self.wallet1
                                         )
        self.creditcard1_u1.save()
        self.creditcard2_u1 = CreditCard(number='000000002',
                                         due_date='2017-11-22',
                                         expiration_date='2017-11-25',
                                         cvv='123',
                                         limit=Decimal(1000),
                                         available_amount=Decimal(500),
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

        token = Token.objects.create(user=self.user1)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_calculate_available_credit_wallet_with_2_creditcards_should_return_750(self):
        available_credit = Wallet_Manager.calculate_available_credit(self.wallet1)

        self.assertEqual(available_credit, 
                    self.creditcard1_u1.available_amount + self.creditcard2_u1.available_amount)
    
    def test_calculate_available_credit_wallet_with_1_creditcards_should_return_750(self):

        available_credit = Wallet_Manager.calculate_available_credit(self.wallet2)

        self.assertEqual(available_credit, self.creditcard1_u2.available_amount)
    
    def test_calculate_available_credit_wallet_with_0_creditcards_should_return_0(self):

        available_credit = Wallet_Manager.calculate_available_credit(self.wallet3)

        self.assertEqual(available_credit, 0)
