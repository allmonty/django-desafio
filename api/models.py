from django.db import models
from decimal import Decimal


class Wallet(models.Model):
    owner_email = models.CharField('Owner Email', max_length=255, unique=True, default=None, null=True, blank=True)
    owner_name = models.CharField('Owner Name', max_length=255, default=None, null=True, blank=True)
    chosen_limit = models.DecimalField("Chosen Limit", max_digits=20, decimal_places=2, default=Decimal(0.00))

    def __str__(self):
        return "%s's wallet" % (self.owner_name)


class CreditCard(models.Model):
    number          = models.CharField('Number', max_length=25, default=None, null=True, blank=True)
    due_date        = models.DateField('Due date', default=None, null=True, blank=True)
    expiration_date = models.DateField('Exp date', default=None, null=True, blank=True)
    cvv             = models.CharField('CVV', max_length=5, default=None, null=True, blank=True)
    limit           = models.DecimalField("Limit", max_digits=20, decimal_places=2, default=Decimal(0.00))
    available_amount= models.DecimalField("Available Amount", max_digits=20, decimal_places=2, default=Decimal(0.00))
    wallet          = models.ForeignKey(Wallet, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return "card: %s - exp: %s - in: %s" % (self.number, self.expiration_date, self.wallet)
