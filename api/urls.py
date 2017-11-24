from django.conf.urls import url
from rest_framework.authtoken import views as rest_framework_views

from api.views.creditcard_view import ApiCreditCards
from api.views.wallet_view import ApiWallets, ApiCreateWallets
from api.views.purchase_view import ApiPurchase


urlpatterns = [
    url(r'credit-cards/$', ApiCreditCards.as_view()),
    url(r'credit-cards/(?P<number>\d{1,25})/$', ApiCreditCards.as_view()),
    url(r'wallets/$', ApiWallets.as_view()),
    url(r'wallets/create/$', ApiCreateWallets.as_view()),
    url(r'purchase/$', ApiPurchase.as_view()),
    url(r'get_auth_token/$', rest_framework_views.obtain_auth_token, name='get_auth_token')
]
