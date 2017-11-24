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

USERS_GROUP = "api_users"

def makeWalletJSON(wallet):
		wallet_json = {
			"user": str(wallet.user),
			"maximum_limit": Wallet_Manager.calculate_maximum_limit(wallet),
			"available_credit": Wallet_Manager.calculate_available_credit(wallet),
			"chosen_limit":	wallet.chosen_limit
			}
		return wallet_json

class ApiWallets(APIView):

	renderer_classes = (JSONRenderer, )

	authentication_classes = (authentication.TokenAuthentication,)
	permission_classes = (permissions.IsAuthenticated,)

	def get(self, request):
		user = None
		try:
			user = User.objects.get(username=request.user)
		except Exception as e:
			return Response({'error': True, 'msg': 'Error: User not found', "exception": str(e)}, status=status.HTTP_404_NOT_FOUND)
		
		wallet = Wallet.objects.get(user=user)

		wallet_json = makeWalletJSON(wallet)
		return Response(wallet_json)

	def post(self, request):
		body_unicode = request.body.decode('utf-8')
		body = json.loads(body_unicode)

		user = None
		try:
			user = User.objects.get(username=request.user)
		except Exception as e:
			return Response({'error': True, 'msg': 'Error: User not found', "exception": str(e)}, status=status.HTTP_404_NOT_FOUND)

		wallet = Wallet.objects.get(user=user)

		try:
			new_chosen_limit = body['chosen_limit']
			Wallet_Manager.edit_chosen_limit(wallet, new_chosen_limit)
		except Exception as e:
			return Response({'error': True, 'msg': 'Error: problem updating chosen limit', "exception": str(e)}, status=status.HTTP_400_BAD_REQUEST)


		wallet_json = makeWalletJSON(wallet)
		return Response(wallet_json)


class ApiCreateWallets(APIView):

	renderer_classes = (JSONRenderer, )

	authentication_classes = (authentication.TokenAuthentication,)
	permission_classes = (permissions.AllowAny,)

	def post(self,request):
		body_unicode = request.body.decode('utf-8')
		body = json.loads(body_unicode)

		user = None
		try:
			user = User.objects.create_user(
                            username = body['username'],
                            password = body['password'],
                            email = body['email'],
                            first_name = body['first_name'],
                            last_name = body['last_name']
				)
		except Exception as e:
			return Response({'error': True, 'msg': 'Error creating user', "exception": str(e)}, status=status.HTTP_400_BAD_REQUEST)
		
		try:
			group = Group.objects.get(name=USERS_GROUP)
			user.groups.add(group)
			user.save()
		except Exception as e:
			return Response({'error': True, 'msg': 'Error creating user permission', "exception": str(e)}, status=status.HTTP_400_BAD_REQUEST)
		
		try:
			Token.objects.create(user=user)
		except Exception as e:
			return Response({'error': True, 'msg': 'Error creating user token', "exception": str(e)}, status=status.HTTP_400_BAD_REQUEST)

		wallet = None
		try:
			wallet = Wallet(
					user = user,
					chosen_limit = 0
				)
			wallet.save()
		except Exception as e:
			return Response({'error': True, 'msg': 'Error saving wallet', "exception": str(e)}, status=status.HTTP_400_BAD_REQUEST)
		
		wallet_json = makeWalletJSON(wallet)

		return Response(wallet_json)
