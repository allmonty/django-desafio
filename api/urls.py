from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'credit-cards/$', views.ApiCreditCards.as_view())
]