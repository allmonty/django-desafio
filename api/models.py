from django.db import models
from django.contrib.auth.models import User

from decimal import Decimal


class Wallet(models.Model):
    chosen_limit    = models.DecimalField("Chosen Limit", max_digits=20, decimal_places=2, default=Decimal(0.00))
    user            = models.OneToOneField(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return "%s's wallet - limit: %s" % (self.user, self.chosen_limit)


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
