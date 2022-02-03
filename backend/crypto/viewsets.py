from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet

from crypto import coinbase_client
from crypto.models import Account, Buy
from crypto.serializers import AccountSerializer, BuySerializer


class RefreshViewSet(ViewSet):
    http_method_names = ['post']

    @action(detail=False, methods=['post'])
    def accounts(self, request):
        account_data = coinbase_client.get_accounts()
        print('account data', account_data)
        account_ids = [account["id"] for account in account_data["data"]]
        accounts = Account.objects.filter(id__in=account_ids)
        accounts_dict = {str(account.id): account for account in accounts}
        for account in account_data["data"]:
            if account["id"] in accounts_dict:
                account_to_update: Account = accounts_dict[account["id"]]
                account_to_update.balance_amount = account["balance"]["amount"]
                account_to_update.balance_currency = account["balance"]["currency"]
                account_to_update.native_amount = account["native_balance"]["amount"]
                account_to_update.native_currency = account["native_balance"]["currency"]
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

    @action(detail=False, methods=['post'])
    def buys(self, request):
        account_id = request.query_params.get('account_id')
        print('account id', account_id)
        buy_data = coinbase_client.get_buys(account_id)
        buys = Buy.objects.filter(account__id=account_id)
        existing_buy_ids = [str(b.id) for b in buys]
        for buy in buy_data["data"]:
            # if buy["id"] not in existing_buy_ids:
            #     fields = Buy._meta.fields
            #     data_to_serialize = {}
            #     for field in fields:
            #         buy_field = buy.get(field, None)
            #         if not isinstance()
            #     new_buy = BuySerializer({
            #         "id": buy["id"],
            #         "account": account_id,
            #         "status": buy["status"],
            #         "created_at": buy["created_at"]
            #     })
            print('buy', buy)
            print(type(buy["fees"]))

        return Response(data=buys)


class AccountViewSet(ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    http_method_names = ['get']


class BuyViewSet(ModelViewSet):
    serializer_class = BuySerializer

    @action(detail=False, methods=['post'])
    def refresh(self):
        return Response(status=status.HTTP_204_NO_CONTENT)
