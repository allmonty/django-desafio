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


class ApiCreditCards(APIView):

	renderer_classes = (JSONRenderer, )

	authentication_classes = (authentication.TokenAuthentication,)
	permission_classes = (permissions.IsAuthenticated,)

	def findWallet(self, username):
		wallet = None
		user = User.objects.get(username=username)
		wallet = Wallet.objects.get(user=user)
		return wallet

	def get(self, request, number=None):
		wallet = None
		try:
			wallet = self.findWallet(request.user)
		except Exception as e:
			return Response({'error': True, 'msg': 'Error: User/Wallet not found', "exception": str(e)}, status=status.HTTP_404_NOT_FOUND)

		if number:
			creditcard = CreditCard.objects.filter(wallet=wallet, number=number)
			response = serializers.serialize("json", creditcard)
		else:
			creditcards = CreditCard.objects.filter(wallet=wallet)
			response = serializers.serialize("json", creditcards)
		return Response(json.loads(response))

	def post(self, request, number=None):
		body_unicode = request.body.decode('utf-8')
		body = json.loads(body_unicode)

		wallet = None
		try:
			wallet = self.findWallet(request.user)
		except Exception as e:
			return Response({'error': True, 'msg': 'Error: User/Wallet not found', "exception": str(e)}, status=status.HTTP_404_NOT_FOUND)

		credit_card = None
		try:
			if number:
				credit_card = self.editCreditCard(wallet, number, body)
			else:
				credit_card = self.createCreditCard(wallet, body)
		except Exception as e:
			return Response({'error': True, 'msg': 'Error saving credit card', "exception": str(e)}, status=status.HTTP_400_BAD_REQUEST)


		credit_card_json = json.loads(serializers.serialize("json", [CreditCard.objects.get(pk=credit_card.pk),]))
		return Response(credit_card_json)
	
	def delete(self, request, number=None):
		wallet = None
		try:
			wallet = self.findWallet(request.user)
		except Exception as e:
			return Response({'error': True, 'msg': 'Error: User/Wallet not found', "exception": str(e)}, status=status.HTTP_404_NOT_FOUND)

		if number:
			creditcard = CreditCard.objects.filter(wallet=wallet, number=number)
			
			if not creditcard:
				return Response({'error': True, 'msg': 'Error: Creditcard not found in your wallet'}, status=status.HTTP_404_NOT_FOUND)
			
			creditcard.delete()
			response = serializers.serialize("json", creditcard)
		else:
			return Response({'error': True, 'msg': 'Error: Creditcard number not provided'}, status=status.HTTP_400_BAD_REQUEST)
		return Response(json.loads(response))

	def createCreditCard(self, wallet, data):
		credit_card = None
		credit_card = CreditCard(
						number			= data['number'],
						due_date		= data['due_date'],
						expiration_date	= data['expiration_date'],
						cvv				= data['cvv'],
						limit			= Decimal(data['limit']),
						available_amount= Decimal(data['available_amount']),
						wallet			= wallet
					)
		credit_card.save()
		return credit_card

	def editCreditCard(self, wallet, number, data):
		credit_card = CreditCard.objects.get(number=number, wallet=wallet)

		for key, value in data.items():
			getattr(credit_card, key)
			setattr(credit_card, key, value)
		
		credit_card.save(update_fields=data.keys())

		return credit_card




