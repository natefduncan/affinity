from __future__ import annotations

import mimetypes
import datetime as dt
import io
import requests as r
from enum import Enum
from dataclasses import asdict
from typing import List, Optional, Dict


from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)

from affinity.common.exceptions import TokenMissing, RequestTypeNotAllowed, RequestFailed, RequiredPayloadFieldMissing, RequiredQueryParamMissing, ClientError
from affinity.common.constants import EntityType, InteractionType, ReminderResetType, ReminderType, ValueType
from affinity.core import models

BASE_URL = "https://api.affinity.co"


class RequestType(Enum):
    GET = 1
    LIST = 2
    CREATE =  3
    DELETE = 4
    UPDATE = 5


class Endpoint:
    endpoint: str = ""
    allowed_request_types: List[RequestType] = []
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

    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(5))
    def _get(self, query_params: Optional[dict] = None,  **kwargs):

        query_params = query_params if query_params else {}
        if not self.token:
            raise TokenMissing
        if RequestType.GET not in self.allowed_request_types:
            raise RequestTypeNotAllowed

        self.verify_query_params(query_params)
        url = self.construct_url(query_params)
        response = r.get(url=url, auth=("", self.token), allow_redirects=True)
        if response.status_code != 200:
            raise RequestFailed(response.content)
        return self.parse_get(response, **kwargs)

    def parse_get(self, response: r.Response, **kwargs):

        response.raise_for_status()
        return response.json()

    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(5))
    def _download(self, save_path: str):
        if not self.token:
            raise TokenMissing
        if RequestType.GET not in self.allowed_request_types:
            raise RequestTypeNotAllowed
        url = self.construct_url({})
        response = r.get(url=url, auth=("", self.token), allow_redirects=True)
        if response.status_code != 200:
            raise RequestFailed(response.content)
        return self.parse_download(response, save_path)

    def parse_download(self, response: r.Response, save_path: str):
        # Assume 200 status code
        with open(save_path, "wb") as file:
            file.write(response.content)

    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(5))
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

    def _upload(self, files: dict, form: dict):
        if not self.token:
            raise TokenMissing
        if RequestType.CREATE not in self.allowed_request_types:
            raise RequestTypeNotAllowed
        url = self.construct_url({})
        # FIXME: Figure out how to upload multiple files
        responses = []
        for file_name, file in files.items():
            response = r.post(url=url, files={"file" : (file_name, file, mimetypes.guess_type(file_name)[0])}, params=form, auth=("", self.token))
            if response.status_code != 200:
                raise RequestFailed(response.content)
            responses.append(self.parse_create(response))
        return responses

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
        return self._get(None)
 
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
        return self._get(None)

    def parse_get(self, response: r.Response) -> models.ListEntry:
        return models.ListEntry(**response.json())

    def list(self, page_size: Optional[int] = None, page_token: Optional[str] = None):
        self.endpoint = f"lists/{self.list_id}/list-entries"
        query_params = {k: v for k,v in locals().items() if k != "self" and v != None}
        return self._list(query_params=query_params)

    def parse_list(self, response: r.Response) -> List[models.ListEntry]:
        return [models.ListEntry(**i) for i in response.json()]

    def create(self, entity_id: int, creator_id: Optional[int] = None):
        payload = {k: v for k,v in locals().items() if k != "self" and v != None}
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

    def list(self, list_id: Optional[int] = None, value_type: Optional[int] = None, with_modified_names: Optional[bool] = False):
        query_params = {k: v for k,v in locals().items() if k != "self" and v != None}
        return self._list(query_params=query_params)

    def parse_list(self, response: r.Response) -> List[models.Field]:
        return [models.Field(**i) for i in response.json()]
    
    # Default create
    def create(self, name: str, entity_type: EntityType, value_type: ValueType, list_id: Optional[int] = None, allows_multiple: Optional[bool] = None, is_list_specific: Optional[bool] = None, is_required : Optional[bool] = None):
        payload = {k: v for k,v in locals().items() if k != "self" and v != None}
        return self._create(payload)

    def parse_create(self, response: r.Response) -> models.Field:
        return models.Field(**response.json())

    def delete(self, field_id: int):
        self.endpoint = f"fields/{field_id}"
        return self._delete()

    # Default parse delete


