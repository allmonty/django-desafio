from django.test import TestCase

from api.models import CreditCard, Wallet


class TestWalletModel(TestCase):
    def setUp(self):
        self.wallet = Wallet(owner_name="allan")
        self.wallet.save()

    def test_wallet_creation(self):
        self.assertEqual(Wallet.objects.count(), 1)

    def test_wallet_representation(self):
        self.assertEqual(self.wallet.owner_name + "'s wallet", str(self.wallet))