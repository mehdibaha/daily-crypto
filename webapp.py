from flask import Flask, request
from gains import get_current_gains

app = Flask(__name__)

@app.route('/')
def index():
    root = request.url.split('com')[0] + 'com'
    return f'no user selected. go to {root}/your_user'

@app.route('/<user>')
def entry_point(user):
    if user not in ['mehdi', 'ali']:
        return 'no user found.'
    if user == 'mehdi':
        gains, total = get_current_gains()
    if user == 'ali':
        gains, total = {'ETH': '0.0', 'BTC': '0.0'}, '0.0'
    s = [f'Your total gains are: {total}€']
    s += [f'Gains in {curr}: {amt}€' for curr, amt in gains.items()]
    return '<br>'.join(s)

if __name__ == '__main__':
    app.run(debug=True)
