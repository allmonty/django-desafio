from django.contrib import admin
from api.models import *
from django import forms

# Register your models here.

class CreditCardAdmin(admin.ModelAdmin):
    list_display = ['number', 'due_date', 'expiration_date', 'cvv', 'limit', 'avilable_amount']
    list_filter = ['due_date', 'expiration_date', 'limit', 'avilable_amount']

admin.site.register(CreditCard, CreditCardAdmin)