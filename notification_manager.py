import smtplib, ssl
from twilio.rest import Client
import os
from dotenv import load_dotenv
load_dotenv('.env')


account_sid = os.environ['account_sid']
auth_token = os.environ['auth_token']
twilio_account_number = os.environ['twilio_account_number']
my_email = os.environ['my_email']
password = os.environ['password']
phone_number = os.environ['my_phone_number']


# This class is responsible for sending notifications with the flight deal details.
class NotificationManager:
    def __init__(self):
        self.client = Client(account_sid, auth_token)

    # Sends message using Twilio API
    def send_msg(self, content):
        message = self.client.messages \
            .create(
            body=content,
            from_=twilio_account_number,
            to=phone_number
        )

        print(message.sid)

    # Sends an email
    def send_emails(self, emails, message, link):
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 587, context=context) as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            for email in emails:
                connection.sendmail(from_addr=my_email, to_addrs=my_email, msg=f'New Low Price Flight!\n\n{message}\n '
                                                                            f'To book your flight: {link}'.
                                    encode('utf-8')
                                    )
