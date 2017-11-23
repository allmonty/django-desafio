from django.test import TestCase, RequestFactory
from rest_framework.test import APIClient
from decimal import Decimal

from django.contrib.auth.models import User, Group
from rest_framework.authtoken.models import Token
from api.models import CreditCard, Wallet


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

        self.creditcard1_u1 = CreditCard(number='123456789',
                                      due_date='2017-11-22',
                                      expiration_date='2017-11-25',
                                      cvv='123',
                                      limit=Decimal(1000),
                                      available_amount=Decimal(250),
                                      wallet=self.wallet1
                                      )
        self.creditcard1_u1.save()
        self.creditcard2_u1 = CreditCard(number='987654321',
                                         due_date='2017-11-22',
                                         expiration_date='2017-11-25',
                                         cvv='123',
                                         limit=Decimal(1000),
                                         available_amount=Decimal(500),
                                         wallet=self.wallet1
                                         )
        self.creditcard2_u1.save()
        self.creditcard1_u2 = CreditCard(number='456789123',
                                         due_date='2017-11-22',
                                         expiration_date='2017-11-25',
                                         cvv='123',
                                         limit=Decimal(1000),
                                         available_amount=Decimal(250),
                                         wallet=self.wallet2
                                         )
        self.creditcard1_u2.save()

        token = Token.objects.create(user=self.user1)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_GET_all_creditcards_should_exist_url(self):
        response = self.client.get('/api/credit-cards/')

        self.assertEqual(response.status_code, 200)

    def test_GET_all_creditcards_should_count_2_elements(self):
        response = self.client.get('/api/credit-cards/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_GET_by_number_should_exist_url(self):
        credit_number = self.creditcard1_u1.number

        response = self.client.get('/api/credit-cards/'+credit_number+"/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
    
    def test_GET_other_user_creditcard_by_number_should_return_empty(self):
        credit_number = self.creditcard1_u2.number

        response = self.client.get('/api/credit-cards/' + credit_number + "/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)
    
    def test_POST_create_creditcard_should_count_more_1_in_DB(self):
        numberOfCreditCardsBefore = len(CreditCard.objects.filter(wallet=self.wallet1))

        data = {
            'number'            : '123987654',
            'due_date'          : '2018-12-22',
            'expiration_date'   : '2018-12-28',
            'cvv'               : '435',
            'limit'             : 1550,
            'available_amount'  : 1250
            }

        response = self.client.post('/api/credit-cards/', data, format='json')

        numberOfCreditCardsAfter = len(CreditCard.objects.filter(wallet=self.wallet1))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(numberOfCreditCardsAfter, numberOfCreditCardsBefore + 1)
    
    def test_POST_create_creditcard_missing_creditcard_info_should_respond_400(self):
        numberOfCreditCardsBefore = len(CreditCard.objects.filter(wallet=self.wallet1))

        data = {
            'number': '123987654',
            # 'due_date': '2017-12-22',
            'expiration_date': '2017-12-28',
            'cvv': '435',
            'limit': 1550,
            'available_amount': 1250
        }

        response = self.client.post('/api/credit-cards/', data, format='json')
        
        numberOfCreditCardsAfter = len(CreditCard.objects.filter(wallet=self.wallet1))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(numberOfCreditCardsAfter, numberOfCreditCardsBefore)
    
    def test_DELETE_creditcard_should_count_minus_1_in_DB(self):
        numberOfCreditCardsBefore = len(CreditCard.objects.filter(wallet=self.wallet1))

        response = self.client.delete('/api/credit-cards/'+self.creditcard2_u1.number+'/')

        numberOfCreditCardsAfter = len(CreditCard.objects.filter(wallet=self.wallet1))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(numberOfCreditCardsAfter, numberOfCreditCardsBefore - 1)
    
    def test_DELETE_unexistent_creditcard_should_respond_404(self):
        numberOfCreditCardsBefore = len(CreditCard.objects.filter(wallet=self.wallet1))

        response = self.client.delete('/api/credit-cards/000000000000000000000/')

        numberOfCreditCardsAfter = len(CreditCard.objects.filter(wallet=self.wallet1))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(numberOfCreditCardsAfter, numberOfCreditCardsBefore)
    
    def test_DELETE_other_user_creditcard_should_respond_404(self):
        numberOfCreditCardsBefore = len(CreditCard.objects.filter(wallet=self.wallet2))

        response = self.client.delete('/api/credit-cards/'+self.creditcard1_u2.number+'/')

        numberOfCreditCardsAfter = len(CreditCard.objects.filter(wallet=self.wallet2))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(numberOfCreditCardsAfter, numberOfCreditCardsBefore)