def parse_value(fields, field_value) -> models.Value:
    value = {k: None for k in ["person","organization","dropdown", "number", "date", "location", "text", "ranked_dropdown", "opportunity"]}
    field = next((f for f in fields if f.id == field_value['field_id']), None)
    if field:
        if field.value_type == ValueType.person:
            value["person"] = field_value["value"]
        elif field.value_type == ValueType.organization:
            value["organization"] = field_value["value"]
        elif field.value_type == ValueType.dropdown:
            value["dropdown"] = field_value["value"]
        elif field.value_type == ValueType.number:
            value["number"] = field_value["value"]
        elif field.value_type == ValueType.date:
            value["date"] = field_value["value"]
        elif field.value_type == ValueType.location:
            value["location"] = models.Location(**field_value["value"])
        elif field.value_type == ValueType.text:
            value["text"] = field_value["value"]
        elif field.value_type == ValueType.ranked_dropdown:
            value["ranked_dropdown"] = field_value["value"]
        elif field.value_type == ValueType.opportunity:
            value["opportunity"] = field_value["value"]
    return models.Value(**value)


class FieldValues(Endpoint):
    endpoint = "field-values"
    allowed_request_types = [RequestType.LIST, RequestType.CREATE, RequestType.DELETE, RequestType.UPDATE]

    def list(self, person_id: Optional[int] = None, organization_id: Optional[int] = None, opportunity_id: Optional[int] = None, list_entry_id: Optional[int] = None):
        query_params = {k: v for k,v in locals().items() if k != "self" and v != None}
        if not query_params:
            raise RequiredQueryParamMissing("Must have person_id, organization_id, opportunity_id, or list_entry_id")
        if len(query_params) != 1:
            raise ClientError("Can only input one query parameter for this endpoint")
        return self._list(query_params)

    def parse_list(self, response: r.Response) -> List[models.FieldValue]:
        fields = Fields(self.token).list()
        fvs = []
        for fv in response.json():
            value = parse_value(fields, fv)
            fvs.append(models.FieldValue(**{
                "id" : fv['id'],
                "field_id" : fv['field_id'], 
                "list_entry_id" : fv["list_entry_id"], 
                "entity_id": fv["entity_id"], 
                "value" : value
                })
            )
        return fvs 

    def create(self, field_id: int, entity_id: int, value: models.Value, list_entry_id: Optional[int] = None):
        payload = {k: v for k,v in locals().items() if k != "self" and v != None}
        value = [v for v in asdict(value).values() if v][0]
        payload["value"] = value 
        return self._create(payload)
    
    def parse_create(self, response: r.Response) -> models.FieldValue:
        fields = Fields(self.token).list()
        field_value = response.json()
        value = parse_value(fields, field_value)
        return models.FieldValue(**{
            "id" : field_value["id"], 
            "field_id" : field_value["field_id"],
            "list_entry_id" : field_value["list_entry_id"], 
            "entity_id" : field_value["entity_id"], 
            "value" : value
        })

    def update(self, field_value_id: int, value: models.Value):
        value = [v for v in asdict(value).values() if v][0]
        self.endpoint = f"field-values/{field_value_id}"
        return self._update({"value": value})

    # Default parse update

    def delete(self, field_value_id: int):
        self.endpoint = f"field-values/{field_value_id}"
        return self._delete()

    # Default parse delete


