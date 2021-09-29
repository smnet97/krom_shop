from rest_framework import serializers


class CallbackResponseSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    transactionId = serializers.IntegerField()
    amount = serializers.IntegerField()
    transaction_type = serializers.CharField(max_length=30)