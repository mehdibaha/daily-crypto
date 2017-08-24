import coinbase
import os
import sendgrid

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

from coinbase.wallet.client import Client
from sendgrid.helpers.mail import *

def send_mail(sender, recipient, subject):
    # Create a text/plain message
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    # Creating mail
    from_email = Email(sender[0], sender[1])
    to_email = Email(recipient)
    content = Content('text/plain', '')
    mail = Mail(from_email, subject, to_email, content)
    print(mail.get())
    # Sending email
    try:
        res = sg.client.mail.send.post(request_body=mail.get())
        print(res)
    except Exception as error:
        print(f'Email not sent for {recipient}.\nFollowing error has occured:\n{error}')

def get_current_gains():
    api_key, api_secret = os.environ.get('API_KEY'), os.environ.get('API_SECRET')
    client = Client(api_key, api_secret)

    accounts = client.get_accounts()['data']
    gains = 0
    for acc in accounts:
        id, curr, nat_bal = acc['id'], acc['balance']['currency'], float(acc['native_balance']['amount'])
        trans = client.get_transactions(id)['data']
        nat_payments = sum([float(t['native_amount']['amount']) for t in trans])
        gains += nat_bal - nat_payments
    return '{:.2f}'.format(gains)

def do_job():
    gains = get_current_gains() or 'N/A'
    sender = ('no-reply@cb-24613.com', 'Coinbase')
    subject = f'Your gains in Coinbase are currently: {gains}€'
    recipient = 'elmehdi.baha@gmail.com'
    send_mail(sender, recipient, subject)

do_job()