class Persons(Endpoint):
    endpoint = "persons"
    allowed_request_types = [RequestType.GET, RequestType.LIST, RequestType.CREATE, RequestType.DELETE, RequestType.UPDATE]

    def fields(self) -> dict:
        self.endpoint = "persons/fields"
        return self._get(None, is_fields=True)

    # TODO: Impl min&max_{interaction_type}_date query parms
    def list(self, term: Optional[str] = None, with_interaction_dates: Optional[bool] = None, with_current_organizations: Optional[bool] = None, with_interaction_persons: Optional[bool] = None, with_opportunities: Optional[bool] = None, page_size: Optional[int] = None, page_token: Optional[str] = None):
        query_params = {k: v for k,v in locals().items() if k != "self" and v != None}
        return self._list(query_params=query_params)

    def parse_list(self, response: r.Response) -> dict:
        data = response.json()
        return {
            "persons" : [models.Person(**i) for i in data["persons"]],
            "next_page_token" : data["next_page_token"]
        }

    def get(self, person_id: int,  with_interaction_dates: Optional[bool] = None, with_interaction_persons: Optional[bool] = None, with_opportunities: Optional[bool] = None, with_current_organizations: bool = None):

        self.endpoint = f"persons/{person_id}"

        query_params = {k: v for k, v in locals().items() if k not in ["self", "person_id"] and v is not None}
        return self._get(query_params=query_params)

    def parse_get(self, response: r.Response, **kwargs) -> models.Person | List[models.PersonFields]:
        if kwargs.get('is_fields'):
            return [models.PersonFields(**i) for i in response.json()]
        return models.Person(**response.json())
 
    def create(self, first_name: str, last_name: str, emails: List[str], organization_ids: List[int] = []):
        payload = {k: v for k,v in locals().items() if k != "self" and v != None}
        return self._create(payload)

    def parse_create(self, response: r.Response) -> models.Person:
        return models.Person(**response.json())

    def delete(self, person_id: int):
        self.endpoint = f"persons/{person_id}"
        return self._delete()

    # Default parse delete

    def update(self, person_id: int, first_name: Optional[str] = None, last_name: Optional[str] = None, emails: List[str] = [], organization_ids: List[int] = []): 
        payload = {k: v for k,v in locals().items() if k != "self" and v != None}
        payload.pop("person_id", None)
        self.endpoint = f"persons/{person_id}"
        return self._update(payload)

    # Default parse update


class Organizations(Endpoint):
    endpoint = "organizations"
    allowed_request_types = [RequestType.GET, RequestType.LIST, RequestType.CREATE, RequestType.DELETE, RequestType.UPDATE]

    def fields(self) -> dict:
        self.endpoint = "organizations/fields"
        return self._get(None, is_fields=True)

    # TODO: Impl min&max_{interaction_type}_date query params
    def list(self, term: Optional[str] = None, with_interaction_dates: Optional[bool] = None, with_interaction_persons: Optional[bool] = None, with_opportunities: Optional[bool] = None, page_size: Optional[int] = None, page_token: Optional[str] = None):
        query_params = {k: v for k,v in locals().items() if k != "self" and v != None}
        return self._list(query_params=query_params)

    def parse_list(self, response: r.Response) -> dict:
        data = response.json()
        return {
            "organizations" : [models.Organization.from_dict(i) for i in data["organizations"]],
            "next_page_token" : data["next_page_token"]
        }

    def get(self, organization_id: int, with_interaction_dates: Optional[bool] = None, with_interaction_persons: Optional[bool] = None, with_opportunities: Optional[bool] = None):
        self.endpoint = f"organizations/{organization_id}"
        query_params = {k: v for k, v in locals().items() if k not in ["self", "organization_id"] and v is not None}

        return self._get(query_params=query_params)

    def get_by_domain(self, domain: str, with_interaction_dates: Optional[bool] = None, with_interaction_persons: Optional[bool] = None, with_opportunities: Optional[bool] = None, with_people: Optional[bool] = True):

        # https://api.affinity.co/organizations?term=abaka.me
        query_params = {k: v for k, v in locals().items() if k not in ["self", "domain"] and v is not None}
        query_params.update({"term": domain})
        org_candidates = self._list(query_params=query_params).get('organizations')
        if not org_candidates:
            return None
        for org in org_candidates:
            if org.domain == domain:
                if with_interaction_dates or with_interaction_persons or with_opportunities or with_people:
                    return self.get(org.id, with_interaction_dates, with_interaction_persons, with_opportunities)
                return org

    def parse_get(self, response: r.Response, **kwargs) -> models.Organization | List[models.OrganizationFields]:
        if kwargs.get('is_fields'):
            return [models.OrganizationFields(**i) for i in response.json()]
        return models.Organization.from_dict(response.json())

    def create(self, name: str, domain: Optional[str] = None, person_ids: List[int] = []):
        payload = {k: v for k,v in locals().items() if k != "self" and v != None}
        return self._create(payload)

    def parse_create(self, response: r.Response) -> models.Organization:
        return models.Organization.from_dict(response.json())

    def delete(self, organization_id: int):
        self.endpoint = f"organizations/{organization_id}"
        return self._delete()

    # Default parse delete

    def update(self, organization_id: int, name: Optional[str] = None, domain: Optional[str] = None, person_ids: List[int] = []):
        payload = {k: v for k,v in locals().items() if k != "self" and v != None}
        payload.pop("organization_id", None)
        self.endpoint = f"organizations/{organization_id}"
        return self._update(payload)

    # Default parse update


