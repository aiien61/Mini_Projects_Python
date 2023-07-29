import requests
from datetime import datetime

# Make record tracking app using website 'Pixela' (https://pixe.la/)
# API document: https://docs.pixe.la/

## ---------------------- Create user account ---------------------------- ##

pixela_endpoint = "https://pixe.la/v1/users"
USERNAME = "" # Set your own username
TOKEN = "" # Set your own token
GRAPH_ID = "" # Set your own graph ID

user_params = {
    "token": TOKEN,
    "username": USERNAME,
    "agreeTermsOfService": "yes",
    "notMinor": "yes"
}

# response = requests.post(url=pixela_endpoint, json=user_params)
# print(response.text)

## ---------------------- Create a graph --------------------------------- ##

graph_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs"

graph_config = {
    "id": GRAPH_ID,
    "name": "Cycling Graph",
    "unit": "Km",
    "type": "float",
    "color": "shibafu"
}

headers = {
    "X-USER-TOKEN": TOKEN
}

# response = requests.post(url=graph_endpoint, json=graph_config, headers=headers)
# print(response.text)


## ---------------------- Post a pixel ----------------------------------- ##

pixel_creation_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}"

today = datetime.now()
target_date = datetime(year=2023, month=7, day=20)

pixel_data = {
    "date": today.strftime("%Y%m%d"),
    "quantity": "20"
}
response = requests.post(url=pixel_creation_endpoint,
                         json=pixel_data,
                         headers=headers)
print(response.text)


## ---------------------- Update a pixel --------------------------------- ##

update_endpoint = pixel_creation_endpoint + f"/{today.strftime('%Y%m%d')}"

pixel_data = {
    "quantity": input("How many kilometers did you cycle today? ")
}

response = requests.put(url=update_endpoint, json=pixel_data, headers=headers)
print(response.text)


## ---------------------- Delete a pixel --------------------------------- ##

delete_endpoint = pixel_creation_endpoint + f"/{today.strftime('%Y%m%d')}"

# response = requests.delete(url=delete_endpoint, headers=headers)
# print(response.text)
