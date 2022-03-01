from rest_framework import serializers
from .models import Contract, Invoice


class ContractSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Contract
        # fields = ('owner', 'title')
        fields = "__all__"
