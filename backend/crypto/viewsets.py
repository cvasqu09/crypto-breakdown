from rest_framework import status, serializers
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
                Account.objects.create_account(account)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'])
    def buys(self, request):
        account_id = request.query_params.get('account_id')
        print('account id', account_id)
        buy_data = coinbase_client.get_buys(account_id)
        buys = Buy.objects.filter(account__id=account_id)
        existing_buy_ids = [str(b.id) for b in buys]
        existing_account_ids = Account.objects.all().values_list('id', flat=True)
        existing_account_ids = [str(account_id) for account_id in existing_account_ids]
        for buy in buy_data["data"]:
            if buy["id"] not in existing_buy_ids:
                data_to_serialize = {
                    **buy,
                    "account": account_id
                }
                new_buy = BuySerializer(data=data_to_serialize)
                try:
                    if account_id not in existing_account_ids:
                        account = coinbase_client.get_account(account_id)
                        Account.objects.create_account(account)
                    new_buy.is_valid(raise_exception=True)
                    new_buy.save()
                except serializers.ValidationError as e:
                    print('e', e)

        return Response(status=status.HTTP_204_NO_CONTENT)


class AccountViewSet(ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    http_method_names = ['get']


class BuyViewSet(ModelViewSet):
    serializer_class = BuySerializer

    @action(detail=False, methods=['post'])
    def refresh(self):
        return Response(status=status.HTTP_204_NO_CONTENT)
