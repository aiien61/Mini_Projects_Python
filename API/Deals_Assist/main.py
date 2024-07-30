import os
import logging
from typing import List
from pprint import pprint
from dotenv import load_dotenv
from datetime import datetime, timedelta
from flight_search import FlightSearch, TravelAgent
from notification_manager import NotificationManager
from flight_data import FlightData, generate_flight_data
from data_manager import SheetDataManager, Project, Sheet

logger = logging.getLogger(__name__)
logging.basicConfig(filename='flightdeals.log',
                    level=logging.DEBUG,
                    format="{asctime}-{levelname}-{name}-{message}",
                    style='{',
                    datefmt='%Y-%m-%d %H:%M:%S')

load_dotenv()

def find_cheapest_price(all_flight_data: dict):
    if all_flight_data is None or not all_flight_data['data']:
        logger.debug('No flights data')
        return FlightData(
            price='N/A', 
            departure_airport_code='N/A', 
            destination_airport_code='N/A', 
            out_date='N/A', 
            return_date='N/A', 
            stops='N/A'
        )
    
    first_flight: dict = all_flight_data['data'][0]
    cheapest_flight: FlightData = generate_flight_data(first_flight)
    destination: str = cheapest_flight.destination_airport_code

    for flight in all_flight_data['data']:
        price: float = float(flight['price']['grandTotal'])
        if price < cheapest_flight.price:
            cheapest_flight = generate_flight_data(flight)
            print(f'Update cheapest flight to {destination}: ${cheapest_flight.price}')

    return cheapest_flight


def main(sheet: Sheet, agent: TravelAgent, project_name: Project):
    data_manager = SheetDataManager(sheet=sheet, project_name=project_name)
    sheet_data = data_manager.get_destination_data()
    flight_search = FlightSearch(agent, os.getenv('AMADEUS_API_KEY'), os.getenv('AMADEUS_API_SECRET'))
    notification_manager = NotificationManager()
    customer_data: dict = data_manager.get_customer_emails()
    customer_email_list: List[str] = [row['whatIsYourEmail?'] for row in customer_data]
    # pprint(customer_data)
    
    # Update the airport codes in google sheet
    for row in sheet_data:
        if row['iataCode'] == '':
            row['iataCode'] = flight_search.get_destination_code(row['city'])
    
    data_manager.destination_data = sheet_data
    data_manager.update_destination_codes()

    # search for flights
    tomorrow: datetime = datetime.now() + timedelta(days=1)
    six_month_from_today: datetime = datetime.now() + timedelta(days=6 * 30)
    agent.from_time = tomorrow
    agent.to_time = six_month_from_today

    for destination in sheet_data:
        print(f"Getting flights for {destination['city']}")
        agent.destination_city_code = destination['iataCode']
        flights: dict = flight_search.check_flights()
        cheapest_flight = find_cheapest_price(flights)
        print(f"{destination['city']}: NT${cheapest_flight.price}")

        if cheapest_flight.price == 'N/A':
            print(f'No direct flight to {destination["city"]}. Looking for indirect flights...')
            agent.is_direct = False
            stopover_flights: dict = flight_search.check_flights()
            cheapest_flight = find_cheapest_price(stopover_flights)
            print(f"Cheapest indirect flight price is: NT${cheapest_flight.price}")

        # Update google sheet
        if cheapest_flight.price != 'N/A' and cheapest_flight.price < destination['lowestPrice']:
            print(f'Lower price flight found to {destination["city"]}!')
            if cheapest_flight.stops == 0:
                message = f"Low price alert! Only NT${cheapest_flight.price} to fly "\
                          f"from {cheapest_flight.departure_airport_code} to "\
                          f"{cheapest_flight.destination_airport_code}, "\
                          f"on {cheapest_flight.out_date} until {cheapest_flight.return_date}."
            else:
                message = f"Low price alert! Only NT${cheapest_flight.price} to fly "\
                          f"from {cheapest_flight.departure_airport_code} to "\
                          f"{cheapest_flight.destination_airport_code}, "\
                          f"with {cheapest_flight.stops} stop(s) "\
                          f"departing on {cheapest_flight.out_date} and "\
                          f"returning on {cheapest_flight.return_date}."
            notification_manager.send_sms(message_body=message)
            notification_manager.send_whatsapp(message_body=message)
            notification_manager.send_emails(email_list=customer_email_list, email_body=message)


if __name__ == '__main__':
    sheet = Sheet(username=os.getenv('SHEETY_USERNAME'), 
                  password=os.getenv('SHEETY_PASSWORD'),
                  token=os.getenv('SHEETY_TOKEN'))
    
    agent = TravelAgent(departure_city_code='TPE')
    main(sheet, agent, Project.FLIGHTDEALS)
