"""
Rain Alert App

https://www.twilio.com
https://home.openweathermap.org
"""

import os
import requests
from enum import Enum, auto
from typing import List, Dict
from abc import ABC, abstractmethod

from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient


COORDINATES_MAP: dict = {
    "London": (51.5074, 0.1278),
    "Paris": (48.8566, 2.3522),
    "New York": (40.7128, -74.0060),
    "Sydney": (-33.8688, 151.2093)
}


class DeviceType(Enum):
    PHONE = auto()
    WHATSAPP = auto()


class Observer(ABC):
    @abstractmethod
    def payload(self): raise NotImplementedError


class SingletonAlert(type):
    __instances: dict = {}
    def __call__(cls, *args, **kwargs):
        if not cls in cls.__instances:
            cls.__instances[cls] = super().__call__(*args, **kwargs)
        return cls.__instances[cls]


class Observable(ABC):
    __metaclass__ = SingletonAlert

    @abstractmethod
    def register_observer(self, observer: Observer): raise NotImplementedError

    @abstractmethod
    def remove_observer(self, observer: Observer): raise NotImplementedError

    @abstractmethod
    def notify_observers(self): raise NotImplementedError
    

class RainAlert(Observable):
    def __init__(self, api_key: str, account_sid: str, auth_token: str, on_server: bool=False) -> None:
        self.endpoint: str = None
        self.on_server: bool = on_server
        self._observers: List[Observer] = []
        self._api_key: str = api_key
        self._account_sid: str = account_sid
        self._auth_token: str = auth_token
        self._sender_numbers: Dict[str] = {DeviceType.PHONE: None, DeviceType.WHATSAPP: None}

    def update_sender_number(self, sender_number: str, is_phone: bool=False, is_whatsapp: bool=False) -> bool:
        if is_phone:
            self._sender_numbers[DeviceType.PHONE] = sender_number
        elif is_whatsapp:
            self._sender_numbers[DeviceType.WHATSAPP] = f"whatsapp:{sender_number}"
        return True
    
    def register_observer(self, observer: Observer) -> bool:
        assert observer.is_verified()
        self._observers.append(observer)
        return True
    
    def remove_observer(self, observer: Observer) -> bool:
        try:
            self._observers.remove(observer)
        except ValueError:
            return False
        return True
    
    def notify_observers(self) -> bool:
        owm_parameters: dict = {
            # 'lat': None,
            # 'lon': None,
            'q': None,
            'appid': self._api_key
        }
        # TODO: asyncio
        for observer in self._observers:
            # owm_parameters['lat'] = COORDINATES_MAP[observer.city][0]
            # owm_parameters['lon'] = COORDINATES_MAP[observer.city][1]
            payload: dict = observer.payload()
            owm_parameters['q'] = payload['city']

            response: requests.Response = requests.get(url=self.endpoint, params=owm_parameters)
            response.raise_for_status()
            weather_data: dict = response.json()

            will_rain: bool = False
            weather_condition: dict = weather_data['weather'][0]
            condition_code: int = int(weather_condition['id'])
            if condition_code < 700:
                will_rain = True

            if will_rain:
                if self.on_server:
                    proxy_client = TwilioHttpClient()
                    proxy_client.session.proxies = {'https': os.environ['https_proxy']}

                device_type = payload['device_type']
                recipient_number = payload['recipient_number']

                client: Client = Client(self._account_sid, self._auth_token)
                message = client.messages.create(
                    body="It's going to rain today. Remember to bring an umbrella ☔️.",
                    from_=self.generate_device_sender_number(device_type),
                    to=self.generate_device_recipient_number(device_type, recipient_number)
                )
                print(message.status)
        return True
    
    def generate_device_sender_number(self, device_type: DeviceType) -> str:
        return self._sender_numbers.get(device_type)
    
    def generate_device_recipient_number(self, device_type: DeviceType, number: str) -> str:
        return {
            DeviceType.PHONE: number,
            DeviceType.WHATSAPP: f"whatsapp:{number}"
        }.get(device_type)

class Recipient(Observer):
    def __init__(self, recipient_number: str, device_type: DeviceType, city: str) -> None:
        self._recipient_number: str = recipient_number
        self._device_type: DeviceType = device_type
        self._city = city

    def set_device_type(self, new_device_type: DeviceType) -> bool:
        assert isinstance(new_device_type, DeviceType)
        self._device_type = new_device_type
        return True

    def set_city(self, new_city: str) -> bool:
        assert isinstance(new_city, str)
        self._city = new_city
        return True

    def set_recipient_number(self, new_recipient_number: str) -> bool:
        # TODO: verify the recipient number using regex
        assert isinstance(new_recipient_number, str)
        self._recipient_number = new_recipient_number
        return True

    def is_verified(self) -> bool:
        # TODO: verify the recipient number using regex
        assert isinstance(self._device_type, DeviceType)
        return True
    
    def payload(self) -> dict:
        return {
            'city': self._city,
            'device_type': self._device_type,
            'recipient_number': self._recipient_number
        }

if __name__ == '__main__':
    account_sid: str = os.environ.get("ACCOUNT_SID")
    auth_token: str = os.environ.get("AUTH_TOKEN")
    owm_api_key: str = os.environ.get("OWM_API_KEY")
    owm_endpoint: str = "https://api.openweathermap.org/data/2.5/weather"

    rain_alert = RainAlert(owm_api_key, account_sid, auth_token)
    rain_alert.endpoint = owm_endpoint
    rain_alert.update_sender_number(os.environ.get("TWILIO_VERIFIED_NUMBER"), is_phone=True)
    rain_alert.update_sender_number(os.environ.get("TWILIO_WHATSAPP_NUMBER"), is_whatsapp=True)

    phone_number: str = os.environ.get("RECIPIENT_NUMBER")

    recipient1 = Recipient(phone_number, device_type=DeviceType.PHONE, city="Taipei")
    rain_alert.register_observer(recipient1)

    recipient2 = Recipient(phone_number, device_type=DeviceType.WHATSAPP, city="Taipei")
    rain_alert.register_observer(recipient2)

    rain_alert.notify_observers()
