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

        token = Token.objects.create(user=self.user1)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_calculate_available_credit_wallet_with_0_creditcards_should_return_0(self):

        available_credit = Wallet_Manager.calculate_available_credit(self.wallet3)

        self.assertEqual(available_credit, 0)
    
    def test_calculate_available_credit_wallet_with_1_creditcards_should_return_750(self):

        available_credit = Wallet_Manager.calculate_available_credit(self.wallet2)

        self.assertEqual(available_credit, self.creditcard1_u2.available_amount)
    
    def test_calculate_available_credit_wallet_with_2_creditcards_should_return_750(self):
        available_credit = Wallet_Manager.calculate_available_credit(self.wallet1)

        self.assertEqual(available_credit, 
                    self.creditcard1_u1.available_amount + self.creditcard2_u1.available_amount)
    
    def test_calculate_maximum_limit_wallet_with_0_creditcards_should_return_0(self):

        available_credit = Wallet_Manager.calculate_maximum_limit(self.wallet3)

        self.assertEqual(available_credit, 0)

    def test_calculate_maximum_limit_wallet_with_1_creditcards_should_return_750(self):

        maximum_limit = Wallet_Manager.calculate_maximum_limit(self.wallet2)

        self.assertEqual(maximum_limit, self.creditcard1_u2.limit)
    
    def test_calculate_maximum_limit_wallet_with_2_creditcards_should_return_750(self):
        maximum_limit = Wallet_Manager.calculate_maximum_limit(self.wallet1)

        self.assertEqual(maximum_limit, 
                    self.creditcard1_u1.limit + self.creditcard2_u1.limit)
    
    def test_edit_chosen_limit_wallet_with_2_creditcards_to_negative_should_do_nothing(self):
        wallet = self.wallet1
        chosen_limit_before = wallet.chosen_limit
        
        error_occured = False
        try:
            Wallet_Manager.edit_chosen_limit(wallet, -10)
        except ValueError as e:
            error_occured = True
        
        new_chosen = Wallet.objects.get(user=self.user1).chosen_limit

        self.assertIs(error_occured, True)
        self.assertEqual(new_chosen, chosen_limit_before)
    
    def test_edit_chosen_limit_wallet_with_2_creditcards_half_maximum_should_edit(self):
        wallet = self.wallet1
        maximum_limit = Wallet_Manager.calculate_maximum_limit(wallet)

        Wallet_Manager.edit_chosen_limit(wallet, maximum_limit / 2)
        
        new_chosen = Wallet.objects.get(user=self.user1).chosen_limit

        self.assertEqual(new_chosen, maximum_limit / 2)
    
    def test_edit_chosen_limit_wallet_with_2_creditcards_more_than_maximum_do_nothing(self):
        wallet = self.wallet1
        maximum_limit = Wallet_Manager.calculate_maximum_limit(wallet)
        chosen_limit_before = wallet.chosen_limit
        
        error_occured = False
        try:
            Wallet_Manager.edit_chosen_limit(wallet, maximum_limit * 2)
        except ValueError as e:
            error_occured = True
        
        new_chosen = Wallet.objects.get(user=self.user1).chosen_limit

        self.assertIs(error_occured, True)
        self.assertEqual(new_chosen, chosen_limit_before)
    
# ==================== can purchase ==================== #

    def test_can_purchase_less_than_chosen_limit_should_return_true(self):
        chosen_limit        = 1000
        available_credit    = 200
        value               = 100

        self.assertIs(Wallet_Manager.can_purchase(chosen_limit, available_credit, value), True)
    
    def test_can_purchase_equal_chosen_limit_should_return_true(self):
        chosen_limit        = 1000
        available_credit    = 1500
        value               = 1000

        self.assertIs(Wallet_Manager.can_purchase(chosen_limit, available_credit, value), True)
    
    def test_can_purchase_more_than_chosen_limit_should_return_false(self):
        chosen_limit        = 1000
        available_credit    = 200
        value               = 2000

        self.assertIs(Wallet_Manager.can_purchase(chosen_limit, available_credit, value), False)
    
    def test_can_purchase_negative_value_should_return_false(self):
        chosen_limit = 1000
        available_credit = 200
        value = -100

        self.assertIs(Wallet_Manager.can_purchase(chosen_limit, available_credit, value), False)
    
    def test_can_purchase_more_than_available_credit_should_return_false(self):
        chosen_limit        = 1000
        available_credit    = 200
        value               = 250

        self.assertIs(Wallet_Manager.can_purchase(chosen_limit, available_credit, value), False)
    
    def test_can_purchase_equal_available_credit_should_return_True(self):
        chosen_limit        = 1000
        available_credit    = 200
        value               = 200

        self.assertIs(Wallet_Manager.can_purchase(chosen_limit, available_credit, value), True)
    
    def test_can_purchase_less_than_available_credit_should_return_True(self):
        chosen_limit        = 1000
        available_credit    = 200
        value               = 100

        self.assertIs(Wallet_Manager.can_purchase(chosen_limit, available_credit, value), True)
    
