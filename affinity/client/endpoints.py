import datetime as dt
import requests as r
from enum import Enum
from typing import List, Optional
from affinity.common.exceptions import TokenMissing, RequestTypeNotAllowed, RequestFailed, RequiredPayloadFieldMissing, RequiredQueryParamMissing
from affinity.common.constants import InteractionType
from affinity.core import models

BASE_URL = "https://api.affinity.co"

class RequestType(Enum):
    GET = 1
    LIST = 2
    CREATE =  3
    DELETE = 4
    UPDATE = 5

class Endpoint:
    endpoint : str = ""
    allowed_request_types: List[RequestType] = []
    required_payload_fields: List[str] = []
    required_query_params: List[str] = []
    
    def __init__(self, token: str):
        self.token = token

    def construct_url(self, query_params: dict) -> str:
        query_path = "&".join([f"{key}={value}" for key, value in query_params.items()])
        return f"{BASE_URL}/{self.endpoint}?{query_path}"

    def verify_query_params(self, params: dict):
        for r in self.required_query_params:
            if r not in params:
                raise RequiredQueryParamMissing(r) 

    def verify_payload_fields(self, data: dict):
        for f in self.required_payload_fields:
            if f not in data:
                raise RequiredPayloadFieldMissing(f)

    def _get(self):
        if not self.token:
            raise TokenMissing
        if RequestType.GET not in self.allowed_request_types:
            raise RequestTypeNotAllowed
        url = self.construct_url({})
        response = r.get(url=url, auth=("", self.token))
        if response.status_code != 200:
            raise RequestFailed(response.content)
        return self.parse_get(response)

    def parse_get(self, response: r.Response):
        # Assume 200 status code
        return response.json()

    def _list(self, query_params: dict):
        if not self.token:
            raise TokenMissing
        if RequestType.LIST not in self.allowed_request_types:
            raise RequestTypeNotAllowed
        self.verify_query_params(query_params)
        url = self.construct_url(query_params)
        response = r.get(url=url, auth=("", self.token))
        if response.status_code != 200:
            raise RequestFailed(response.content)
        return self.parse_list(response)

    def list(self, query_params: dict = {}):
        return self._list(query_params)

    def parse_list(self, response: r.Response):
        # Assume 200 status code
        return response.json()

    def _create(self, payload: dict):
        if not self.token:
            raise TokenMissing
        if RequestType.CREATE not in self.allowed_request_types:
            raise RequestTypeNotAllowed
        headers = {"Content-Type" : "application/json"}
        self.verify_payload_fields(payload)
        url = self.construct_url({})
        response = r.post(url=url, json=payload, headers=headers, auth=("", self.token))
        if response.status_code != 200:
            raise RequestFailed(response.content)
        return self.parse_create(response)

    def create(self, payload: dict = {}):
        return self._create(payload)

    def parse_create(self, response: r.Response):
        # Assume 200 status code
        return response.json()

    def _delete(self):
        if not self.token:
            raise TokenMissing
        if RequestType.DELETE not in self.allowed_request_types:
            raise RequestTypeNotAllowed
        url = self.construct_url({})
        response = r.delete(url=url, auth=("", self.token))
        if response.status_code != 200:
            raise RequestFailed(response.content)
        return self.parse_delete(response)
    
    def parse_delete(self, response: r.Response):
        # Assume 200 status code
        return response.json()

    def _update(self, payload: dict):
        if not self.token:
            raise TokenMissing
        if RequestType.UPDATE not in self.allowed_request_types:
            raise RequestTypeNotAllowed
        headers = {"Content-Type" : "application/json"}
        url = self.construct_url(payload)
        response = r.put(url=url, auth=("", self.token), headers=headers)
        if response.status_code != 200:
            raise RequestFailed(response.content)
        return self.parse_update(response)

    def parse_update(self, response: r.Response):
        # Assume 200 status code
        return response.json()

    def update(self, payload: dict = {}):
        return self._update(payload)
    
class Lists(Endpoint):
    allowed_request_types = [RequestType.GET, RequestType.LIST]
    endpoint = "lists"
    
    def get(self, list_id: int):
        self.endpoint = f"lists/{list_id}"
        return self._get()
 
    def parse_get(self, response: r.Response) -> models.List:
        return models.List(**response.json())
       
    # Default list

    def parse_list(self, response: r.Response) -> list[models.List]:
        return [models.List(**i) for i in response.json()]

