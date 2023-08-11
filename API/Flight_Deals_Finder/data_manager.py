import requests

SHEETY_PRICES_ENDPOINT = "https://api.sheety.co/da8b5fc3220373013ccad2ee472013c5/flightDeals/prices"

class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.destination_data = {}

    def get_destiniation_data(self):
        response = requests.get(url=SHEETY_PRICES_ENDPOINT)
        sheet_data = response.json()
        self.destination_data = sheet_data['prices']
        return self.destination_data

    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }

            response = requests.put(
                url=f"{SHEETY_PRICES_ENDPOINT}/{city['id']}",
                json=new_data
            )
            print(response.text)