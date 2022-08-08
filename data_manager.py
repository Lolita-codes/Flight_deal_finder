import requests

sheety_endpoint = 'https://api.sheety.co/f5564c44950431bb1442536746275035/copyOfFlightDeals/prices'
sheety_userendpoint = 'https://api.sheety.co/f5564c44950431bb1442536746275035/copyOfFlightDeals/users'


# This class is responsible for interacting with the Google Sheet(already created) through Sheety API.
class DataManager:
    def __init__(self):
        self.sorted_info = {}
        self.customer_data = {}

    # Gets all the data for prices in the sheet and pass into a sheet_data variable in main.py
    def get_info(self):
        response = requests.get(url=sheety_endpoint)
        data = response.json()
        print(data)
        self.sorted_info = data["prices"]
        return self.sorted_info

    def update_info(self):
        for city in self.sorted_info:
            put_params = {
                'price': {
                    'iataCode': city['iataCode']
                }
            }
            response = requests.put(url=f"{sheety_endpoint}/{city['id']}", json=put_params)
            print(response.text)

    def get_customer_emails(self):
        response = requests.get(url=sheety_userendpoint)
        data = response.json()
        self.customer_data = data["users"]
        return self.customer_data
