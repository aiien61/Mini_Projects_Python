from pprint import pprint
from datetime import datetime, timedelta

from data_manager import DataManager
from flight_search import FlightSearch

flight_search = FlightSearch()
data_manager = DataManager()
sheet_data = data_manager.get_destiniation_data()

ORIGINAL_CITY_IATA = 'LON'

if sheet_data[0]['iataCode'] == '':    
    for row in sheet_data:
        row['iataCode'] = flight_search.get_destiniation_code(row['city'])
    data_manager.destination_data = sheet_data
    data_manager.update_destination_codes()


tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=6*30)

for destination in sheet_data:

    flight = flight_search.check_flights(
        from_time=tomorrow,
        to_time=six_month_from_today,
        **{
            "departure_city_code": ORIGINAL_CITY_IATA,
            "destination_city_code": destination["iataCode"],
        }
    )