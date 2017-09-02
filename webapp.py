import os

from flask import Flask, render_template, request
from gains import get_current_gains, get_fake_gains

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

NAT_CURR = 'EUR'

@app.route('/')
def index():
    return f'no user selected. go to {request.url}user'

@app.route('/<user>')
def entry_point(user):
    if user not in ['mehdi', 'ali']:
        return 'no user found.'
    try:
        gains, total = get_current_gains(user)
    except Exception as e:
        print(f'following error has occured\n{e}')
        gains, total = get_fake_gains(user)
    return render_template('index.html', gains=gains, total=total)

@app.template_filter('prettify')
def prettify(amt):
    currencies = {'USD': '$', 'EUR': '€', 'GBP': '£'}
    nat_curr = os.environ.get('NAT_CURRENCY', 'EUR')
    fmt = '+' if amt > 0 else '' # Adding value sign
    fmt += '{:.2f}'.format(amt) # Setting float precision
    fmt += currencies[nat_curr] # Add currency symbol
    return fmt

if __name__ == '__main__':
    app.run(debug=True)
