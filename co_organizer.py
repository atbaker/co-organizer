from flask import Flask, request
from twilio import twiml
from twilio.rest import TwilioRestClient

app = Flask(__name__)

# Instantiate a Twilio REST API client
client = TwilioRestClient()

FIRST_TIME = 0
ASK_NAME = 1
ASK_COORGANIZERS = 2

meetup_config = {
    'status': FIRST_TIME,
    'phone_number': None,
    'meetup_name': None,
    'organizers': []
}

### Text message response functions

def first_time_setup():
    # Get from number from POST request
    organizer = request.form['From']

    meetup_config['organizers'].append(organizer)

    # Store the 'to' number
    phone_number = request.form['To']
    meetup_config['phone_number'] = phone_number

    # Reply to the organizer and say 'hi'
    message = \
        '''
        Hi organizer! I'm your new Meetup assistant! What's the name of your meetup?
        '''
    client.messages.create(
        body=message,
        to=organizer,
        from_=phone_number,
    )

    # Update status to ASK_NAME
    meetup_config['status'] = ASK_NAME

def set_name():
    # Set the name of the meetup
    meetup_name = request.form['Body']
    meetup_config['meetup_name'] = meetup_name

    message = "Cool! I'm excited to help you organize {0}. Do you have any coorganizers helping you? Tell me their phone numbers" \
        .format(meetup_name)
    client.messages.create(
        body=message,
        to=meetup_config['organizers'][0],
        from_=meetup_config['phone_number'],
    )

### Flask routes

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    """Twilio Voice URL - says welcome message and connects to organizer"""
    r = twiml.Response()
    r.say('Welcome to {0}! Connecting you to an organizer now.'.format(meetup_config['meetup_name']))
    r.dial(meetup_config['organizers'][0])
    return str(r)

@app.route('/message', methods=['GET', 'POST'])
def message():
    """Twilio SMS URL - used to configure app"""
    # Get the status of setting up our number and reply accordingly
    status = meetup_config['status']

    if status == FIRST_TIME:
        first_time_setup()
    elif status == ASK_NAME:
        set_name()

if __name__ == '__main__':
    app.run(debug=True)
