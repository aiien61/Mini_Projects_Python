import ssl
import random
import smtplib
import pandas as pd
import datetime as dt
from enum import Enum, auto
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Host(Enum):
    GMAIL = auto()
    YAHOO = auto()
    HOTMAIL = auto()
    OUTLOOK = auto()


class SingletonPost(type):
    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance

class EmailSender(metaclass=SingletonPost):
    hosthash: dict = {
        Host.GMAIL: ("smtp.gmail.com", 587),
        Host.YAHOO: ("smtp.mail.yahoo.com", 587),
        Host.HOTMAIL: ("smtp.live.com", 587),
        Host.OUTLOOK: ("smtp-mail.outlook.com", 587)
    }

    def __init__(self, host: Host, email: str, app_password: str):
        self._email: str = email
        self._app_password: str = app_password
        self.server: tuple = self.hosthash[host]
        self.mail: MIMEMultipart = None

    @property
    def email(self): return self._email

    @email.setter
    def email(self, value: str):
        # TODO: use regex to verify email first before setting
        self._email = value

    @property
    def app_password(self): return self._app_password

    @app_password.setter
    def app_password(self, value: str):
        self._app_password = value

    def construct_content(self, subject: str, contents: str) -> MIMEMultipart:
        message: MIMEMultipart = MIMEMultipart()
        message['From'] = self.email
        message['Subject'] = subject
        message.attach(MIMEText(contents, 'plain'))
        return message
    
    def send(self, recipient_address: str):
        self.mail['To'] = recipient_address
        context = ssl.create_default_context()
        
        with smtplib.SMTP(self.server[0], self.server[1]) as connection:
            connection.ehlo()
            connection.starttls(context=context)
            connection.ehlo()
            connection.login(user=self.email, password=self.app_password)
            connection.sendmail(from_addr=self.email, 
                                to_addrs=recipient_address, 
                                msg=self.mail.as_string())


def main(host: Host, email: str, app_password: str):
    placeholder: str = "[NAME]"
    today = dt.datetime.now()
    data_df: pd.DataFrame = pd.read_csv("birthdays.csv")
    has_birthday_month = data_df['month'] == today.month 
    has_birthday_day = data_df['day'] == today.day
    has_birthday = has_birthday_month & has_birthday_day

    if has_birthday.any():
        post: EmailSender = EmailSender(host, email, app_password)
        
        letter_path: str = f"letter_templates/letter_{random.randint(1, 3)}.txt"
        with open(letter_path) as letter_file:
            contents = letter_file.read()

        for _, row in data_df[has_birthday].iterrows():
            birthday_person: pd.Series = row
            body: str = contents.replace(placeholder, birthday_person['name'])
            post.mail = post.construct_content("Happy Birthday!", body)
            post.send(birthday_person['email'])


if __name__ == "__main__":
    gmail: str = "YOUR-GMAIL@gmail.com"
    gmail_app_password: str = "YOUR-APP-PASSWORD"
    yahoo_email: str = "YOUR-YAHOO-EMAIL@yahoomail.com"
    yahoo_app_password: str = "YOUR-APP-PASSWORD"

    main(Host.GMAIL, gmail, gmail_app_password)
