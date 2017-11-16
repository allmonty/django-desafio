from django.contrib import admin
from hello.models import *
from django import forms

# Register your models here.

class GreetingAdmin(admin.ModelAdmin):
    list_display = ['when']
    list_filter = ['when']

admin.site.register(Greeting, GreetingAdmin)