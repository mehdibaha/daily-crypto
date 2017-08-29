from flask import Flask, request
from gains import get_current_gains

app = Flask(__name__)

@app.route('/')
def index():
    return f'no user selected. go to {request.url}user'

@app.route('/<user>')
def entry_point(user):
    if user not in ['mehdi', 'ali']:
        return 'no user found.'
    gains, total = get_current_gains(user)
    s = [f'Your total gains are: {total}€']
    s += [f'Gains in {curr}: {amt}€' for curr, amt in gains.items()]
    return '<br>'.join(s)

if __name__ == '__main__':
    app.run(debug=True)
