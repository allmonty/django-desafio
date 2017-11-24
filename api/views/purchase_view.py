from django.shortcuts import render
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.core import serializers
from decimal import Decimal
import json

from rest_framework import authentication, permissions
from django.contrib.auth.models import User, Group
from rest_framework.authtoken.models import Token

from api.models import CreditCard, Wallet
from api.wallet import Wallet_Manager


def purchaseResponseJSON(wallet, maximum_limit, available_credit, value):
		response_json = {
						"value": value,
						"wallet":{
							"user": str(wallet.user),
							"maximum_limit": maximum_limit,
							"available_credit": available_credit,
							"chosen_limit":	wallet.chosen_limit
							}
						}
		return response_json

class ApiPurchase(APIView):

	renderer_classes = (JSONRenderer, )

	authentication_classes = (authentication.TokenAuthentication,)
	permission_classes = (permissions.IsAuthenticated,)

	def post(self, request):
		body_unicode = request.body.decode('utf-8')
		body = json.loads(body_unicode)

		user = None
		try:
			user = User.objects.get(username=request.user)
		except Exception as e:
			return Response({'error': True, 'msg': 'Error: User not found', "exception": str(e)}, status=status.HTTP_404_NOT_FOUND)

		wallet = Wallet.objects.get(user=user)
		
		# =============================== #

		value = 0.0
		try:
			value = Decimal(body['value'])
		except Exception as e:
			return Response({'error': True, 'msg': 'Error: problem processing value', "exception": str(e)}, status=status.HTTP_400_BAD_REQUEST)
		
		maximum_limit = Wallet_Manager.calculate_maximum_limit(wallet)
		available_credit = Wallet_Manager.calculate_available_credit(wallet)

		Wallet_Manager.make_purchase(wallet, maximum_limit, available_credit, value)

		wallet = Wallet.objects.get(user=user)

		wallet_json = purchaseResponseJSON(wallet, maximum_limit, available_credit, value)
		return Response(wallet_json)


