import coinbase
import os

from coinbase.wallet.client import Client
from coinbase.wallet.model import APIObject

def get_current_gains(user):
    api_key, api_secret = os.environ.get(f'API_KEY_{user.upper()}'), os.environ.get(f'API_SECRET_{user.upper()}')
    client = Client(api_key, api_secret)

    accounts = client.get_accounts()['data']
    gains, total = {}, 0
    for acc in accounts:
        id, curr = acc['id'], acc['balance']['currency']
        if curr == 'EUR':
            continue
        trans = client.get_transactions(id)['data']
        trans = [t for t in trans if t['type'] == 'buy']
        if user == 'ali':
            res = client._make_api_object(client._get('v2', 'prices', f'{curr.upper()}-EUR', 'spot'), APIObject)
            spot_price = float(res.amount)
            nat_bal = sum([float(t['amount']['amount']) * spot_price for t in trans])
        if user == 'mehdi':
            nat_bal = float(acc['native_balance']['amount'])
        nat_payments = sum([float(t['native_amount']['amount']) for t in trans])
        gain = nat_bal - nat_payments
        total += gain
        if gain > 0:
            gains[curr] = '{:.2f}'.format(gain)
    total = '{:.2f}'.format(total)
    return gains, total
