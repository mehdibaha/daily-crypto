import coinbase
import os

from coinbase.wallet.client import Client

def get_current_gains():
    api_key, api_secret = os.environ.get('API_KEY'), os.environ.get('API_SECRET')
    client = Client(api_key, api_secret)

    accounts = client.get_accounts()['data']
    gains, total = {}, 0
    for acc in accounts:
        id, curr, nat_bal = acc['id'], acc['balance']['currency'], float(acc['native_balance']['amount'])
        trans = client.get_transactions(id)['data']
        nat_payments = sum([float(t['native_amount']['amount']) for t in trans])
        gain = nat_bal - nat_payments
        total += gain
        gains[curr] = '{:.2f}'.format(gain)
    total = '{:.2f}'.format(total)
    return gains, total