class ListEntries(Endpoint):
    allowed_request_types = [RequestType.GET, RequestType.LIST, RequestType.CREATE, RequestType.DELETE]

    def __init__(self, list_id: int, token: str):
        self.list_id = list_id
        super().__init__(token)

    def get(self, list_entry_id: int):
        self.endpoint = f"lists/{self.list_id}/list-entries/{list_entry_id}"
        return self._get()

    def parse_get(self, response: r.Response) -> models.ListEntry:
        return models.ListEntry(**response.json())

    def list(self, page_size: Optional[int] = None, page_token: Optional[str] = None):
        self.endpoint = f"lists/{self.list_id}/list-entries"
        query_params = {k: v for k,v in locals().get("kwargs", {}).items() if v}
        return self._list(query_params=query_params)

    def parse_list(self, response: r.Response) -> List[models.ListEntry]:
        return [models.ListEntry(**i) for i in response.json()]

    def create(self, payload: dict):
        self.endpoint = f"lists/{self.list_id}/list-entries"
        return self._create(payload)

    def parse_create(self, response: r.Response) -> models.ListEntry:
        return models.ListEntry(**response.json())

    def delete(self, list_entry_id: int):
        self.endpoint = f"lists/{self.list_id}/list-entries/{list_entry_id}"
        return self._delete()
       
    # Default parse delete

class Fields(Endpoint):
    endpoint = "fields"
    allowed_request_types = [RequestType.LIST, RequestType.CREATE, RequestType.DELETE]
    required_payload_fields = ["name", "entity_type", "value_type"]

    def list(self, list_id: Optional[int] = None, value_type: Optional[int] = None, with_modified_names: Optional[bool] = False):
        query_params = {k: v for k,v in locals().get("kwargs", {}).items() if v}
        return self._list(query_params=query_params)

    def parse_list(self, response: r.Response) -> List[models.Field]:
        return [models.Field(**i) for i in response.json()]
    
    # Default create

    def parse_create(self, response: r.Response) -> models.Field:
        return models.Field(**response.json())

    def delete(self, field_id: int):
        self.endpoint = f"fields/{field_id}"
        return self._delete()

    # Default parse delete
    
class Persons(Endpoint):
    endpoint = "persons"
    allowed_request_types = [RequestType.GET, RequestType.LIST, RequestType.CREATE, RequestType.DELETE, RequestType.UPDATE]
    required_payload_fields = ["first_name", "last_name", "emails"]

    # TODO: Impl min&max_{interaction_type}_date query parms
    def list(self, term: Optional[str] = None, with_interaction_dates: Optional[bool] = None, with_interaction_persons: Optional[bool] = None, with_opportunities: Optional[bool] = None, page_size: Optional[int] = None, page_token: Optional[str] = ""):
        query_params = {k: v for k,v in locals().get("kwargs", {}).items() if v}
        return self._list(query_params=query_params)

    def parse_list(self, response: r.Response) -> dict:
        data = response.json()
        return {
            "persons" : [models.Person(**i) for i in data["persons"]],
            "next_page_token" : data["next_page_token"]
        }

    def get(self, person_id: int):
        self.endpoint = f"persons/{person_id}"
        return self._get()

    def parse_get(self, response: r.Response) -> models.Person:
        return models.Person(**response.json())
 
    # Default create

    def parse_create(self, response: r.Response) -> models.Person:
        return models.Person(**response.json())

    def delete(self, person_id: int):
        self.endpoint = f"persons/{person_id}"
        return self._delete()

    # Default parse delete

    def update(self, person_id: int, payload: dict):
        self.endpoint = f"persons/{person_id}"
        return self._update(payload)

class Organizations(Endpoint):
    endpoint = "organizations"
    allowed_request_types = [RequestType.GET, RequestType.LIST, RequestType.CREATE, RequestType.DELETE]
    required_payload_fields = ["name"]

    # TODO: Impl min&max_{interaction_type}_date query params
    def list(self, term: Optional[str] = None, with_interaction_dates: Optional[bool] = None, with_interaction_persons: Optional[bool] = None, with_opportunities: Optional[bool] = None, page_size: Optional[int] = None, page_token: Optional[str] = ""):
        query_params = {k: v for k, v in locals().get("kwargs", {}).items() if v}
        return self._list(query_params=query_params)

    def parse_list(self, response: r.Response) -> dict:
        data = response.json()
        return {
            "organizations" : [models.Organization.from_dict(i) for i in data["organizations"]],
            "next_page_token" : data["next_page_token"]
        }

    def get(self, organization_id: int):
        self.endpoint = f"organizations/{organization_id}"
        return self._get()

    def parse_get(self, response: r.Response) -> models.Organization:
        return models.Organization.from_dict(response.json())

class Interactions(Endpoint):
    endpoint = "interactions"
    allowed_request_types = [RequestType.GET, RequestType.LIST, RequestType.CREATE, RequestType.DELETE]

    def __init__(self, token: str, type: InteractionType):
        self.type = type
        super().__init__(token)

    def parse_list(self, response: r.Response) -> dict:
        data = response.json()
        return {
            "emails" : [models.EmailInteraction.from_dict(i) for i in data["emails"]],
            "next_page_token": data["next_page_token"]
        }
