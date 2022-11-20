
# Twilio Offical Example: https://www.twilio.com/blog/verify-email-address-python-flask-twilio-verify

import os
from dotenv import load_dotenv
from flask import Flask, request, render_template, redirect, session, url_for
from twilio.rest import Client as TwilioClient


load_dotenv()


class Configuration(object):
    SECRET_KEY = 'secretkeylol'
    TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
    TWILIO_VERIFY_SERVICE = os.environ.get('TWILIO_VERIFY_SERVICE')
    SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY') 



# Create flask application and add configuration settings
app = Flask(__name__)
app.config.from_object(Configuration)

# Create a twilio client
twilio_client = TwilioClient(Configuration.TWILIO_ACCOUNT_SID, Configuration.TWILIO_AUTH_TOKEN)



## ROUTES

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        to_email = request.form['email']
        session['to_email'] = to_email
        send_verification(to_email)
        return redirect(url_for('generate_verification_code'))
    return render_template('index.html')


    
def send_verification(to_email):
    verification = twilio_client.verify \
        .services(Configuration.TWILIO_VERIFY_SERVICE) \
        .verifications \
        .create(to=to_email, channel='email')
    print(verification.sid)


    

@app.route('/verifyme', methods=['GET', 'POST'])
def generate_verification_code():
    to_email = session['to_email']
    error = None
    if request.method == 'POST':
        verification_code = request.form['verificationcode']
        if check_verification_token(to_email, verification_code):
            return render_template('success.html', email = to_email)
        else:
            error = "Invalid verification code. Please try again."
            return render_template('verifypage.html', error = error)
    return render_template('verifypage.html', email = to_email)


def check_verification_token(phone, token):
    check = twilio_client.verify \
        .services(Configuration.TWILIO_VERIFY_SERVICE) \
        .verification_checks \
        .create(to=phone, code=token)    
    return check.status == 'approved'



    