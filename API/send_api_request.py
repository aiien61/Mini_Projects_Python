"""
Working on API calls

https://www.webfx.com/web-development/glossary/http-status-codes/
https://docs.python-requests.org/en/latest/
http://open-notify.org/Open-Notify-API/ISS-Location-Now/
https://www.latlong.net/Show-Latitude-Longitude.html
"""
import requests

response: requests.Response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()

data: dict = response.json()

longitude: float = data['iss_position']['longitude']
latitude: float = data['iss_position']['latitude']
iss_position: tuple = (longitude, latitude)

print(iss_position)