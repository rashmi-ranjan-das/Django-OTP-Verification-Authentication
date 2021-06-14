# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
def otpverify(number = 999999, contact_number = 0):
    account_sid = 'AC3e4a64a02e49e0799b514a1e05c6efd8'
    auth_token = '0c4147746e59a80df475d37a4e7591fa'
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
            body=f'Your OTP for registration is {number}',
            from_='+12568011009',
            to=f'+91{contact_number}'
        )

    print(message.sid)
