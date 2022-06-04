import datetime as dt
import requests as r
from enum import Enum
from typing import List, Optional
from affinity.common.exceptions import TokenMissing, RequestTypeNotAllowed, RequestFailed
from affinity.core import models

BASE_URL = "https://api.affinity.co"

class RequestType(Enum):
    GET = 1
    LIST = 2
    CREATE =  3
    DELETE = 4

class Endpoint:
    endpoint: Optional[str] = None
    request_types: List[RequestType] = []

    def __init__(self, token: str):
        self.token = token

    def get(self, id: int):
        if not self.token:
            raise TokenMissing
        if RequestType.GET not in self.request_types:
            raise RequestTypeNotAllowed
        response = r.get(url=f"{BASE_URL}/{self.endpoint}/{id}", auth=("", self.token))
        if response.status_code != 200:
            raise RequestFailed(response.content)
        return self.parse_get(response)

    def parse_get(self, response: r.Response):
        # Assume 200 status code
        return response.json()

    def list(self):
        if not self.token:
            raise TokenMissing
        if RequestType.LIST not in self.request_types:
            raise RequestTypeNotAllowed
        print(self.endpoint)
        response = r.get(url=f"{BASE_URL}/{self.endpoint}", auth=("", self.token))
        if response.status_code != 200:
            raise RequestFailed(response.content)
        return self.parse_list(response)

    def parse_list(self, response: r.Response):
        # Assume 200 status code
        return response.json()

    def create(self, data):
        if not self.token:
            raise TokenMissing
        if RequestType.CREATE not in self.request_types:
            raise RequestTypeNotAllowed
        headers = {"Content-Type" : "application/json"}
        response = r.post(url=f"{BASE_URL}/{self.endpoint}", data=data, headers=headers, auth=("", self.token))
        if response.status_code != 200:
            raise RequestFailed(response.content)
        return self.parse_create(response)

    def parse_create(self, response: r.Response):
        # Assume 200 status code
        return response.json()

    def delete(self, id):
        if not self.token:
            raise TokenMissing
        if RequestType.DELETE not in self.request_types:
            raise RequestTypeNotAllowed
        response = r.delete(url=f"{BASE_URL}/{self.endpoint}/{id}", auth=("", self.token))
        if response.status_code != 200:
            raise RequestFailed(response.content)
        return self.parse_delete(response)
    
    def parse_delete(self, response: r.Response):
        # Assume 200 status code
        return response.json()

class Lists(Endpoint):
    endpoint = "lists"
    request_types = [RequestType.GET, RequestType.LIST]
    
    def parse_get(self, response: r.Response) -> models.List:
        return models.List(**response.json())

    def parse_list(self, response: r.Response) -> list[models.List]:
        return [models.List(**i) for i in response.json()]

class ListEntries(Endpoint):
    request_types = [RequestType.GET, RequestType.LIST, RequestType.CREATE, RequestType.DELETE]

    def __init__(self, token: str, list_id: int):
        self.endpoint = f"lists/{list_id}/list-entries"
        super().__init__(token)

    def parse_list(self, response: r.Response) -> list[models.ListEntry]:
        return [models.ListEntry(**i) for i in response.json()]

    def parse_get(self, response: r.Response) -> models.ListEntry:
        return models.ListEntry(**response.json())

class Fields(Endpoint):
    endpoint = "fields"
    request_types = [RequestType.LIST, RequestType.CREATE, RequestType.DELETE]

    def parse_list(self, response: r.Response) -> list[models.Field]:
        return [models.Field(**i) for i in response.json()]
   
class Persons(Endpoint):
    endpoint = "persons"
    request_types = [RequestType.GET, RequestType.LIST, RequestType.CREATE, RequestType.DELETE]

    def parse_list(self, response: r.Response) -> dict:
        data = response.json()
        return {
                "persons" : [models.Person(**i) for i in data["persons"]],
                "next_page_token" : data["next_page_token"]
        }

    def parse_get(self, response: r.Response) -> models.Person:
        return models.Person(**response.json())