class Opportunities(Endpoint):
    endpoint = "opportunities"
    allowed_request_types = [RequestType.GET, RequestType.LIST, RequestType.CREATE, RequestType.DELETE, RequestType.UPDATE]

    def list(self, term: Optional[str] = None, page_size: Optional[int] = None, page_token: Optional[str] = None):
        query_params = {k: v for k,v in locals().items() if k != "self" and v != None}
        return self._list(query_params=query_params)

    def parse_list(self, response: r.Response) -> dict:
        data = response.json()
        return {
            "opportunities" : [models.Opportunity(**i) for i in data["opportunities"]],
            "next_page_token" : data["next_page_token"]
        }

    def get(self, opportunity_id: int):
        self.endpoint = f"opportunities/{opportunity_id}"
        return self._get(None)

    def parse_get(self, response: r.Response) -> models.Opportunity:
        return models.Opportunity(**response.json())

    def create(self, name: str, list_id: int, person_ids: List[int] = [], organization_ids: List[int] = []):
        payload = {k: v for k,v in locals().items() if k != "self" and v != None}
        return self._create(payload)
    
    def parse_create(self, response: r.Response) -> models.Opportunity:
        return models.Opportunity(**response.json())

    def delete(self, opportunity_id: int):
        self.endpoint = f"opportunities/{opportunity_id}"
        return self._delete()

    # Default parse delete

    def update(self, opportunity_id: int, name: Optional[str], person_ids: List[int] = [], organization_ids: List[int] = []):
        payload = {k: v for k,v in locals().items() if k != "self" and v != None}
        payload.pop("opportunity_id", None)
        self.endpoint = f"opportunities/{opportunity_id}"
        return self._update(payload)

    # Default parse update


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


class RelationshipsStrengths(Endpoint):
    endpoint = "relationships-strengths"
    allowed_request_types = [RequestType.LIST]
    required_query_params = ["external_id"]

    def list(self, external_id: int, internal_id: Optional[int] = None):
        query_params = {k: v for k,v in locals().items() if k != "self" and v != None}
        return self._list(query_params=query_params)

    def parse_list(self, response: r.Response) -> List[models.RelationshipStrength]:
        return [models.RelationshipStrength(**i) for i in response.json()]


