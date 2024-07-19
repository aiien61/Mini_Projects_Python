"""
Working on API calls

https://www.webfx.com/web-development/glossary/http-status-codes/
https://docs.python-requests.org/en/latest/
http://open-notify.org/Open-Notify-API/ISS-Location-Now/
https://www.latlong.net/Show-Latitude-Longitude.html
https://www.latlong.net/
https://sunrise-sunset.org/api
"""
import requests
from pprint import pprint
from datetime import datetime

def send_without_parameters() -> None:
    response: requests.Response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    
    data: dict = response.json()
    longitude: float = data['iss_position']['longitude']
    latitude: float = data['iss_position']['latitude']
    iss_position: tuple = (longitude, latitude)
    pprint(iss_position)

def send_with_parameters() -> None:
    # Latitude and longitude of coordinates of Sydney
    sydney_coordinates: tuple = (-33.868820, 151.209290)
    
    parameters: dict = {
        'lat': sydney_coordinates[0],
        'lng': sydney_coordinates[1],
        'formatted': 0
    }
    response: requests.Response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data: dict = response.json()
    pprint(data)

    sunrise: str = data['results']['sunrise']
    sunset: str = data['results']['sunset']
    
    _, sunrise_time = sunrise.split('T')
    sunrise_hour, sunrise_minutes, *_ = sunrise_time.split(':')

    _, sunset_time = sunset.split('T')
    sunset_hour, sunset_minutes, *_ = sunset_time.split(':')

    print(sunrise_hour, sunrise_minutes)
    print(sunset_hour, sunset_minutes)

    time_now: datetime = datetime.now()

    current_hour: str = f'{time_now.hour:02d}'
    current_minutes: str = f'{time_now.minute:02d}'
    print(current_hour, current_minutes)

    if current_hour == sunrise_hour and current_minutes >= sunrise_minutes:
        print('Sunrise')
    elif current_hour == sunset_hour and current_minutes <= sunset_minutes:
        print('Sunset')


if __name__ == "__main__":
    # send_without_parameters()
    send_with_parameters()