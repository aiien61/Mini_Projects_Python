import os
import requests
import logging
from abc import ABC
from datetime import datetime
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)
logging.basicConfig(filename='flightdeals.log',
                    level=logging.DEBUG,
                    format="{asctime}-{levelname}-{name}-{message}",
                    style='{',
                    datefmt='%Y-%m-%d %H:%M:%S')

@dataclass
class TravelAgent:
    departure_city_code: str
    destination_city_code: str = field(default=None)
    from_time: datetime = field(default=None)
    to_time: datetime = field(default=None)
    adults: int = field(default=1)
    is_direct: bool = field(default=True)

class Search(ABC):
    pass

class FlightSearch(Search):

    endpoints: dict = {
        'token': "https://test.api.amadeus.com/v1/security/oauth2/token",
        'iata': "https://test.api.amadeus.com/v1/reference-data/locations/cities",
        'flight': "https://test.api.amadeus.com/v2/shopping/flight-offers"
    }

    def __init__(self, travel_agent: TravelAgent, api_key: str, api_secret: str):
        self.travel_agent: TravelAgent = travel_agent
        self._api_key: str = api_key
        self._api_secret: str = api_secret
        self._token: str = self._get_new_token()

    def _get_new_token(self) -> str:
        header: dict = {'Content-Type': 'application/x-www-form-urlencoded'}
        body: dict = {
            'grant_type': 'client_credentials',
            'client_id': self._api_key,
            'client_secret': self._api_secret
        }
        response = requests.post(
            url=self.token_endpoint, headers=header, data=body)
        return response.json()['access_token']
    
    @property
    def token_endpoint(self) -> str:
        return self.endpoints['token']
    
    @property
    def iata_endpoint(self) -> str:
        return self.endpoints['iata']
    
    @property
    def flight_endpoint(self) -> str:
        return self.endpoints['flight']
    
    @property
    def headers(self) -> dict:
        return {'Authorization': f'Bearer {self._token}'}

    def get_destination_code(self, city_name: str) -> str:
        print(f'Using this token to get destination {self._token}')
        query: dict = {
            'keyword': city_name,
            'max': '2',
            'include': 'AIRPORTS'
        }
        response = requests.get(url=self.iata_endpoint, headers=self.headers, params=query)

        print(f"Status code {response.status_code}. Airport IATA: {response.text}")
        try:
            code: str = response.json()['data'][0]['iataCode']
        except IndexError:
            logger.debug(f"IndexError: No airport code found for {city_name}")
            code = "N/A"
        except KeyError:
            logger.debug(f"KeyError: No airport code found for {city_name}")
            code = "Not Found"
        finally:
            return code
    
    def check_flights(self):
        query: dict = {
            'originLocationCode': self.travel_agent.departure_city_code,
            'destinationLocationCode': self.travel_agent.destination_city_code,
            'departureDate': self.travel_agent.from_time.strftime('%Y-%m-%d'),
            'returnDate': self.travel_agent.to_time.strftime('%Y-%m-%d'),
            'adults': self.travel_agent.adults,
            'nonStop': str(self.travel_agent.is_direct).lower(),
            'currencyCode': 'TWD',
            'max': '10'
        }
        response = requests.get(url=self.flight_endpoint, headers=self.headers, params=query)

        if response.status_code != 200:
            logger.debug(f"Check flights response code: {response.status_code}")
            logger.debug(f"Response body: {response.text}")
            return None

        return response.json()
