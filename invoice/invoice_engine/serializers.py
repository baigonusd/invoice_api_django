from rest_framework import serializers
from .models import Contract, Invoice, Product, InvoiceItem
from rest_framework.serializers import ValidationError
import requests


class ContractSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Contract
        # fields = ('owner', 'title')
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('title', 'price')


class InvoiceSerializer(serializers.ModelSerializer):
    user = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Invoice
        fields = ('user', 'number', 'contract', 'date')

    def create(self, validated_data):
        user = validated_data["user"]
        try:
            instance = user.contracts.get(pk=validated_data["contract"].pk)
        except Contract.DoesNotExist:
            raise ValidationError(
                {"Error": "You don't have a permission for this contract"})

        return Invoice.objects.create(**validated_data)


class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = ('invoice', 'product', 'qty', 'price')

    def create(self, validated_data):
        validated_data["amount"] = validated_data["qty"] * \
            validated_data["price"]

        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user

        if user == validated_data["invoice"].user:
            return InvoiceItem.objects.create(**validated_data)
        else:
            raise ValidationError(
                {"Error": "You don't have a permission for this invoice"})


class ListOfInvoicesSerializer(serializers.ModelSerializer):
    invoice_items = InvoiceItemSerializer(many=True)

    class Meta:
        model = Invoice
        fields = ('user', 'number', 'contract', 'date')

    # contracts = Contract.objects.filter(user=user, pk=validated_data["contract"].pk).exists()
    # if validated_data["contract"] in contracts:
    #     return Invoice.objects.create(**validated_data)
    # else:
    #     raise ValidationError(
    #         {"Error": "You don't have a permission for this contract"})

    # class EmailSerializer(serializers.ModelSerializer):
    #     class Meta:
    #         model = Invoice
    #         fields = ('user', 'title', 'contract',
    #                   'product', 'price', 'number', 'sum')
    # fields = "__all__"
