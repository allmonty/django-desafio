from decimal import Decimal

from api.models import CreditCard, Wallet

class Wallet_Manager():

    def calculate_available_credit(wallet):
        available_credit = 0
        credit_cards = CreditCard.objects.filter(wallet=wallet)
        for credit_card in credit_cards:
            available_credit += credit_card.available_amount
        return available_credit

    def calculate_maximum_limit(wallet):
        maximum_limit = 0
        credit_cards = CreditCard.objects.filter(wallet=wallet)
        for credit_card in credit_cards:
            maximum_limit += credit_card.limit
        return maximum_limit

    def edit_chosen_limit(wallet, value):
        maximum_limit = Wallet_Manager.calculate_maximum_limit(wallet)
        if value >= 0 and value <= maximum_limit:
            wallet.chosen_limit = value
            wallet.save(update_fields=['chosen_limit'])
        else:
            raise ValueError('Chosen Limit Problem: value must be (>= 0) and (<= maximum_limit)')
