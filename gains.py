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

    accounts = client.get_accounts()
    gains = []
    for acc in accounts.data:
        id, curr, name = acc.id, acc.balance.currency, acc.name
        trans = client.get_transactions(id).data
        orig_trans = trans
        coin_sells = [float(t.amount.amount) for t in trans if t.type == 'sell']
        trans = [t for t in trans if t.type == 'buy' and 'wallet' not in t.details.payment_method_name.lower()]
        if not trans: # if user has bought some currency
            continue
        coin_buys = [float(t.amount.amount) for t in trans]
        native_buys = [float(t.native_amount.amount) for t in trans]
        # Getting spot price
        sell_price = float(client._make_api_object(client._get('v2', 'prices', f'{curr.upper()}-{nat_curr}', 'sell'), APIObject).amount)
        buy_price = float(client._make_api_object(client._get('v2', 'prices', f'{curr.upper()}-{nat_curr}', 'buy'), APIObject).amount)
        # Calculating final gains
        native_balance = sum([t*sell_price*(1-SELL_FEE) for t in coin_buys])
        native_payments = sum(native_buys)
        coin_balance = sum(coin_buys) + sum(coin_sells)
        gain = native_balance - native_payments
        yield {
            'currency': curr,
            'name': name,
            'gain': gain,
            'native_payments': native_payments,
            'coin_balance': coin_balance,
            'buy_price': buy_price,
            'sell_price': sell_price,
        }
    return gains, orig_trans

def get_fake_gains(user):
    gains = []
    gains.append({'currency': 'ETH', 'name': 'Ethereum', 'gain': -10.5, 'native_payments': 200, 'coin_balance': 0.12, 'buy_price': 500.12, 'sell_price': 400.34})
    gains.append({'currency': 'BTC', 'name': 'Bitcoin', 'gain': 20.5, 'native_payments': 100, 'coin_balance': 0.23, 'buy_price': 100.12, 'sell_price': 200.34})
    return gains




