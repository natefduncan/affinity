import datetime as dt
import requests as r
from enums import Enum
from typing import List, Dict, Optional
from affinity.common.exceptions import TokenMissing

BASE_URL = "https://api.affinity.co"

class RequestType:
    get: 1
    list: 2
    create: 3
    delete: 4

class Endpoint:
    endpoint: str = None
    request_types: List[RequestType] = []

    def __init__(self, token: str):
        self.token = token

    def get(self, id: int):
        return r.get(url=f"{BASE_URL}/{self.endpoint}/{id}", auth=(None, self.token))

    def list(self):
        return r.get(url=f"{BASE_URL}/{self.endpoint}", auth=(None, self.token))
        
    def create(self, data):
        headers = {"Content-Type" : "application/json"}
        return r.post(url=f"{BASE_URL}/{self.endpoint}", data=data, headers=headers, auth=(None, self.token))

    def delete(self, id):
        return r.delete(url=f"{BASE_URL}/{self.endpoint}")
