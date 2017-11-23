from django.shortcuts import render
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from api.models import CreditCard, Wallet
import json
from django.core import serializers

from api.wallet import Wallet_Manager

from django.http import HttpResponse


class ApiWallets(APIView):

	renderer_classes = (JSONRenderer, )

	def get(self, request, email=None):
		if email:
			response = serializers.serialize("json",[Wallet.objects.get(owner_email=email),])
		else:
			response = serializers.serialize("json",Wallet.objects.all())
		return Response(json.loads(response))

	def post(self,request):
		body_unicode = request.body.decode('utf-8')
		body = json.loads(body_unicode)
		wallet = None
		try:
			wallet = Wallet(
					owner_email = body['owner_email'],
					owner_name = body['owner_name'],
					chosen_limit = 0
				)
			wallet.save()
		except Exception as e:
			return Response({'error': True, 'msg': 'Error saving wallet', "exception": str(e)}, status=status.HTTP_400_BAD_REQUEST)
		wallet_json = json.loads(serializers.serialize("json", [Wallet.objects.get(pk=wallet.pk),]))
		return Response(wallet_json)
