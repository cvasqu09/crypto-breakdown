from coinbase.wallet.client import Client
from os import environ

coinbase_client = Client(environ["CB_API_KEY"], environ["CB_API_SECRET"])