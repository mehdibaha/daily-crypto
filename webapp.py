import logging
import os
import traceback

from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from gains import get_current_gains, get_fake_gains

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

CORS(app)

USER_LIST = ['mehdi', 'juliette']

@app.route('/')
def index():
    return f'no user selected. go to {request.url}user'

@app.route('/<user>')
def entry_point(user):
    if user not in USER_LIST:
        return 'no user found.'
    try:
        gains = get_current_gains(user)
    except Exception as e:
        traceback.print_exc()
        gains = get_fake_gains(user)
    return render_template('index.html', gains=gains)

@app.template_filter('prettify')
def prettify(amt, curr=None):
    currencies = {'USD': '$', 'EUR': '€', 'GBP': '£'}
    nat_curr = os.environ.get('NAT_CURRENCY', 'EUR')
    amt = '{:.2f}'.format(amt) # Setting float precision
    amt += currencies[nat_curr] if not curr else curr
    return amt

if __name__ == '__main__':
    app.run(debug=True)
