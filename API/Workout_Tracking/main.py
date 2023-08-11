import os
import requests
from datetime import datetime
from pprint import pprint

GENDER = "male"
WEIGHT_KG = 80
HEIGHT_CM = 180
AGE = 32

# Visit Nutritionix (https://www.nutritionix.com/business/api) to get your nutrition API Key
APP_ID = os.environ["ENV_NIX_APP_ID"]
API_KEY = os.environ["ENV_NIX_API_KEY"]

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
exercise_text = input("Tell which exercise you did: ")

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

parameters = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

response = requests.post(url=exercise_endpoint, json=parameters, headers=headers)
result = response.json()
print("Nutritionix API call:")
pprint(result)

# Create a copy of Google spreadsheet
# Visit Sheety (https://sheety.co/) to connect Google sheet that you've just created
GOOGLE_SHEET_NAME = "workout"
sheet_endpoint = os.environ["ENV_SHEETY_ENDPOINT"]

for exercise in result['exercises']:
    new_entry = {
        GOOGLE_SHEET_NAME: {
            "date": datetime.now().strftime("%d/%m/%Y"),
            "time": datetime.now().strftime("%X"),
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    ## ----------- Sheety API Call & Authentication ---------------------- ##
    ## Select the type of authentication on your Sheety dashboard
    ## Choose the selected type of code to update google sheet and comment the other two blocks of code

    # Option 1: No Auth
    sheet_response = requests.post(url=sheet_endpoint, json=new_entry)

    # Option 2: Basic Auth
    sheet_response = requests.post(
        url=sheet_endpoint,
        json=new_entry,
        auth=(
            os.environ["ENV_SHEETY_USERNAME"],
            os.environ["ENV_SHEETY_PASSWORD"],
        )
    )

    # Option 3: Bearer Token
    bearer_headers = {
        "Authorization": f"Bearer {os.environ['ENV_SHEETY_TOKEN']}"
    }
    sheet_response = requests.post(
        url=sheet_endpoint, json=new_entry, headers=bearer_headers
    )

    print(sheet_response.text)
    
response = requests.get(url=sheet_endpoint)
data = response.json()
print(data)
