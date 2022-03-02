from rest_framework import serializers
from .models import Contract, Invoice
from rest_framework.serializers import ValidationError
import requests


class ContractSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Contract
        # fields = ('owner', 'title')
        fields = "__all__"


class InvoiceSerializer(serializers.ModelSerializer):
    user = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Invoice
        fields = ('user', 'title', 'contract', 'product', 'price', 'number')

    def create(self, validated_data):
        user = validated_data["user"]
        contracts = Contract.objects.filter(user=user)
        contract = validated_data["contract"]
        if contract in contracts:
            return Invoice.objects.create(**validated_data)
        else:
            raise ValidationError(
                {"Error": "You don't have a permission for this contract"})


# class EmailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Invoice
#         fields = ('user', 'title', 'contract',
#                   'product', 'price', 'number', 'sum')
        # fields = "__all__"
