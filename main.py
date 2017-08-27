import datetime
import os
import sendgrid

from gains import get_current_gains
from sendgrid.helpers.mail import *

def send_mail(sender, recipient, subject, message):
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email(sender[0], sender[1])
    to_email = Email(recipient)
    content = Content('text/plain', message)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())

def do_job():
    try:
        # Getting gains
        gains, total = get_current_gains()
        # Setting mail
        sender = ('***REMOVED***', 'Crypto Daily')
        recipient = '***REMOVED***'
        date = datetime.datetime.now().strftime('%d/%m/%Y')
        subject = f'[{date}] Your total gains are: {total}€'
        message = '\n'.join([f'Gains in {curr}: {amt}€' for curr, amt in gains.items()])
        # Sending mail
        send_mail(sender, recipient, subject, message)
        print(f'Mail sent to {recipient}')
    except Exception as e:
        print(f'Following error occured: {e}')

do_job()
