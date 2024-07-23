"""
Stock News App

https://www.alphavantage.co/
https://newsapi.org/
"""
import os
import requests
from enum import Enum, auto
from typing import List, Dict
from datetime import datetime
from abc import ABC, abstractmethod

from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

STOCK_API_EKY: str = os.environ.get("STOCK_API_KEY")
NEWS_API_KEY: str = os.environ.get("NEWS_API_KEY")


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


class StockNotifier(Observable):
    __api_keys: dict = {
        # 'stock_api_key': os.environ.get('STOCK_API_KEY'),
        # 'news_api_key': os.environ.get('NEWS_API_KEY')
        'stock_api_key': STOCK_API_EKY,
        'news_api_key': NEWS_API_KEY
    }
    __endpoints: dict = {
        'stock_endpoint': "https://www.alphavantage.co/query",
        'news_endpoint': "https://newsapi.org/v2/everything"
    }
    def __init__(self, account_sid: str, auth_token: str, on_server: bool = False) -> None:
        self.on_server: bool = on_server
        self._observers: List[Observer] = []
        self._account_sid: str = account_sid
        self._auth_token: str = auth_token
        self._sender_numbers: Dict[str] = {DeviceType.PHONE: None, DeviceType.WHATSAPP: None}

    def update_sender_number(self, sender_number: str, device_type: DeviceType) -> bool:
        self._sender_numbers[device_type] = {
            DeviceType.PHONE: sender_number, 
            DeviceType.WHATSAPP: f"whatsapp:{sender_number}"
        }.get(device_type)
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
        stock_parameters: dict = {
            'function': 'TIME_SERIES_DAILY',
            'symbol': None,
            'apikey': self.__api_keys['stock_api_key']
        }
        # TODO: asyncio
        for observer in self._observers:
            payload: dict = observer.payload()
            if payload['stock_name'] is None:
                continue
            
            stock_parameters['symbol'] = payload['stock_name']
            stock_endpoint: str = self.__endpoints['stock_endpoint']

            response: requests.Response = requests.get(url=stock_endpoint, params=stock_parameters)
            response.raise_for_status()
            stock_price_data: dict = response.json()
            percentage: float = self.calculate_close_price_difference_percentage(stock_price_data)
            up_down: str = "🔺" if percentage > 0 else "🔻"

            if abs(percentage) < 1:
                continue
            
            if payload['company_name'] is None:
                continue
            
            new_parameters: dict = {
                'apiKey': self.__api_keys['news_api_key'],
                'qInTitle': payload['company_name']
            }
            news_list: List[dict] = self.get_top_n_stock_news(api_parameters=new_parameters, n=3)
            message_list: List[str] = self.generate_stock_message_list(news_list)

            if self.on_server:
                proxy_client = TwilioHttpClient()
                proxy_client.session.proxies = {'https': os.environ['https_proxy']}

            device_type: DeviceType = payload['device_type']
            recipient_number: str = payload['recipient_number']
            stock_name: str = payload['stock_name']

            client: Client = Client(self._account_sid, self._auth_token)

            for message_body in message_list:
                message_body = f"{stock_name}: {up_down}{abs(percentage)}%\n" + message_body
                message = client.messages.create(
                    body=message_body,
                    from_=self.generate_device_sender_number(device_type),
                    to=self.generate_device_recipient_number(device_type, recipient_number)
                )
                print(message.status)
        
        return True

    
    def calculate_close_price_difference_percentage(self, stock_price_data: dict) -> float:
        daily_data: dict = stock_price_data['Time Series (Daily)']
        daily_data_list: List[dict] = [v for k, v in daily_data.items()]
        yesterday_data: dict = daily_data_list[0]
        yesterday_closing_price: float = float(yesterday_data['4. close'])

        day_before_yesterday_data: dict = daily_data_list[1]
        day_before_yesterday_closing_price: float = float(day_before_yesterday_data['4. close'])

        price_difference: float = yesterday_closing_price - day_before_yesterday_closing_price
        percentage: float = round((price_difference / yesterday_closing_price) * 100)
        return percentage
    
    def get_top_n_stock_news(self, api_parameters: dict, n: int) -> List[dict]:
        news_endpoint: str = self.__endpoints['news_endpoint']
        response: requests.Response = requests.get(news_endpoint, params=api_parameters)
        response.raise_for_status()
        return response.json()['articles'][:n]

    def generate_device_sender_number(self, device_type: DeviceType) -> str:
        return self._sender_numbers.get(device_type)

    def generate_device_recipient_number(self, device_type: DeviceType, number: str) -> str:
        return {
            DeviceType.PHONE: number,
            DeviceType.WHATSAPP: f"whatsapp:{number}"
        }.get(device_type)
    
    def generate_stock_message_list(self, news_list: List[dict]) -> List[str]:
        return [f"Headline: {news['title']}. \nBrief: {news['description']}" for news in news_list]



class Recipient(Observer):
    def __init__(self, recipient_number: str, device_type: DeviceType) -> None:
        self._recipient_number: str = recipient_number
        self._device_type: DeviceType = device_type
        self._stock_name: str = None
        self._company_name: str = None

    def set_device_type(self, new_device_type: DeviceType) -> bool:
        assert isinstance(new_device_type, DeviceType)
        self._device_type = new_device_type
        return True

    def set_recipient_number(self, new_recipient_number: str) -> bool:
        # TODO: verify the recipient number using regex
        assert isinstance(new_recipient_number, str)
        self._recipient_number = new_recipient_number
        return True
    
    def set_stock_name(self, new_stock_name: str) -> bool:
        assert isinstance(new_stock_name, str)
        self._stock_name = new_stock_name
        return True
    
    def set_company_name(self, new_company_name: str) -> bool:
        assert isinstance(new_company_name, str)
        self._company_name = new_company_name
        return True

    def is_verified(self) -> bool:
        # TODO: verify the recipient number using regex
        assert isinstance(self._device_type, DeviceType)
        return True

    def payload(self) -> dict:
        return {
            'stock_name': self._stock_name,
            'device_type': self._device_type,
            'company_name': self._company_name,
            'recipient_number': self._recipient_number
        }


if __name__ == '__main__':
    stock_name: str = "TSLA"
    company_name: str = "Tesla Inc"

    twilio_account_sid: str = os.environ.get("TWILIO_ACCOUNT_SID")
    twilio_auth_token: str = os.environ.get("TWILIO_AUTH_TOKEN")

    twilio_phone_number: str = os.environ.get("TWILIO_PHONE_NUMBER")
    twilio_whatsapp_number: str = os.environ.get("TWILIO_WHATSAPP_NUMBER")

    app = StockNotifier(account_sid=twilio_account_sid, auth_token=twilio_auth_token)
    app.update_sender_number(sender_number=twilio_phone_number, device_type=DeviceType.PHONE)
    app.update_sender_number(sender_number=twilio_whatsapp_number, device_type=DeviceType.WHATSAPP)

    phone_number: str = os.environ.get("RECIPIENT_NUMBER")

    recipient1 = Recipient(recipient_number=phone_number,device_type=DeviceType.WHATSAPP)
    recipient1.set_stock_name(stock_name)
    recipient1.set_company_name(company_name)
    app.register_observer(recipient1)

    recipient2 = Recipient(recipient_number=phone_number, device_type=DeviceType.PHONE)
    recipient2.set_stock_name(stock_name)
    recipient2.set_company_name(company_name)
    app.register_observer(recipient2)

    app.notify_observers()