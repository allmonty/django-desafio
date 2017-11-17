from django.contrib import admin
from api.models import *
from django import forms

# Register your models here.

class WalletAdmin(admin.ModelAdmin):
    list_display = ['owner_name']
    list_filter = ['owner_name']

admin.site.register(Wallet, WalletAdmin)

class CreditCardAdmin(admin.ModelAdmin):
    list_display = ['number', 'wallet', 'due_date', 'expiration_date', 'cvv', 'limit', 'avilable_amount']
    list_filter = ['due_date', 'expiration_date', 'limit', 'avilable_amount', 'wallet']

admin.site.register(CreditCard, CreditCardAdmin)