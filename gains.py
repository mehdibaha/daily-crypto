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
    gains, total = {}, 0
    for acc in accounts:
        id, curr = acc['id'], acc['balance']['currency']
        if curr == 'EUR':
            continue
        trans = client.get_transactions(id)['data']
        trans = [t for t in trans if t['type'] == 'buy']
        res = client._make_api_object(client._get('v2', 'prices', f'{curr.upper()}-{nat_curr}', 'sell'), APIObject)
        spot_price = float(res.amount)
        nat_bal = sum([float(t['amount']['amount']) * spot_price for t in trans])
        nat_bal -= SELL_FEE*nat_bal
        nat_payments = sum([float(t['native_amount']['amount']) for t in trans])
        gain = nat_bal - nat_payments
        total += gain
        gains[curr] = gain
    return gains, total

def get_fake_gains(user):
    gains, total =  {'ETH': -51.23, 'BTC': 53.4, 'LTC': 0.0}, 2.1700001
    return gains, total




