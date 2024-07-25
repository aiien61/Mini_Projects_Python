import os
import json
import logging
import requests
from enum import Enum, auto
from datetime import datetime
from typing import List
logger = logging.getLogger(__name__)
logging.basicConfig(filename="mylog.log", level=logging.DEBUG, format="%(levelname)s:%(message)s")


class Color(Enum):
    RED = auto()
    GREEN = auto()
    BLUE = auto()
    YELLOW = auto()
    PURPLE = auto()
    BLACK = auto()


def get_color(color: Color) -> str:
    return {
        Color.RED: "momiji",
        Color.GREEN: "shibafu",
        Color.BLUE: "sora",
        Color.YELLOW: "ichou",
        Color.PURPLE: "ajisai",
        Color.BLACK: "kuro"
    }.get(color)


class SingletonDatabase(type):
    _instances: dict = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class PixelDatabase(metaclass=SingletonDatabase):
    db_name: str = "pixel_db.json"
    def __init__(self):
        self.create_new_db()

    def create_new_db(self) -> bool:
        if not os.path.exists(self.db_name):
            with open(self.db_name, 'w') as file:
                json.dump({}, file)
        return True

    def add_user(self, username: str) -> bool:
        new_user_db: dict = {username: {}}
        with open(self.db_name, 'r') as file:
            db: dict = json.load(file)

        db.update(new_user_db)
        with open(self.db_name, 'w') as file:
            json.dump(db, file)

        return True
    
    def get_all_users(self) -> List[str]:
        with open(self.db_name, 'r') as file:
            db: dict = json.load(file)
        return list(db.keys())

    def has_user(self, username: str) -> bool:
        with open(self.db_name, 'r') as file:
            db: dict = json.load(file)
        return username in db
    
    def delete_user(self, username: str) -> bool:
        with open(self.db_name, 'r') as file:
            db = json.load(file)
        del db[username]
        with open(self.db_name, 'w') as file:
            json.dump(db, file)
        return True
    
    def add_graph(self, username: str, graph_id: str, type_: str) -> bool:
        new_graph_db: dict = {graph_id: {'type': type_, 'dates': {}}}
        with open(self.db_name, 'r') as file:
            db: dict = json.load(file)
        db[username].update(new_graph_db)
        with open(self.db_name, 'w') as file:
            json.dump(db, file)
        return True
    
    def get_graph(self, username: str, graph_id: str) -> dict:
        with open(self.db_name, 'r') as file:
            db: dict = json.load(file)
        return db[username][graph_id]
    
    def get_all_graphs(self, username: str) -> List[str]:
        with open(self.db_name, 'r') as file:
            db: dict = json.load(file)
        return list(db[username].keys())

    def has_graph(self, username: str, graph_id: str) -> bool:
        with open(self.db_name, 'r') as file:
            db: dict = json.load(file)
        return graph_id in db[username]
    
    def delete_graph(self, username: str, graph_id: str) -> bool:
        with open(self.db_name, 'r') as file:
            db = json.load(file)
        del db[username][graph_id]
        with open(self.db_name, 'w') as file:
            json.dump(db, file)
        return True
    
    def add_pixel(self, username: str, graph_id: str, date: str, intensity: float) -> bool:
        return self.update_pixel(username, graph_id, date, intensity)
    
    def update_pixel(self, username: str, graph_id: str, date: str, intensity: float) -> bool:
        with open(self.db_name, 'r') as file:
            db: dict = json.load(file)
        db[username][graph_id]["dates"][date] = intensity
        print(db)
        with open(self.db_name, 'w') as file:
            json.dump(db, file)
        return True
    
    def get_pixel(self, username: str, graph_id: str, date: str) -> float:
        with open(self.db_name, 'r') as file:
            db: dict = json.load(file)
        return db[username][graph_id]["dates"][date]
    
    def has_pixel(self, username: str, graph_id: str, date: str) -> bool:
        with open(self.db_name, 'r') as file:
            db: dict = json.load(file)
        return date in db[username][graph_id]["dates"]
    
    def delete_pixel(self, username: str, graph_id: str, date: str) -> bool:
        with open(self.db_name, 'r') as file:
            db = json.load(file)
        del db[username][graph_id]["dates"][date]
        with open(self.db_name, 'w') as file:
            json.dump(db, file)
        return True


