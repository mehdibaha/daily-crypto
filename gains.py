import coinbase
import os

from coinbase.wallet.client import Client
from coinbase.wallet.model import APIObject

# source: https://support.coinbase.com/customer/portal/articles/2109597-buy-sell-bank-transfer-fees
SELL_FEE = 0.0149

def get_current_gains(user):
    api_key, api_secret = os.environ.get(f'API_KEY_{user.upper()}'), os.environ.get(f'API_SECRET_{user.upper()}')
    client = Client(api_key, api_secret)
    nat_curr = os.environ.get('NAT_CURRENCY', 'EUR')

    accounts = client.get_accounts()['data']
    gains = []
    for acc in accounts:
        id, curr = acc['id'], acc['balance']['currency']
        trans = client.get_transactions(id)['data']
        trans = [t for t in trans if t['type'] == 'buy']
        if not trans: # if user has bought some currency
            continue
        coin_buys = [float(t['amount']['amount']) for t in trans]
        native_buys = [float(t['native_amount']['amount']) for t in trans]
        # Getting spot price
        coin_price = float(client._make_api_object(client._get('v2', 'prices', f'{curr.upper()}-{nat_curr}', 'sell'), APIObject).amount)
        # Calculating final gains
        native_payments = sum(native_buys)
        coin_balance = sum(coin_buys)
        native_balance = sum([t*coin_price*(1-SELL_FEE) for t in coin_buys])
        native_gain = native_balance - native_payments
        gains.append({'currency': curr, 'gain': native_gain, 'native_payments': native_payments, 'coin_balance': coin_balance})
    return gains

def get_fake_gains(user):
    gains = []
    gains.append({'currency': 'ETH', 'gain': -12.3, 'native_payments': 200, 'coin_balance': 0.23})
    gains.append({'currency': 'BTC', 'gain': 53.4, 'native_payments': 100, 'coin_balance': 0.01})
    return gains




