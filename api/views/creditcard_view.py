from django.shortcuts import render
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from api.models import CreditCard
import json
from django.core import serializers

from api.wallet import Wallet_Manager

from django.http import HttpResponse


class ApiCreditCards(APIView):

	renderer_classes = (JSONRenderer, )

	def get(self,request, number=None):
		if number:
			response = serializers.serialize("json",[CreditCard.objects.get(number=number),])
		else:
			response = serializers.serialize("json",CreditCard.objects.all())
		return Response(json.loads(response))

	# def post(self,request):
	# 	body_unicode = request.body.decode('utf-8')
	# 	body = json.loads(body_unicode)
	# 	credit_card = None
	# 	try:
	# 		credit_card = CreditCard(
	# 				number = body['number'],
	# 				due_date = body['due_date'],
	# 				expiration_date = body['expiration_date'],
	# 				cvv = body['cvv'],
	# 				limit = body['limit'],
	# 				avilable_amount = body['avilable_amount']
	# 			)
	# 		credit_card.save()
	# 	except Exception as e:
	# 		return Response({'error': True, 'msg': 'Error saving credit card', "exception": str(e)}, status=status.HTTP_400_BAD_REQUEST)
	# 	credit_card_json = json.loads(serializers.serialize("json", [CreditCard.objects.get(pk=credit_card.pk),]))
	# 	return Response(credit_card_json)


