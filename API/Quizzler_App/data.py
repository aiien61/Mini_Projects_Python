import requests
from typing import List

parameters: dict = {
    'amount': 10,
    'type': 'boolean'
}

response: requests.Response = requests.get(url="https://opentdb.com/api.php", params=parameters)
response.raise_for_status()
question_data: dict = response.json()