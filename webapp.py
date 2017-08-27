from flask import Flask
from gains import get_current_gains

app = Flask(__name__)

@app.route('/')
def entry_point():
    gains, total = get_current_gains()
    s = [f'Your total gains are: {total}€']
    s += [f'Gains in {curr}: {amt}€' for curr, amt in gains.items()]
    return '<br>'.join(s)

if __name__ == '__main__':
    app.run(debug=True)