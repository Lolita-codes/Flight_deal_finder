from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

data_manager = DataManager()
sheet_data = data_manager.get_info()
flight_search = FlightSearch()
notification_manager = NotificationManager()


# Checks if sheet_data contains any values for the 'iataCode' key and add the missing codes if not
# iataCode is the  International Air Transport Association (IATA) code
# which helps to identify airports and metropolitan areas.
if sheet_data[0]["iataCode"] == '':
    for i in sheet_data:
        i["iataCode"] = flight_search.get_iata_code(i['city'])
    # Updates the Google sheet
    data_manager.sorted_info = sheet_data
    data_manager.update_info()


# Searches for the available flight deals from the origin_city to all the destinations in the Google Sheet
for i in sheet_data:
    deal = flight_search.get_flight_deal(code=i['iataCode'], city=i['city'])
    # Handles destinations with no flights available so the code doesn't break and crash in these situations.
    if deal is None:
        continue
    # Checks if any of the flights found are cheaper than the Lowest Price listed in the Google Sheet
    #  Uses the Twilio API to send an SMS with enough information to book the flight
    if deal.price < i['lowestPrice']:
        users = data_manager.get_customer_emails()
        emails = [row["email"] for row in users]
        names = [row["firstName"] for row in users]

        # Formats the message or email
        content = f"Low price alert! Only £{deal.price} to fly from {deal.origin_city}-{deal.origin_airport} " \
                f"to {deal.destination_city}-{deal.destination_airport}, from {deal.out_date} to {deal.return_date}."

        # Because the max_stopovers is set to 0,
        # this handles if there are no direct flights from origin city to destination i.e. sends a message.
        if deal.stop_overs > 0:
            content += f"\nFlight has {deal.stop_overs} stop over, via {deal.via_city}."
            print(content)
        notification_manager.send_msg(content)

        # Sends an email with the flight deal
        link = f'https://www.google.co.uk/flights?hl=en#flt=' \
               f'{deal.origin_airport}.{deal.destination_airport}.{deal.out_date}*{deal.destination_airport}.' \
               f'{deal.origin_airport}.{deal.return_date}'

        notification_manager.send_emails(emails=emails, message=content, link=link)