class HabitTracker:
    """Habit tracking app using website 'Pixela' (https://pixe.la/)"""

    pixela_endpoint: str = "https://pixe.la/v1/users"
    pixel_db: PixelDatabase = PixelDatabase()

    def __init__(self, username: str, token: str):
        self._username: str = username
        self._token: str = token
        self._graph_id: str = None
        self._headers: dict = {
            'X-USER-TOKEN': self._token
        }
        self._create_user(username, token)

    @property
    def username(self) -> str:
        return self._username
    
    @username.setter
    def username(self, username: str):
        self._username = username

    @property
    def token(self) -> str:
        return self._token
    
    @token.setter
    def token(self, token: str):
        self._token = token
    
    @property
    def graph_id(self) -> str:
        return self._graph_id
    
    @graph_id.setter
    def graph_id(self, graph_id: str):
        self._graph_id = graph_id

    def get_all_graphs(self) -> List[str]:
        return self.pixel_db.get_all_graphs(self._username)

    def _create_user(self, username: str, token: str) -> bool:
        parameters: dict = {
            'token': token,
            'username': username,
            'agreeTermsOfService': 'yes',
            'notMinor': 'yes'
        }
        try:
            response: requests.Response = requests.post(url=self.pixela_endpoint, json=parameters)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logger.debug(f"{e}")
        finally:
            logger.debug(f"User created: {response.ok}")
            logger.debug(f"Response: {response.text}")
            logger.debug(f"Status code: {response.status_code}")
        
        if not self.pixel_db.has_user(username=username):
            self.pixel_db.add_user(username=username)

        return True

    def create_graph(self, graph_id: str, activity: str, unit: str, unit_type: str, color: Color) -> bool:
        self._graph_id = graph_id

        if self.pixel_db.has_graph(username=self._username, graph_id=self._graph_id):
            return False

        endpoint: str = f"{self.pixela_endpoint}/{self._username}/graphs"
        config: dict = {
            'id': self._graph_id,
            'name': activity,
            'unit': unit,
            'type': unit_type,
            'color': get_color(color)
        }
        try:
            response: requests.Response = requests.post(url=endpoint, json=config, headers=self._headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logger.debug(f"{e}")
        finally:
            logger.debug(f"User created: {response.ok}")
            logger.debug(f"Response: {response.text}")
            logger.debug(f"Status code: {response.status_code}")
        
        if not self.pixel_db.has_graph(username=self._username, graph_id=graph_id):
            self.pixel_db.add_graph(username=self._username, graph_id=graph_id, type_=unit_type)
        
        return True

    def create_pixel(self, intensity: float, date: str=None) -> bool:
        """Create a pixel

        Args:
            intensity (float): Intensity of the pixel
            date (str, optional): Date in YYYYMMDD format. Defaults to current date.

        Returns:
            bool: True if successful else False
        """

        if date is None:
            date: str = datetime.now().strftime("%Y%m%d")
        
        if self.pixel_db.has_pixel(username=self._username, graph_id=self._graph_id, date=date):
            return False

        endpoint: str = f"{self.pixela_endpoint}/{self._username}/graphs/{self._graph_id}"
        data: dict = {
            'date': date,
            'quantity': str(intensity)
        }

        try:
            response: requests.Response = requests.post(url=endpoint, json=data, headers=self._headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logger.debug(f"{e}")
        else:
            self.pixel_db.add_pixel(username=self._username, graph_id=self._graph_id, date=date, intensity=intensity)
        finally:
            logger.debug(f"pixel created: {response.ok}")
            logger.debug(f"Response: {response.text}")
            logger.debug(f"Status code: {response.status_code}")
        
        return self.pixel_db.has_pixel(username=self._username, graph_id=self._graph_id, date=date)

    def update_pixel(self, intensity: float, date: str=None) -> bool:
        """Update a pixel

        Args:
            intensity (float): Intensity of the pixel
            date (str, optional): Date in YYYYMMDD format. Defaults to current date.

        Returns:
            bool: True if successful else False
        """
        if date is None:
            date: str = datetime.now().strftime("%Y%m%d")
        
        endpoint: str = f"{self.pixela_endpoint}/{self._username}/graphs/{GRAPH_ID}/{date}"
        data: dict = {'quantity': str(intensity)}

        try:
            response: requests.Response = requests.put(url=endpoint, json=data, headers=self._headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logger.debug(f"{e}")
        else:
            self.pixel_db.update_pixel(username=self._username, graph_id=self._graph_id, date=date, intensity=intensity)
        finally:
            logger.debug(f"pixel updated: {response.ok}")
            logger.debug(f"Response: {response.text}")
            logger.debug(f"Status code: {response.status_code}")
            pixel_intensity = self.pixel_db.get_pixel(username=self._username, graph_id=self._graph_id, date=date)
            return intensity == pixel_intensity
    
    def increase_intensity(self, amount: float, date: str=None) -> bool:
        if date is None:
            date: str = datetime.now().strftime("%Y%m%d")
        try:
            intensity = self.pixel_db.get_pixel(username=self._username, graph_id=self._graph_id, date=date)
            self.update_pixel(intensity + amount, date)
        except KeyError as e:
            logger.error(f"Error: {e}")
        finally:
            new_intensity = self.pixel_db.get_pixel(username=self._username, graph_id=self._graph_id, date=date)
            return (intensity + amount) == new_intensity
        
    def decrease_intensity(self, amount: float, date: str=None) -> bool:
        if date is None:
            date: str = datetime.now().strftime("%Y%m%d")
        try:
            intensity = self.pixel_db.get_pixel(username=self._username, graph_id=self._graph_id, date=date)
            assert intensity >= amount, f"Error: {intensity} < {amount}"
            self.update_pixel(intensity - amount, date)
        except KeyError as e:
            logger.error(f"{e}")
        except AssertionError as e:
            logger.error(f"{e}")
        finally:
            new_intensity = self.pixel_db.get_pixel(username=self._username, graph_id=self._graph_id, date=date)
            return (intensity - amount) == new_intensity
        
    def delete_pixel(self, date: str=None) -> bool:
        if date is None:
            date: str = datetime.now().strftime("%Y%m%d")

        if not self.pixel_db.has_pixel(username=self._username, graph_id=self._graph_id, date=date):
            logging.debug(f"pixel not found: {date}")
            return False
        
        try:
            endpoint: str = f"{self.pixela_endpoint}/{self._username}/graphs/{self._graph_id}/{date}"
            response: requests.Response = requests.delete(url=endpoint, headers=self._headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logger.debug(f"{e}")
        else:
            self.pixel_db.delete_pixel(username=self._username, graph_id=self._graph_id, date=date)
        finally:
            logger.debug(f"pixel updated: {response.ok}")
            logger.debug(f"Response: {response.text}")
            logger.debug(f"Status code: {response.status_code}")
            
            pixel_deleted: bool = not self.pixel_db.has_pixel(username=self._username, graph_id=self._graph_id, date=date)
            return response.ok == pixel_deleted

    def delete_graph(self, graph_id: str) -> bool:
        if not self.pixel_db.has_graph(username=self._username, graph_id=graph_id):
            logging.debug(f"graph not found: {graph_id}")
            return False
        
        try:
            endpoint: str = f"{self.pixela_endpoint}/{self._username}/graphs/{graph_id}"
            response: requests.Response = requests.delete(url=endpoint, headers=self._headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logger.debug(f"{e}")
        else:
            self.pixel_db.delete_graph(username=self._username, graph_id=graph_id)
        finally:
            logger.debug(f"graph deleted: {response.ok}")
            logger.debug(f"Response: {response.text}")
            logger.debug(f"Status code: {response.status_code}")
            graph_deleted = not self.pixel_db.has_graph(username=self._username, graph_id=graph_id)
            return response.ok == graph_deleted

if __name__ == "__main__":
    USERNAME: str = "SET YOUR USERNAME HERE"
    TOKEN: str = 'SET YOUR TOKEN HERE'
    GRAPH_ID: str = 'SET YOUR GRAPH ID HERE'


    myhabit = HabitTracker(username=USERNAME, token=TOKEN)
    myhabit.create_graph(graph_id=GRAPH_ID, activity='Cycling Graph', unit='Km', unit_type='float', color=Color.GREEN)
    
    myhabit.graph_id = GRAPH_ID
    myhabit.create_pixel(60)
    myhabit.increase_intensity(30)
    myhabit.decrease_intensity(10)
    myhabit.delete_pixel()
    myhabit.delete_graph(graph_id=GRAPH_ID)
