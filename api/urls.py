from django.conf.urls import url
from api.views.creditcard_view import ApiCreditCards
from api.views.wallet_view import ApiWallets

urlpatterns = [
    url(r'credit-cards/$', ApiCreditCards.as_view()),
    url(r'credit-cards/(?P<number>\d{1,25})/$', ApiCreditCards.as_view()),
    url(r'wallets/$', ApiWallets.as_view()),
    url(r'wallets/(?P<email>\S+@\S+com(\W\w{1,2})?)/$', ApiWallets.as_view()),
]
