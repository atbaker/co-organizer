from flask import Flask
from twilio import twiml


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    r = twiml.Response()
    r.say('Welcome to Django-district! Connecting you to an organizer now.')
    r.dial('+17036230231')
    return str(r)

if __name__ == '__main__':
    app.run()