# ==================== choose credit card ==================== #

    def test_choose_credit_farther_in_the_month_should_return_card_1(self):
        card1 = CreditCard(number='000000011', due_date='2017-11-25', available_amount=Decimal(350))
        card2 = CreditCard(number='000000012', due_date='2017-11-22', available_amount=Decimal(350))
        value = 100

        credit_cards = [card1, card2]

        self.assertEqual(Wallet_Manager.choose_credit_card(credit_cards, value), [card1])
    
    def test_choose_credit_farther_in_the_month_should_return_card_2(self):
        card1 = CreditCard(number='000000011', due_date='2017-11-22', available_amount=Decimal(350))
        card2 = CreditCard(number='000000012', due_date='2017-11-25', available_amount=Decimal(350))
        value = 100

        credit_cards = [card1, card2]

        self.assertEqual(Wallet_Manager.choose_credit_card(credit_cards, value), [card2])
    
    def test_choose_credit_smallest_limit_when_both_has_same_due_date_should_return_card_1(self):
        card1 = CreditCard(number='000000011', due_date='2017-11-22', available_amount=Decimal(200))
        card2 = CreditCard(number='000000012', due_date='2017-11-22', available_amount=Decimal(350))
        value = 100

        credit_cards = [card1, card2]

        self.assertEqual(Wallet_Manager.choose_credit_card(credit_cards, value), [card1])
    
    def test_choose_credit_smallest_limit_when_both_has_same_due_date_should_return_card_2(self):
        card1 = CreditCard(number='000000011', due_date='2017-11-22', available_amount=Decimal(350))
        card2 = CreditCard(number='000000012', due_date='2017-11-22', available_amount=Decimal(200))
        value = 100

        credit_cards = [card1, card2]

        self.assertEqual(Wallet_Manager.choose_credit_card(credit_cards, value), [card2])
    
    def test_choose_credit_dividing_value_in_2_different_due_date_should_return_card1_before_card2(self):
        card1 = CreditCard(number='000000011', due_date='2017-11-25', available_amount=Decimal(200))
        card2 = CreditCard(number='000000012', due_date='2017-11-22', available_amount=Decimal(350))
        value = 400

        credit_cards = [card1, card2]

        self.assertEqual(Wallet_Manager.choose_credit_card(credit_cards, value), [card1, card2])
    
    def test_choose_credit_dividing_value_in_2_different_due_date_should_return_card2_before_card1(self):
        card1 = CreditCard(number='000000011', due_date='2017-11-21', available_amount=Decimal(200))
        card2 = CreditCard(number='000000012', due_date='2017-11-26', available_amount=Decimal(350))
        value = 400

        credit_cards = [card1, card2]

        self.assertEqual(Wallet_Manager.choose_credit_card(credit_cards, value), [card2, card1])
    
    def test_choose_credit_dividing_value_in_2_same_due_date_should_return_card1_before_card2(self):
        card1 = CreditCard(number='000000011', due_date='2017-11-21', available_amount=Decimal(200))
        card2 = CreditCard(number='000000012', due_date='2017-11-21', available_amount=Decimal(350))
        value = 400

        credit_cards = [card1, card2]

        self.assertEqual(Wallet_Manager.choose_credit_card(credit_cards, value), [card1, card2])
    
    def test_choose_credit_dividing_value_in_3_different_due_date_should_return_cards_1_2_3__a(self):
        card1 = CreditCard(number='000000011', due_date='2017-11-26', available_amount=Decimal(200))
        card2 = CreditCard(number='000000012', due_date='2017-11-24', available_amount=Decimal(200))
        card3 = CreditCard(number='000000013', due_date='2017-11-22', available_amount=Decimal(350))
        value = 500

        credit_cards = [card1, card2, card3]

        self.assertEqual(Wallet_Manager.choose_credit_card(credit_cards, value), [card1, card2, card3])
    
    def test_choose_credit_dividing_value_in_3_different_due_date_should_return_cards_1_2_3__b(self):
        card1 = CreditCard(number='000000011', due_date='2017-11-26', available_amount=Decimal(200))
        card2 = CreditCard(number='000000012', due_date='2017-11-24', available_amount=Decimal(200))
        card3 = CreditCard(number='000000013', due_date='2017-11-22', available_amount=Decimal(350))
        value = 500

        credit_cards = [card3, card1, card2]

        self.assertEqual(Wallet_Manager.choose_credit_card(credit_cards, value), [card1, card2, card3])

    def test_choose_credit_dividing_value_in_3_same_due_date_should_return_cards_1_2_3(self):
        card1 = CreditCard(number='000000011', due_date='2017-11-26', available_amount=Decimal(200))
        card2 = CreditCard(number='000000012', due_date='2017-11-26', available_amount=Decimal(200))
        card3 = CreditCard(number='000000013', due_date='2017-11-26', available_amount=Decimal(350))
        value = 500

        credit_cards = [card1, card2, card3]

        self.assertEqual(Wallet_Manager.choose_credit_card(credit_cards, value), [card1, card2, card3])
    
    def test_choose_credit_dividing_value_in_3_with_2_same_due_date_should_return_cards_1_2_3__a(self):
        card1 = CreditCard(number='000000011', due_date='2017-11-26', available_amount=Decimal(200))
        card2 = CreditCard(number='000000012', due_date='2017-11-26', available_amount=Decimal(200))
        card3 = CreditCard(number='000000013', due_date='2017-11-23', available_amount=Decimal(350))
        value = 500

        credit_cards = [card1, card2, card3]

        self.assertEqual(Wallet_Manager.choose_credit_card(credit_cards, value), [card1, card2, card3])
    
    def test_choose_credit_dividing_value_in_3_with_2_same_due_date_should_return_cards_1_2_3__b(self):
        card1 = CreditCard(number='000000011', due_date='2017-11-26', available_amount=Decimal(200))
        card2 = CreditCard(number='000000012', due_date='2017-11-23', available_amount=Decimal(200))
        card3 = CreditCard(number='000000013', due_date='2017-11-23', available_amount=Decimal(350))
        value = 500

        credit_cards = [card1, card2, card3]

        self.assertEqual(Wallet_Manager.choose_credit_card(credit_cards, value), [card1, card2, card3])