import requests
from config import HEADERS

class Loader:
    @staticmethod
    def load(url: str) -> str:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.text