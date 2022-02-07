from rest_framework import serializers
from crypto.models import Account, Buy, FavoriteWallet
from crypto.validations import JsonSchemaValidator

amount_schema = {
    "type": "object",
    "properties": {
        "amount": {
            "type": "number",
        },
        "currency": {
            "type": "string",
        },
    },
    "required": ["amount", "currency"]
}


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'


class BuySerializer(serializers.ModelSerializer):
    class Meta:
        model = Buy
        fields = '__all__'

    def validate_fees(self, data):
        for fee in data:
            JsonSchemaValidator.validate(fee, amount_schema)
        return data

    def validate_amount(self, data):
        JsonSchemaValidator.validate(data, amount_schema)
        return data

    def validate_subtotal(self, data):
        JsonSchemaValidator.validate(data, amount_schema)
        return data

    def validate_total(self, data):
        JsonSchemaValidator.validate(data, amount_schema)
        return data


class FavoriteWalletSerializer(serializers.ModelSerializer):
    wallet = AccountSerializer(read_only=True)

    class Meta:
        model = FavoriteWallet
        fields = ['id', 'wallet']