class Notes(Endpoint):
    endpoint = "notes"
    allowed_request_types = [RequestType.GET, RequestType.LIST, RequestType.CREATE, RequestType.DELETE, RequestType.UPDATE]

    def list(self, person_id: Optional[int] = None, organization_id: Optional[int] = None, opportunity_id: Optional[int] = None, creator_id: Optional[int] = None):
        query_params = {k: v for k,v in locals().items() if k != "self" and v != None}
        return self._list(query_params=query_params)

    def parse_list(self, response: r.Response) -> dict:
        data = response.json()
        data["notes"] = [models.Note(**i) for i in data["notes"]]
        return data

    def get(self, note_id: int):
        self.endpoint = f"notes/{note_id}"
        return self._get(None)

    def parse_get(self, response: r.Response) -> models.Note:
        return models.Note(**response.json())

    def create(self, person_ids: List[int] = [], organization_ids: List[int] = [], opportunity_ids: List[int] = [], content: Optional[str] = None, gmail_id: Optional[str] = None, creator_id: Optional[int] = None, created_at: Optional[dt.datetime] = None):
        payload = {k: v for k,v in locals().items() if k != "self" and v != None}
        # Must have either gmail_id or content
        if "content" not in payload and "gmail_id" not in payload:
            raise RequiredPayloadFieldMissing("Must have either 'content' or 'gmail_id' in payload")
        return self._create(payload)

    def parse_create(self, response: r.Response) -> models.Note:
        return models.Note(**response.json())

    def delete(self, note_id: int):
        self.endpoint = f"notes/{note_id}"
        return self._delete()

    # Default parse delete

    def update(self, note_id: int, content: str):
        #  You cannot update the content of a note that has mentions. 
        #  You also cannot update the content of a note associated with an email.
        self.endpoint = f"notes/{note_id}"
        return self._update({"content" : content})

    # Default parse update


class EntityFiles(Endpoint):
    endpoint = "entity-files"
    allowed_request_types = [RequestType.GET, RequestType.LIST, RequestType.CREATE] 

    def list(self, opportunity_id: Optional[int] = None, person_id: Optional[int] = None, organization_id: Optional[int] = None, page_size: Optional[int] = None, page_token: Optional[str] = None):
        query_params = {k: v for k,v in locals().items() if k != "self" and v != None}
        return self._list(query_params=query_params)

    def parse_list(self, response: r.Response) -> dict:
        data = response.json()
        print(data["entity_files"][0])
        data["entity_files"] = [models.EntityFile(**i) for i in data["entity_files"]]
        return data

    def get(self, entity_file_id: int):
        self.path = f"entity-files/{entity_file_id}"
        return self._get(None)

    def parse_get(self, response: r.Response) -> models.EntityFile:
        data = response.json()["entity_files"][0] # API response is formatted strangely
        return models.EntityFile(**data)
    
    def download(self, entity_file_id: int, save_path: str): 
        self.endpoint = f"entity-files/download/{entity_file_id}"
        return self._download(save_path)

    # Default parse download

    def upload(self, files: Dict[str, io.IOBase], person_id: Optional[int] = None, organization_id: Optional[int] = None, opportunity_id : Optional[int] = None):
        payload = {k: v for k,v in locals().items() if k != "self" and v != None}
        payload.pop("files", None)
        has_person = "person_id" in payload
        has_organization = "organization_id" in payload
        has_opportunity = "opportunity_id" in payload
        if sum([has_person, has_organization, has_opportunity]) != 1:
            raise RequiredPayloadFieldMissing("Must have one of person_id, organization_id, or opportunity_id")
        return self._upload(files=files, form=payload)

    # Default parse create


