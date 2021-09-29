from apelsinuz.serializers import CallbackResponseSerializer
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from shop.models import OrderModel

import json
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def check_apelsin(request):
    data = json.loads(request.body)
    serializer = CallbackResponseSerializer(data=data)
    
    if serializer.is_valid():
        data = serializer.validated_data
        if data['order_id']:
            order = OrderModel.objects.get(pk=data['order_id'])
            if order.amount*100 == data['amount']:
                order.payment_status = 3
                order.save()
                return JsonResponse({"status": True})
        
    return JsonResponse({"status": False})