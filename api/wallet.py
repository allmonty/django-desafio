from decimal import Decimal
from itertools import groupby

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

    def can_purchase(chosen_limit, available_credit, value):
        if value > 0 and value <= chosen_limit:
            if value <= available_credit:
                return True
        return False

    def choose_credit_card(credit_cards, value):
        chosen_credit_cards = []
        sorted_credit_cards = []

        keys = set([])
        groups_by_key = {}
        for card in credit_cards:
            keys.add(card.due_date)
            if card.due_date in groups_by_key:
                groups_by_key[str(card.due_date)].append(card)
            else:
                groups_by_key[str(card.due_date)] = [card]
        keys = sorted(keys, reverse=True)

        for key in keys:
            sorted_by_limit = sorted(groups_by_key[key], key=lambda x: x.available_amount)
            partial_chosen, value = Wallet_Manager.__divide_between_cards(sorted_by_limit, value)
            chosen_credit_cards += partial_chosen
            if value <= 0:
                break
        
        return chosen_credit_cards
    
    def __divide_between_cards(credit_cards, value):
        chosen_cards = []
        for card in credit_cards:
            value -= card.available_amount
            chosen_cards.append(card)
            if value <= 0:
                break
        return chosen_cards, value
