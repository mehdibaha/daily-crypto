import coinbase
import os

from coinbase.wallet.client import Client

def get_current_gains(user):
    api_key, api_secret = os.environ.get(f'API_KEY_{user.upper()}'), os.environ.get(f'API_SECRET_{user.upper()}')
    client = Client(api_key, api_secret)

    accounts = client.get_accounts()['data']
    gains, total = {}, 0
    for acc in accounts:
        id, curr = acc['id'], acc['balance']['currency']
        if user == 'mehdi':
            nat_bal = float(acc['native_balance']['amount'])
        if user == 'ali':
            nat_bal = 500
        trans = client.get_transactions(id)['data']
        nat_trans = [float(t['native_amount']['amount']) for t in trans]
         if user == 'mehdi':
            nat_payments = sum(nat_trans)
        if user == 'ali':
            nat_payments = sum([t for t in nat_trans if t > 0])
        gain = nat_bal - nat_payments
        total += gain
        gains[curr] = '{:.2f}'.format(gain)
    total = '{:.2f}'.format(total)
    return gains, total
