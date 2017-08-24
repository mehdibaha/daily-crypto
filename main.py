import coinbase
import os

from coinbase.wallet.client import Client

def send_mail(sender, recipient, subject, template_id):
    # Create a text/plain message
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    # Creating mail
    mail = Mail()
    mail.from_email = Email(sender[0], sender[1])
    mail.template_id = template_id
    # Substitutes
    personalization = Personalization()
    personalization.add_to(Email(recipient))
    mail.add_personalization(personalization)
    mail.personalizations[0].add_substitution(Substitution('-subject-', subject))

    # Sending email
    try:
        sg.client.mail.send.post(request_body=mail.get())
    except Exception as error:
        print(f'Email not sent for {recipient}. Following error has occured:\n{error}')

def get_current_gain():
    api_key, api_secret = os.environ.get('API_KEY'), os.environ.get('API_SECRET')
    client = Client(api_key, api_secret)

    accounts = client.get_accounts()['data']
    gains = 0
    for acc in accounts:
        id, curr, nat_bal = acc['id'], acc['balance']['currency'], float(acc['native_balance']['amount'])
        trans = client.get_transactions(id)['data']
        nat_payments = sum([float(t['native_amount']['amount']) for t in trans])
        gains += nat_bal - nat_payments

def do_job():
    gain = get_current_gain()
    sender = ('no-reply@cb-gains.herokuapp.com', 'Coinbase')
    template_id = 'c871e900-fc06-45b5-b037-7ec58821ce27'
    subject = f'Your gains in Coinbase are currently: {gain}€'

    send_mail(sender, 'elmehdi.baha@gmail.com', subject, template_id)
