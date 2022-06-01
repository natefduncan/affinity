import datetime as dt
from dataclasses import dataclass, field
from typing import Dict, Optional, Any
from affinity.common.constants import ListType, ActionType, PersonType, EntityType

#  https://api-docs.affinity.co/#fields
@dataclass
class DropdownOption:
    id: int
    text: str
    rank: int
    color: int

@dataclass
class Field:
    id: int
    name: str
    list_id: Optional[int]
    allows_multiple: bool
    dropdown_options: list[DropdownOption]
    value_type: int

#  https://api-docs.affinity.co/#lists
@dataclass
class List: 
    id: int
    type: ListType
    name: str
    public: bool
    owner_id: int
    list_size: int
    fields: list[Field] = field(default_factory=list) 

#  https://api-docs.affinity.co/#list-entries
@dataclass
class ListEntry:
    id: int
    list_id: int
    creator_id: int
    entity_id: int
    entity_type: EntityType
    entity: Any 
    created_at: dt.datetime

#  https://api-docs.affinity.co/#the-field-value-resource
@dataclass
class Location:
    street_address: str
    city: str
    state: str
    country: str

@dataclass
class Value:
    dropdown: Optional[str]
    number: Optional[int]
    person: Optional[int]
    organization: Optional[int]
    location: Optional[Location]
    date: Optional[dt.datetime]
    text: Optional[str]

@dataclass
class FieldValue:
    id: int
    field_id: int
    entity_id: int
    list_entry_id: int
    value: Value

#  https://api-docs.affinity.co/#the-field-value-change-resource
@dataclass
class FieldValueChange:
    id: int
    field_id: int
    entity_id: int
    list_entry_id: int
    action_type: ActionType
    value: Value

#  https://api-docs.affinity.co/#persons
@dataclass
class Interaction:
    date: dt.datetime
    person_ids: list[int]
        
@dataclass
class Person:
    id: int
    type: PersonType
    first_name: str
    last_name: str
    emails: list[str]
    primary_email: str
    organization_ids: list[int]
    opportunity_ids: list[int]
    list_entries: list[ListEntry]
    interaction_dates: Dict[str, dt.datetime]
    interactions: Dict[str, Interaction]
