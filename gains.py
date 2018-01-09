import coinbase
import os

from coinbase.wallet.client import Client
from coinbase.wallet.model import APIObject

# source: https://support.coinbase.com/customer/portal/articles/2109597-buy-sell-bank-transfer-fees
SELL_FEE = 0.0149

def get_current_gains(user):
    user = 'ali' if user is 'alix' else user
    api_key, api_secret = os.environ.get(f'API_KEY_{user.upper()}'), os.environ.get(f'API_SECRET_{user.upper()}')
    client = Client(api_key, api_secret)
    nat_curr = os.environ.get('NAT_CURRENCY', 'EUR')

    accounts = client.get_accounts()
    gains = []
    for acc in accounts.data:
        # Getting general info
        id, curr, name = acc.id, acc.balance.currency, acc.name
        # Getting coin balance
        coin_balance = float(acc.balance.amount)
        # Getting market price
        sell_price = float(client._make_api_object(client._get('v2', 'prices', f'{curr.upper()}-{nat_curr}', 'sell'), APIObject).amount)
        buy_price = float(client._make_api_object(client._get('v2', 'prices', f'{curr.upper()}-{nat_curr}', 'buy'), APIObject).amount)
        # Getting fiat payments and balance
        fiat_balance = coin_balance*sell_price*(1-SELL_FEE)
        fiat_buys = sum([float(b['total']['amount']) for b in client.get_buys(id).data])

        gains.append({
            'currency': curr,
            'name': name,
            'fiat_buys': fiat_buys,
            'fiat_balance': fiat_balance,
            'coin_balance': coin_balance,
            'buy_price': buy_price,
            'sell_price': sell_price,
        })

    return gains

def get_fake_gains(user):
    gains = []
    gains.append({'currency': 'ETH', 'name': 'Ethereum', 'fiat_buys': -10.5, 'fiat_balance': 200, 'coin_balance': 0.12, 'buy_price': 500.12, 'sell_price': 400.34})
    gains.append({'currency': 'BTC', 'name': 'Bitcoin', 'fiat_buys': 20.5, 'fiat_balance': 100, 'coin_balance': 0.23, 'buy_price': 100.12, 'sell_price': 200.34})
    return gains




