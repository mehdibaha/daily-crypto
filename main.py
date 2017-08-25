import coinbase
import os
import sendgrid

from coinbase.wallet.client import Client
from sendgrid.helpers.mail import *

def send_mail(sender, recipient, subject, message):
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email(sender[0], sender[1])
    to_email = Email(recipient)
    content = Content('text/plain', message)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())

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

def do_job():
    try:
        # Getting gains
        gains, total = get_current_gains()
        # Setting mail
        sender = ('***REMOVED***', 'Crypto Daily')
        recipient = '***REMOVED***'
        subject = f'Your gains in Coinbase are currently: {total}€'
        message = '\n'.join([f'Gains in {curr}: {amt}€' for curr, amt in gains.items()])
        # Sending mail
        send_mail(sender, recipient, subject, message)
    except Exception as e:
        print(f'Following error occured: {e}')

do_job()

