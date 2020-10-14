from flask import *
from twilio.rest import Client
import random

app = Flask(__name__)
app.secret_key = 'anything'

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/getOTP', methods = ["POST"])
def getOTP():
    number = request.form['number']
    val = getOTPApi(number)
    if val:
        return render_template('enterOTP.html')

@app.route('/validateOTP', methods = ['POST'])
def validateOTP():
    otp =  request.form['otp']
    if 'response' in session:
        s = session['response']
        session.pop('response', None)
        if s == otp:
            return "You are Authorized. Thank you!"
        else:
            return 'You are not Authorized. Sorry!'

def generateOTP():
    return random.randrange(100000, 999999)

def getOTPApi(number):
    account_sid = 'ACbfd86d77349eae0f9a4d62f9fa982153'
    auth_token = 'd479912913b2cd591871e0bc01195bf8'
    client = Client(account_sid, auth_token)
    otp = generateOTP()
    session['response'] = str(otp)
    body = 'Your OTP is '+ str(otp)
    message = client.messages.create(from_='+442033223576', body=body, to=number)

    if message.sid:
        return True
    else:
        False

if __name__=='__main__':
    app.run(debug=True)