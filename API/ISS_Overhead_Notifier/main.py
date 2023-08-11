import requests
import smtplib
import time
from datetime import datetime


MY_EMAIL = "myemail@gmail.com" # Replace with Your Email
MY_PASSWORD = "my-password" # Generate Your Email App Password
MY_LAT = 51.507351  # You Can Get Your Latitude By https://www.latlong.net/
MY_LONG = -0.127758  # You Can Get Your Longitude By https://www.latlong.net/
ISS_ENDPOINT = "https://api.sunrise-sunset.org/json"


def is_iss_overhead() -> bool:
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    
    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    is_within_latitude = MY_LAT - 5 <= iss_latitude <= MY_LAT + 5
    is_within_longitude = MY_LONG - 5 <= iss_longitude <= MY_LONG + 5
    
    if is_within_latitude and is_within_longitude:
        return True
    return False


def is_night() -> bool:
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get(ISS_ENDPOINT, params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour
    if time_now >= sunset or time_now <= sunrise:
        return True
    return False


if __name__ == "__main__":
    while True:
        time.sleep(60)
        if is_iss_overhead() and is_night():
            connection = smtplib.SMTP("smtp.gmail.com")
            connection.starttls()
            connection.login(MY_EMAIL, MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=MY_EMAIL,
                msg="Subject:Look Up👆\n\nThe ISS is above you in the sky."
            )


