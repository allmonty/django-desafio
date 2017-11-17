from django.db import models

# Create your models here.
class CreditCard(models.Model):
    number          = models.CharField('Number', max_length=255, default=None, null=True, blank=True)
    due_date        = models.DateField('Due date', default=None, null=True, blank=True)
    expiration_date = models.DateField('Exp date', default=None, null=True, blank=True)
    cvv             = models.CharField('CVV', max_length=255, default=None, null=True, blank=True)
    limit           = models.CharField('Limit', max_length=255, default=None, null=True, blank=True)
    avilable_amount = models.CharField('Available amount', max_length=255, default=None, null=True, blank=True)
    wallet          = models.ForeignKey('Wallet', null=True, on_delete=models.CASCADE)

class Wallet(models.Model):
    owner_name = models.CharField('Owner name', max_length=255, default=None, null=True, blank=True)

    def __str__(self):
        return "%s's wallet" % (self.owner_name)