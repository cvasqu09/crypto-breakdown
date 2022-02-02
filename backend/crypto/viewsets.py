from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from crypto import coinbase_client
from crypto.models import Account
from crypto.serializers import AccountSerializer


class AccountViewSet(ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    @action(detail=False, methods=['post'])
    def refresh(self, request):
        account_data = coinbase_client.get_accounts()
        account_ids = [account["id"] for account in account_data["data"]]
        accounts = Account.objects.filter(id__in=account_ids)
        accounts_dict = {[str(account.id)]: account for account in accounts}

        for account in account_data["data"]:
            if account["id"] in accounts_dict:
                account_to_update = accounts_dict[account["id"]]
                account_to_update["balance_amount"] = account["balance"]["amount"]
                account_to_update["balance_currency"] = account["balance"]["currency"]
                account_to_update["native_amount"] = account["native_balance"]["amount"]
                account_to_update["native_currency"] = account["native_balance"]["currency"]
                account_to_update.save()
            else:
                Account.objects.create(
                    id=account["id"],
                    name=account["name"],
                    balance_amount=account["balance"]["amount"],
                    balance_currency=account["balance"]["currency"],
                    native_amount=account["native_balance"]["amount"],
                    native_currency=account["native_balance"]["currency"]
                )

        return Response(status=status.HTTP_204_NO_CONTENT)