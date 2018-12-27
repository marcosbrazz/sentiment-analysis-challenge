from flask import Flask
from flask import request
from model import analyze

app = Flask(__name__)


@app.route('/classify', methods=['POST'])
def classify():
    tweet = request.data.decode("UTF-8")
    result = analyze(tweet)
    if result == 0:
        return 'neutral'
    elif result > 0:
        return 'positive'
    else:
        return 'negative'
