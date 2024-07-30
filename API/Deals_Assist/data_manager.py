import os
import requests
import logging
from typing import List
from enum import Enum, auto
from dotenv import load_dotenv
from dataclasses import dataclass
from requests.auth import HTTPBasicAuth

logger = logging.getLogger(__name__)
logging.basicConfig(filename='flightdeals.log', 
                    level=logging.DEBUG, 
                    format="{asctime}-{levelname}-{name}-{message}",
                    style='{',
                    datefmt='%Y-%m-%d %H:%M:%S')


load_dotenv()

class Project(Enum):
    FLIGHTDEALS = auto()


PROJECT_MAPPER: dict = {
    Project.FLIGHTDEALS: f"{os.getenv('SHEETY_URL')}/flightDealsDemo"
}


@dataclass
class Sheet:
    username: str
    password: str
    token: str

class SheetDataManager:
    
    def __init__(self, sheet: Sheet, project_name: Project):
        self.sheet: Sheet = sheet
        self.project: Project = project_name
        self._authorization: HTTPBasicAuth = HTTPBasicAuth(self.sheet.username, self.sheet.password)
        self.destination_data: List[dict] = None
        self.customer_data = {}

    @property
    def prices_endpoint(self):
        return os.path.join(PROJECT_MAPPER[self.project], 'prices')
    
    @property
    def users_endpoint(self):
        return os.path.join(PROJECT_MAPPER[self.project], 'users')
    
    @property
    def headers(self):
        return {'Authorization': f"Basic {self.sheet.token}"}
    
    def get_destination_data(self):
        try:
            response = requests.get(url=self.prices_endpoint)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logger.debug(f"{e}")
            if response.status_code == 402:
                logger.debug("Out of monthly quota. Not enough credits to make this request.")
                return None

        data: dict = response.json()
        self.destination_data = data["prices"]
        return self.destination_data
    
    def update_destination_codes(self):
        try:
            for city in self.destination_data:
                new_data = {
                    "price": {
                        "iataCode": city['iataCode']
                    }
                }
            response = requests.put(url=f"{self.prices_endpoint}/{city['id']}", json=new_data)
            response.raise_for_status()
            logger.debug(response.ok)
        except requests.exceptions.HTTPError as e:
            logger.debug(f"{e}")
            if response.status_code == 402:
                logger.debug("Out of monthly quota. Not enough credits to make this request.")

    def get_customer_emails(self):
        try:
            response = requests.get(url=self.users_endpoint)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logger.debug(f"{e}")
            if response.status_code == 402:
                logger.debug("Out of monthly quota. Not enough credits to make this request.")
                return None
        
        data: dict = response.json()
        self.customer_data = data['users']
        return self.customer_data

