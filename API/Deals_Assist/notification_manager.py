import os
import ssl
import logging
import smtplib
from enum import Enum, auto
from typing import List, Tuple
from dotenv import load_dotenv
from twilio.rest import Client
from collections import namedtuple
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


logger = logging.getLogger(__name__)
logging.basicConfig(filename='flightdeals.log',
                    level=logging.DEBUG,
                    format="{asctime}-{levelname}-{name}-{message}",
                    style='{',
                    datefmt='%Y-%m-%d %H:%M:%S')

load_dotenv()

class Provider(Enum):
    GMAIL = auto()
    YAHOO = auto()
    HOTMAIL = auto()
    OUTLOOK = auto()

class SingletonPost(type):
    _instances: dict = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class EmailServer(metaclass=SingletonPost):
    ProviderAddress = namedtuple('ProviderAddress', ['address', 'port'])
    
    providers: dict = {
        Provider.GMAIL: ProviderAddress(address="smtp.gmail.com", port=587),
        Provider.YAHOO: ProviderAddress(address="smtp.mail.yahoo.com", port=587),
        Provider.HOTMAIL: ProviderAddress(address="smtp.live.com", port=587),
        Provider.OUTLOOK: ProviderAddress(address="smtp-mail.outlook.com", port=587)
    }

    def __init__(self, provider: Provider, email: str, app_password: str):
        self._email: str = email
        self._app_password: str = app_password
        self.provider: Tuple[str, int] = self._get_provider(provider)
        self.mail: MIMEMultipart = None

    def __repr__(self) -> str:
        return f"EmailServer(email={self._email}, app_password={self._app_password})"

    def _get_provider(self, provider_type: str) -> Tuple[str, int]:
        for provider in self.providers:
            if provider.name == provider_type:
                return self.providers[provider]
        return None

    def construct_content(self, subject: str, contents: str) -> MIMEMultipart:
        message: MIMEMultipart = MIMEMultipart()
        message['From'] = self.email
        message['Subject'] = subject
        message.attach(MIMEText(contents, 'plain'))
        return message

    def send(self, recipient_address: str):
        self.mail['To'] = recipient_address
        context = ssl.create_default_context()

        with smtplib.SMTP(self.provider.address, self.provider.port) as connection:
            connection.ehlo()
            connection.starttls(context=context)
            connection.ehlo()
            connection.login(user=self.email, password=self._app_password)
            connection.sendmail(from_addr=self.email,
                                to_addrs=recipient_address,
                                msg=self.mail.as_string())

class NotificationManager:

    def __init__(self):
        self.client = Client(os.environ.get("TWILIO_SID"), os.environ.get("TWILIO_AUTH_TOKEN"))
        self.twilio_virtual_number: str = os.environ.get("TWILIO_VIRTUAL_NUMBER")
        self.twilio_verified_number: str = os.environ.get("TWILIO_VERIFIED_NUMBER")
        self.whatsapp_number: str = os.environ.get("TWILIO_WHATSAPP_NUMBER")
        self.emailserver = EmailServer(
            provider=os.getenv("SENDER_EMAIL_PROVIDER"), 
            email=os.getenv("SENDER_EMAIL"), 
            app_password=os.getenv("SENDER_EMAIL_APP_PASSWORD")
        )

    def send_sms(self, message_body: str) -> None:
        message = self.client.messages.create(
            from_=self.twilio_virtual_number,
            body=message_body,
            to=self.twilio_verified_number
        )
        logger.debug(message.sid)
        return None

    def send_whatsapp(self, message_body: str) -> None:
        message = self.client.messages.create(
            from_=f"whatsapp:{self.whatsapp_number}",
            body=message_body,
            to=f"whatsapp:{self.twilio_verified_number}"
        )
        logger.debug(message.sid)
        return None

    def send_emails(self, email_list: List[str], email_body: str) -> None:
        subject: str = "New Low Price Flight!"

        for recipient in email_list:
            self.emailserver.mail = self.emailserver.construct_content(subject=subject, contents=email_body)
            self.emailserver.send(recipient)
