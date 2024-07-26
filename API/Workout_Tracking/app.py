import os
import requests
import logging
from pprint import pprint
from datetime import datetime
from dataclasses import dataclass

logger: logging = logging.getLogger(__name__)
logging.basicConfig(filename='workout.log', level=logging.DEBUG, format="%(levelname)s:%(message)s")

GOOGLE_SPREADSHEET_NAME: str = "YOUR-SPREADSHEET-NAME"
GOOGLE_SHEET_NAME: str = "YOUR-SHEET-NAME"
NIX_APP_ID: str = os.environ.get("NIX_APP_ID")
NIX_API_KEY: str = os.environ.get("NIX_API_KEY")
BEARER_TOKEN: str = os.environ.get("BEARER_TOKEN")

@dataclass
class Participant:
    age: int
    gender: str
    weight_kg: float
    height_cm: float

class WorkoutTracker:
    nlp_headers: dict = {
        'Content-Type': 'application/json',
        # 'x-app-id': os.environ.get("NIX_APP_ID"),
        # 'x-app-key': os.environ.get("NIX_API_KEY"),
        'x-app-id': NIX_APP_ID,
        'x-app-key': NIX_API_KEY
    }

    bearer_headers: dict = {'Authorization': f"Bearer {BEARER_TOKEN}"}

    def __init__(self, participant: Participant, spreadsheet_name: str):
        self.participant: Participant = participant
        self.spreadsheet_name: str = spreadsheet_name
        self.sheet_name: str = ''

    @property
    def sheet_endpoint(self) -> str:
        url: str ='https://api.sheety.co/da8b5fc3220373013ccad2ee472013c5'
        return os.path.join(url, self.spreadsheet_name, f'{self.sheet_name}s')
    
    @property
    def nlp_endpoint(self) -> str:
        url: str = 'https://trackapi.nutritionix.com/v2/natural/exercise'
        return url
    
    def exercise(self):
        parameters: dict = {
            'query': input('Tell which exercise and how long you did: '),
            'gender': self.participant.gender,
            'weight_kg': self.participant.weight_kg,
            'height_cm': self.participant.height_cm,
            'age': self.participant.age
        }
        nlp_response = requests.post(url=self.nlp_endpoint, json=parameters, headers=self.nlp_headers)
        nlp_response.raise_for_status()
        nlp_result: dict = nlp_response.json()
        
        for exercise in nlp_result['exercises']:
            sheet_input: dict = {
                self.sheet_name: {
                    'date': datetime.now().strftime("%d/%m/%Y"),
                    'time': datetime.now().strftime("%H:%M:00"),
                    'exercise': exercise['name'].title(),
                    'duration': exercise['duration_min'],
                    'calories': exercise['nf_calories']
                }
            }
            
            sheet_response = requests.post(url=self.sheet_endpoint, json=sheet_input, headers=self.bearer_headers)
            sheet_response.raise_for_status()
            logger.debug(sheet_response.text)

        return nlp_result

if __name__ == "__main__":
    runner = Participant(age=32, gender='male', weight_kg=80, height_cm=180)
    tracker = WorkoutTracker(participant=runner, spreadsheet_name=GOOGLE_SPREADSHEET_NAME)
    tracker.sheet_name = GOOGLE_SHEET_NAME
    result: dict = tracker.exercise()
    pprint(result)