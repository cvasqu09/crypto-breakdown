from datetime import datetime
from uuid import UUID, uuid4

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Sum
from rest_framework import status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet

from crypto import coinbase_client
from crypto.models import Account, Buy, FavoriteWallet
from crypto.serializers import AccountSerializer, BuySerializer, FavoriteWalletSerializer, CoinbaseBuySerializer


class PriceViewSet(ViewSet):
    http_method_names = ['get', 'post']

    def list(self, request):
        crypto_currency = request.query_params.get('crypto', None)
        native_currency = request.query_params.get('native', 'USD')

        try:
            buy_price = coinbase_client.get_sell_price(currency_pair=f"{crypto_currency}-{native_currency}")
            return Response(status=status.HTTP_200_OK, data=buy_price)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": 'Error retrieving buy price'})

    @action(detail=False, methods=['post'])
    def bulk(self, request):
        data = request.data
        symbols = data["symbols"]
        native_currency = 'USD'
        buy_prices = {}
        print('symbols', symbols)
        for symbol in symbols:
            buy_price = coinbase_client.get_sell_price(currency_pair=f"{symbol}-{native_currency}")
            buy_prices[symbol] = buy_price
        return Response(status=status.HTTP_200_OK, data=buy_prices)


class BreakdownViewSet(ViewSet):
    http_method_names = ['get']

    def list(self, request):
        accounts = list(Account.objects.all())
        breakdown = {}
        for account in accounts:
            current_account_breakdown = Account.objects.get_account_breakdown(str(account.id))
            if current_account_breakdown:
                breakdown[str(account.id)] = current_account_breakdown
        return Response(status=status.HTTP_200_OK, data=breakdown)


class RefreshViewSet(ViewSet):
    http_method_names = ['post']

    @action(detail=False, methods=['post'])
    def accounts(self, request):
        account_data = coinbase_client.get_accounts(limit=100)
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
    queryset = Account.objects.all().order_by('-balance_amount')
    serializer_class = AccountSerializer
    http_method_names = ['get', 'post']

    @action(detail=False, methods=['get'])
    def breakdown(self, request):
        breakdown = {}

        total_native_spent = self.queryset.aggregate(Sum('native_amount'))
        breakdown['total_spent'] = total_native_spent['native_amount__sum']

        all_buys = Buy.objects.all()
        total_fees = 0
        for buy in all_buys:
            fees = buy.fees
            total_fees += sum(float(fee["amount"]["amount"]) for fee in fees)
        breakdown["total_fees"] = total_fees

        return Response(status=status.HTTP_200_OK, data=breakdown)

    @action(detail=False, methods=['get', 'post'])
    def favorites(self, request):
        # TODO: replace with logged in user
        user_model = get_user_model()
        me = user_model.objects.get(id=1)
        if request.method == 'GET':
            favorites = FavoriteWallet.objects.filter(user=me)
            serializer = FavoriteWalletSerializer(favorites, many=True)
            return_data = {wallet["wallet"]["id"]: wallet for wallet in serializer.data}
            return Response(status=status.HTTP_200_OK, data=return_data)
        elif request.method == 'POST':
            body = request.data
            ids = body["ids"]
            user_favorites = FavoriteWallet.objects.filter(user=me)
            user_favorites_ids = [str(favorite.wallet_id) for favorite in user_favorites]
            for favorite_id in ids:
                if str(favorite_id) not in user_favorites_ids:
                    wallet_to_favorite = Account.objects.get(id=favorite_id)
                    FavoriteWallet.objects.create(user=me, wallet=wallet_to_favorite)
                else:
                    wallet_to_delete = next(wallet for wallet in user_favorites if str(wallet.wallet_id) == favorite_id)
                    wallet_to_delete.delete()

            return Response(status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def buys(self, request, pk=None):
        buys = list(Buy.objects.filter(account__id=pk))

        account = Account.objects.get(id=pk)
        buys_serializer = BuySerializer(buys, many=True)

        buys_data = {
            "data": buys_serializer.data,
            "symbol": account.balance_currency
        }

        return Response(status=status.HTTP_200_OK, data=buys_data)

    @action(detail=False, methods=['post'])
    def import_buy(self, request):
        body = request.data
        balance_currency = body.get("balance_currency")
        cost = body.get("cost")
        fees = body.get("fees")
        print("request", balance_currency, cost, fees, body)
        buy_data = CoinbaseBuySerializer({
            "balance_currency": balance_currency,
            "cost": cost,
            "fees": fees
        }).data

        try:
            account = Account.objects.get(balance_currency__iexact=balance_currency)
            Buy.objects.create(
                id=str(uuid4()),
                account=account,
                status=Buy.BuyStatus.COMPLETED,
                fees=buy_data["fees"],
                amount=buy_data["amount"],
                total=buy_data["total"]
            )
        except Account.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "Currency does not exist."})

        return Response(status=status.HTTP_200_OK, data=body)


class CurrencyViewSet(ViewSet):
    def list(self, request):
        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def exchange_rates(self, request):
        rates_data = coinbase_client.get_exchange_rates(currency='USD')
        return Response(status=status.HTTP_200_OK, data=rates_data)
