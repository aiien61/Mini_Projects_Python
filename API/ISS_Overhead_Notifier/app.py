"""
Challenge:
If the ISS is close to the current position,
1. and it is currently dark
2. then send an email to notify to lool up
3. run the code every 60 seconds
"""
import time
import requests
import smtplib
from typing import Tuple
from datetime import datetime


class ISSOverheadNotifier:
    server_email: str = "MY_GMAIL@gmail.com"
    app_password: str = "MY_APP_PASSWORD"

    def __init__(self, recipient_email: str, recipient_latitude: float, recipient_longitude: float):
        self.recipient_email: str = recipient_email
        self.latitude: float = recipient_latitude
        self.longitude: float = recipient_longitude
    
    def access_data(self, url: str, parameters: dict=None) -> dict:
        response: requests.Response = requests.get(url=url, params=parameters)
        response.raise_for_status()
        data: dict = response.json()
        return data

    def is_iss_overhead(self) -> bool:
        data: dict = self.access_data(url="http://api.open-notify.org/iss-now.json")
        iss_latitude: float = float(data['iss_position']['latitude'])
        iss_longitude: float = float(data['iss_position']['longitude'])
        is_lat_closed: bool = self.latitude - 5 <= iss_latitude <= self.latitude + 5
        is_lng_closed: bool = self.longitude - 5 <= iss_longitude <= self.longitude + 5
        return True if is_lat_closed and is_lng_closed else False
    
    def is_night(self) -> bool:
        parameters: dict = {
            "lat": self.latitude,
            "lng": self.longitude,
            "formatted": 0
        }

        data: dict = self.access_data(url="http://api.sunrise-sunset.org/json", parameters=parameters)
        _, sunrise_time = data['results']['sunrise'].split('T')
        sunrise_hour, sunrise_minutes, *_ = sunrise_time.split(':')
        
        _, sunset_time = data['results']['sunrise'].split('T')
        sunset_hour, sunset_minutes, *_ = sunset_time.split(':')

        time_now: datetime = datetime.now()
        if time_now >= int(sunset_hour) or time_now <= int(sunrise_hour):
            return True
        return False
    
    def send_email(self) -> None:
        if self.is_iss_overhead() and self.is_night():
            with smtplib.SMTP("smtp.gmail.com") as connection:
                connection.starttls()
                connection.login(user=self.server_email, password=self.app_password)
                connection.sendmail(from_addr=self.server_email,
                                    to_addrs=self.recipient_email,
                                    msg=f"Subject:Look Up👆\n\nThe ISS is above you in the sky.")
                
    def turn_on(self) -> None:
        while True:
            time.sleep(60)
            self.send_email()
        

if __name__ == "__main__":
    your_email: str = "YOUR-GMAIL@gmail.com"
    your_latitude: float = 0
    your_longitude: float = 0
    iss_notifier = ISSOverheadNotifier(your_email, your_latitude, your_longitude)
    iss_notifier.turn_on()        
