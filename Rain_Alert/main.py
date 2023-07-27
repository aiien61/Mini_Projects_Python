import os
import requests
from twilio.rest import Client

# Go to OpenWeather (https://home.openweathermap.org) to get your API key
OWM_Endpoint = "https://api.openweathermap.org/data/2.5/weather"
OWM_API_KEY = os.environ.get("OWM_API_KEY")

# Go to Twilio (https://www.twilio.com/try-twilio) to get your account sid and token
ACCOUNT_SID = "YOUR ACCOUNT SID"
AUTH_TOKEN = os.environ.get("AUTH_TOKEN")

parameters = {
    "q": "London",
    "appid": OWM_API_KEY,
}

response = requests.get(url=OWM_Endpoint, params=parameters)
response.raise_for_status()
weather_data = response.json()


will_rain = False
condition_code = weather_data["weather"][0]["id"]
if int(condition_code) < 700:
    will_rain = True

if will_rain:
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    message = client.messages.create(
        body="It's going to rain today. Remember to bring an umbrella ☔️.",
        from_="YOUR TWILIO VIRTUAL NUMBER",
        to="YOUR TWILIO VERIFIED REAL NUMBER"
    )

print(message.status)
