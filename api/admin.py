from django.contrib import admin
from api.models import *
from django import forms

# Register your models here.

class WalletAdmin(admin.ModelAdmin):
    list_display = ['user', 'chosen_limit']
    list_filter = ['user', 'chosen_limit']

admin.site.register(Wallet, WalletAdmin)

class CreditCardAdmin(admin.ModelAdmin):
    list_display = ['number', 'wallet', 'due_date', 'expiration_date', 'cvv', 'limit', 'available_amount']
    list_filter = ['due_date', 'expiration_date', 'limit', 'available_amount', 'wallet']

admin.site.register(CreditCard, CreditCardAdmin)