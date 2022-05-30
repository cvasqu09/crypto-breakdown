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


class CoinbaseBuySerializer(serializers.Serializer):
    fees = serializers.SerializerMethodField()
    amount = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()

    def get_total(self, instance):
        instance_cost = instance.get("cost")
        return {
            "amount": f"{instance_cost}",
            "currency": "USD"
        }

    def get_amount(self, instance):
        instance_amount = instance.get("amount")
        instance_balance_currency = instance.get("balance_currency")
        return {
            "amount": f"{instance_amount}",
            "currency": f"{instance_balance_currency}"
        }

    def get_fees(self, instance):
        instance_fees = instance.get("fees")
        return [{
            "type": "coinbase",
            "amount": {"amount": f"{instance_fees}", "currency": "USD"},
        }, {
            "type": "bank",
            "amount": {"amount": "0", "currency": "USD"},
        }]


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
