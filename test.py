# This file is responsible for acquiring customers and getting necessary users' information
import requests


print('Welcome to Lolita\'s Flight Club.\nWe find the best flight deals and email you.')
first_name = input('What is your first name?\n').title()
last_name = input('What is your last name?\n').title()
email = input('What is your email?\n')
email_confirm = input('Type your email again.\n')
if email == email_confirm:
    print("You're in the club!")

    parameters = {
        'user': {
            'firstName': first_name,
            'lastName': last_name,
            'email': email_confirm
        }
    }

    # Syncs a new sheet(tab) in the Flight deals Google sheet with Sheety and
    # Uses the Sheety API to POST the data that the user enters into the new sheet in the Flight Deals Google Sheet
    response = requests.post(url=sheety_endpoint, json=parameters)
    data = response.json()
    print(data)
else:
    print('Your email does not match. Please try again')