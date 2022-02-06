from django.db import models

decimal_fields = {"decimal_places": 8, "max_digits": 30}


class CryptoTransaction(models.Model):
    class TransactionType(models.TextChoices):
        BUY = 'buy',
        SEND = 'send'

    class TransactionStatus(models.TextChoices):
        PENDING = 'pending'
        COMPLETED = 'completed'
        FAILED = 'failed'
        EXPIRED = 'expired'
        CANCELLED = 'canceled'

    id = models.UUIDField(primary_key=True)
    type = models.CharField(choices=TransactionType.choices, max_length=10)
    status = models.CharField(choices=TransactionStatus.choices, max_length=50)
    created_at = models.DateTimeField()
    amount_value = models.DecimalField(**decimal_fields)
    amount_currency = models.CharField(max_length=10)
    native_amount_value = models.DecimalField(**decimal_fields)
    native_amount_currency = models.CharField(max_length=10)


class AccountModelManager(models.Manager):
    def create_account(self, account):
        Account.objects.create(
            id=account["id"],
            name=account["name"],
            balance_amount=account["balance"]["amount"],
            balance_currency=account["balance"]["currency"],
            native_amount=account["native_balance"]["amount"],
            native_currency=account["native_balance"]["currency"]
        )


class Account(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=128)
    balance_amount = models.DecimalField(**decimal_fields)
    balance_currency = models.CharField(max_length=10)
    native_amount = models.DecimalField(**decimal_fields)
    native_currency = models.CharField(max_length=10)

    objects = AccountModelManager()


class Buy(models.Model):
    class BuyStatus(models.TextChoices):
        CANCELLED = 'canceled'
        CREATED = 'created'
        COMPLETED = 'completed'

    id = models.UUIDField(primary_key=True)
    account = models.ForeignKey('Account', on_delete=models.CASCADE)
    status = models.CharField(choices=BuyStatus.choices, max_length=10)
    created_at = models.DateTimeField(null=True)
    fees = models.JSONField(default=list)
    amount = models.JSONField(default=dict)
    subtotal = models.JSONField(default=dict)
    total = models.JSONField(default=dict)

