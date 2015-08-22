from flask import Flask, request
from twilio import twiml
from twilio.rest import TwilioRestClient


app = Flask(__name__)
client = TwilioRestClient()

meetup_config = {
    'phone_number': None,
    'organizers': []
}


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    """Twilio Voice URL - says welcome message and connects to organizer"""
    r = twiml.Response()
    r.say('Welcome to Django-district! Connecting you to an organizer now.')
    r.dial(organizers[0])
    return str(r)

@app.route('/message', methods=['GET', 'POST'])
def message():
    """Twilio SMS URL - used to configure app"""
    # Get from number from POST request
    organizer = request.form['From']
    meetup_config['organizers'].append(organizer)

    # Store the 'to' number
    phone_number = request.form['To']
    meetup_config['phone_number'] = phone_number

    # Reply to the organizer and say 'hi'
    message = client.messages.create(
        body="Hi organizer! I'm your new Meetup assistant!",
        to=organizer,
        from_=phone_number,
    )


if __name__ == '__main__':
    app.run()
