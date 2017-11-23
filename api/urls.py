from django.conf.urls import url
from api.views.creditcard_view import ApiCreditCards
from api.views.wallet_view import ApiWallets, ApiCreateWallets

from rest_framework.authtoken import views as rest_framework_views

urlpatterns = [
    url(r'credit-cards/$', ApiCreditCards.as_view()),
    url(r'credit-cards/(?P<number>\d{1,25})/$', ApiCreditCards.as_view()),
    url(r'wallets/$', ApiWallets.as_view()),
    url(r'wallets/create/$', ApiCreateWallets.as_view()),
    # url(r'wallets/(?P<email>\S+@\S+com(\W\w{1,2})?)/$', ApiWallets.as_view()),
    url(r'get_auth_token/$', rest_framework_views.obtain_auth_token, name='get_auth_token')
]
