import requests
from flight_data import FlightData

TEQUILA_ENDPOINT = "https://tequila-api.kiwi.com"
TEQUILA_API_KEY = "YOUR API KEY"


class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def get_destiniation_code(self, city_name: str) -> str:
        location_endpoint = f"{TEQUILA_ENDPOINT}/locations/query"
        headers = {"apikey": TEQUILA_API_KEY}
        query = {"term": city_name, "location_types": "city"}
        response = requests.get(url=location_endpoint, headers=headers, params=query)
        results = response.json()["locations"]
        code = results[0]["code"]
        return code

    def check_flights(self, from_time, to_time, **kwargs):
        headers = {"apikey": TEQUILA_API_KEY}
        query = {
            "fly_from": kwargs.get("departure_city_code"),
            "fly_to": kwargs.get("destination_city_code"),
            "date_from": from_time.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "GBP"
        }

        response = requests.get(
            url=f"{TEQUILA_ENDPOINT}/v2/search",
            headers=headers,
            params=query
        )

        try:
            data = response.json()["data"][0]
            print('data:', data)
        except IndexError:
            print(f"No flights found for {destination_city_code}.")
            return None
        
        flight_data = FlightData(**{
            "price": data["price"],
            "departure_city": data["route"][0]["cityFrom"],
            "departure_airport_code": data["route"][0]["flyFrom"],
            "destination_city": data["route"][0]["cityTo"],
            "destination_airport_code": data["route"][0]["flyTo"],
            "out_date": data["route"][0]["local_departure"].split("T")[0],
            "return_date": data["route"][1]["local_departure"].split("T")[0]
        })
        print(f"{flight_data.destination_city}: £{flight_data.price}")
        return flight_data