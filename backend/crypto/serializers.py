from rest_framework import serializers

from crypto.models import Account, Buy


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'


class BuySerializer(serializers.ModelSerializer):
    class Meta:
        model = Buy
        fields = '__all__'
        read_only_fields = ['id']

