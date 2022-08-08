import requests
import datetime
from pprint import pprint
from flight_data import FlightData
import os
from dotenv import load_dotenv
load_dotenv('.env')

today = datetime.date.today()
tomorrow = today + datetime.timedelta(days=1)
# strftime formats the date to the required format
tomorrow_format = tomorrow.strftime("%d/%m/%Y")
six_months = today + datetime.timedelta(days=6*30)
check_to = six_months - datetime.timedelta(days=28)
check_to_format = check_to.strftime("%d/%m/%Y")

kiwi_endpoint = 'https://tequila-api.kiwi.com'
header = {'apikey': os.environ['KIWI_API_KEY']}


# This class is responsible for interacting with the Flight Search API.
class FlightSearch:
    # Gets the iataCodes for each city
    def get_iata_code(self, city):
        query = {'term': city, 'location_types': 'city'}
        response = requests.get(url=f'{kiwi_endpoint}/locations/query', params=query, headers=header)
        data = response.json()['locations']
        iata_code = data[0]['code']
        return iata_code

    # Searches for the flight deals from the origin_city to all the destinations in the Google Sheet
    def get_flight_deal(self, code, city):
        query = {
            'fly_from': 'LON',
            'fly_to': code,
            'date_from': tomorrow_format,
            'date_to': check_to_format,
            'nights_in_dst_from': 7,
            'nights_in_dst_to': 28,
            'curr': 'GBP',
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
        }
        response = requests.get(url=f'{kiwi_endpoint}/v2/search', params=query, headers=header)

        try:
            data = response.json()["data"][0]
        except IndexError:
            query['max_stopovers'] = 1
            response = requests.get(url=f'{kiwi_endpoint}/v2/search', params=query, headers=header)
            try:
                data = response.json()["data"][0]
            except IndexError:
                return None
            pprint(data)
            flight_data = FlightData(
                price=data["price"],
                origin_city=data['route'][0]["cityFrom"],
                origin_airport=data['route'][0]["flyFrom"],
                destination_city=data['route'][1]["cityTo"],
                destination_airport=data['route'][1]["flyTo"],
                out_date=data['route'][0]["local_departure"].split("T")[0],
                return_date=data['route'][0]["local_arrival"].split("T")[0],
                stop_overs=1,
                via_city=data['route'][0]['cityTo']
            )
            return flight_data
        else:
            flight_data = FlightData(
                price=data["price"],
                origin_city=data["cityFrom"],
                origin_airport=data["flyFrom"],
                destination_city=data["cityTo"],
                destination_airport=data["flyTo"],
                out_date=data["local_departure"].split("T")[0],
                return_date=data["local_arrival"].split("T")[0]
            )
            return flight_data







