from django.test import TestCase, RequestFactory
from rest_framework.test import APIClient
from decimal import Decimal

from api.models import CreditCard, Wallet


class TestCreditCardsAPI(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.wallet2 = Wallet(owner_email='david@mailinator.com',
                              owner_name='david', chosen_limit=Decimal(450))
        self.wallet2.save()
        self.creditcard1 = CreditCard(number                = '123456789',
                                        due_date            = '2017-11-22',
                                        expiration_date     = '2017-11-25',
                                        cvv                 = '123',
                                        limit               = Decimal(1000),
                                        available_amount    = Decimal(250),
                                        wallet              = self.wallet2
                                  )
        self.creditcard1.save()
        self.creditcard2 = CreditCard(number='987654321',
                                      due_date='2017-11-23',
                                      expiration_date='2017-11-28',
                                      cvv='321',
                                      limit=Decimal(1500),
                                      available_amount=Decimal(750),
                                      wallet=self.wallet2
                                      )
        self.creditcard2.save()

    def test_GET_all_creditcards_should_exist_url(self):
        response = self.client.get('/api/credit-cards/')

        self.assertEqual(response.status_code, 200)

    def test_GET_all_creditcards_should_count_2_elements(self):
        response = self.client.get('/api/credit-cards/')

        self.assertTrue(len(response.data) > 0)
        self.assertEqual(response.status_code, 200)

    def test_GET_by_number_should_exist_url(self):
        credit_number = '987654321'
        response = self.client.get('/api/credit-cards/'+credit_number+"/")

        self.assertEqual(response.status_code, 200)

    def test_GET_by_number_should_count_1_element(self):
        credit_number = '987654321'
        response = self.client.get('/api/credit-cards/'+credit_number+"/")

        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, 200)
    
    def test_POST_create_creditcard_should_count_more_1_in_DB(self):
        numberOfCreditCardsBefore = len(CreditCard.objects.all())

        data = {
            'wallet_owner_email': 'david@mailinator.com',
            'number'            : '123987654',
            'due_date'          : '2017-12-22',
            'expiration_date'   : '2017-12-28',
            'cvv'               : '435',
            'limit'             : 1550,
            'available_amount'  : 1250
            }

        response = self.client.post('/api/credit-cards/', data, format='json')

        numberOfCreditCardsAfter = len(CreditCard.objects.all())

        self.assertEqual(response.status_code, 200)
        self.assertTrue(numberOfCreditCardsAfter > numberOfCreditCardsBefore)
    
    def test_POST_create_creditcard_without_wallet_owner_should_respond_400(self):
        data = {
            'number': '123987654',
            'due_date': '2017-12-22',
            'expiration_date': '2017-12-28',
            'cvv': '435',
            'limit': 1550,
            'available_amount': 1250
        }

        response = self.client.post('/api/credit-cards/', data, format='json')

        self.assertEqual(response.status_code, 400)
    
    def test_POST_create_creditcard_with_nonexisting_wallet_should_respond_400(self):
        data = {
            'wallet_owner_email': 'asdasfd@maiaslinator.com',
            'number': '123987654',
            'due_date': '2017-12-22',
            'expiration_date': '2017-12-28',
            'cvv': '435',
            'limit': 1550,
            'available_amount': 1250
        }

        response = self.client.post('/api/credit-cards/', data, format='json')

        self.assertEqual(response.status_code, 400)
