from uuid import UUID

from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet

from crypto import coinbase_client
from crypto.models import Account, Buy, FavoriteWallet
from crypto.serializers import AccountSerializer, BuySerializer, FavoriteWalletSerializer


class RefreshViewSet(ViewSet):
    http_method_names = ['post']

    @action(detail=False, methods=['post'])
    def accounts(self, request):
        account_data = coinbase_client.get_accounts(limit=100)
        # print('account data', account_data)
        valid_accounts = []
        valid_account_ids = []
        for account in account_data["data"]:
            try:
                uuid_obj = UUID(account["id"])
                valid_accounts.append(account)
                valid_account_ids.append(str(uuid_obj))
            except ValueError:
                continue

        accounts = Account.objects.filter(id__in=valid_account_ids)
        accounts_dict = {str(account.id): account for account in accounts}
        for account in valid_accounts:
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
    http_method_names = ['get', 'post']

    @action(detail=False, methods=['get', 'post'])
    def favorites(self, request):
        # TODO: replace with logged in user
        user_model = get_user_model()
        me = user_model.objects.get(id=1)
        if request.method == 'GET':
            favorites = FavoriteWallet.objects.filter(user=me)
            serializer = FavoriteWalletSerializer(favorites, many=True)
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        elif request.method == 'POST':
            body = request.data
            ids = body["ids"]
            user_favorites = FavoriteWallet.objects.filter(user=me)
            user_favorites = [str(favorite["id"]) for favorite in user_favorites]
            user_wallets = list(Account.objects.filter(user=me))
            for favorite_id in ids:
                if str(favorite_id) not in user_favorites:
                    wallet_to_favorite = next(wallet for wallet in user_wallets if str(wallet.id) == favorite_id)
                    FavoriteWallet.objects.create(user=me, wallet=wallet_to_favorite)

            return Response(status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def buys(self, request, pk=None):
        buys = list(Buy.objects.filter(account__id=pk))

        account = Account.objects.get(id=pk)
        buys_serializer = BuySerializer(buys, many=True)

        buys_data = {
            "data": buys_serializer.data,
            "symbol":  account.balance_currency
        }

        return Response(status=status.HTTP_200_OK, data=buys_data)


class CurrencyViewSet(ViewSet):
    def list(self, request):
        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def exchange_rates(self, request):
        rates_data = coinbase_client.get_exchange_rates(currency='USD')
        return Response(status=status.HTTP_200_OK, data=rates_data)