class Reminders(Endpoint):
    endpoint = "reminders"
    allowed_request_types = [RequestType.GET, RequestType.LIST, RequestType.CREATE, RequestType.DELETE, RequestType.UPDATE]

    def list(self, person_id: Optional[int] = None, organization_id: Optional[int] = None, opportunity_id: Optional[int] = None, creator_id: Optional[int] = None, owner_id: Optional[int] = None, completer_id: Optional[int] = None, type: Optional[int] = None, reset_type: Optional[int] = None, status: Optional[int] = None, due_before: Optional[str] = None, due_after: Optional[str] = None, page_size: Optional[int] = None, page_token: Optional[str] = None):
        query_params = {k: v for k,v in locals().items() if k != "self" and v != None}
        return self._list(query_params=query_params)

    def parse_list(self, response: r.Response) -> dict:
        data = response.json()
        data["reminders"] = [models.Reminder(**i) for i in data["reminders"]]
        return data

    def get(self, reminder_id: int):
        self.endpoint = f"reminders/{reminder_id}"
        return self._get(None)

    def parse_get(self, response: r.Response) -> models.Reminder:
        return models.Reminder(**response.json())

    def create(self, owner_id: int, type: ReminderType, content: Optional[str] = None, reset_type: Optional[ReminderResetType] = None, person_id: Optional[int] = None, organization_id: Optional[int] = None, opportunity_id: Optional[int] = False, due_date : Optional[str] = None, reminder_days: Optional[int] = None, is_completed: Optional[int] = None):
        payload = {k: v for k,v in locals().items() if k != "self" and v != None}
        if type:
            if type == 1:
                if "reset_type" not in payload:
                    raise RequiredPayloadFieldMissing("Must specify reset type if type == 1")
                if "reminder_days" not in payload:
                    raise RequiredPayloadFieldMissing("Must specify reminder days if type == 1")
            elif type == 0:
                if "due_date" not in payload:
                    raise RequiredPayloadFieldMissing("Must specify due date if type == 0")
        return self._create(payload)

    def parse_create(self, response: r.Response) -> models.Reminder:
        return models.Reminder(**response.json())

    def delete(self, reminder_id: int):
        self.endpoint = f"reminders/{reminder_id}"
        return self._delete()

    # Default parse delete

    def update(self, reminder_id: int, owner_id: Optional[int] = None, type: Optional[ReminderType] = None, content: Optional[str] = None, reset_type: Optional[ReminderResetType] = None, person_id: Optional[int] = None, organization_id: Optional[int] = None, opportunity_id: Optional[int] = False, due_date : Optional[str] = None, reminder_days: Optional[int] = None, is_completed: Optional[int] = None):
        payload = {k: v for k,v in locals().items() if k != "self" and v != None}
        payload.pop("reminder_id", None)
        self.endpoint = f"reminders/{reminder_id}"
        return self._update(payload)

    # Default parse update


class WhoAmI(Endpoint):
    endpoint = "auth/whoami"
    allowed_request_types = [RequestType.GET]

    def get(self):
        return self._get(None)
    
    # Default parse get


class FieldValueChanges(Endpoint):
    endpoint = "field-value-changes"
    allowed_request_types = [RequestType.LIST]

    def list(self, field_id: int, action_type: Optional[int] = None, person_id: Optional[int] = None, organization_id: Optional[int] = None, opportunity_id: Optional[int] = None, list_entry_id: Optional[int] = None):
        query_params = {k: v for k,v in locals().items() if k != "self" and v != None}
        return self._list(query_params=query_params)

    def parse_list(self, response: r.Response) -> List[models.FieldValueChange]:
        fields = Fields(self.token).list()
        fvs = []
        for fv in response.json():
            value = parse_value(fields, fv)
            fv.update({"value": value})
            fvs.append(models.FieldValueChange(**fv))
        return fvs


class Webhooks(Endpoint):
    endpoint = "webhook"
    allowed_request_types = [RequestType.LIST, RequestType.GET, RequestType.CREATE, RequestType.UPDATE, RequestType.DELETE]

    def list(self):
        return self._list(query_params={})

    def parse_list(self, response: r.Response) -> List[models.Webhook]:
        return [models.Webhook(**i) for i in response.json()]

    def get(self, webhook_subscription_id: int):
        self.endpoint = f"webhook/{webhook_subscription_id}"
        return self._get(None)

    def parse_get(self, response: r.Response) -> models.Webhook:
        return models.Webhook(**response.json())

    def create(self, webhook_url: str, subscriptions: List[str] = []):
        payload = {k: v for k,v in locals().items() if k != "self" and v != None}
        return self._create(payload)

    # Default parse create

    def update(self, webhook_subscription_id: int, webhook_url: Optional[str] = None, subscriptions: List[str] = [], disabled: Optional[bool] = None):
        payload = {k: v for k,v in locals().items() if k != "self" and v != None}
        payload.pop("webhook_subscription_id", None)
        self.endpoint = "webhook/{webhook_subscription_id}"
        return self._update(payload)

    # Default parse update

    def delete(self, webhook_subscription_id: int):
        self.endpoint = f"webhook/{webhook_subscription_id}"
        return self._delete()

    # Default parse delete
