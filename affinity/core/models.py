import datetime as dt
from typing import List, Dict, Optional
from affinity.common.constants import ListType, ActionType, PersonType

#  https://api-docs.affinity.co/#lists
class List: 
    def __init__(self, id: int, type: ListType, name: str, public: bool, owner_id: int, list_size: int):
        self.id = id
        self.type = type
        self.name = name
        self.public = public
        self.owner_id = owner_id
        self.list_size = list_size

#  https://api-docs.affinity.co/#list-entries
class ListEntry:
    def __init__(self, id: int, list_id: int, creator_id: int, entity_id: int, entity: Entity, created_at: dt.datetime):
        self.id = id
        self.list_id = list_id
        self.creator_id = creator_id
        self.entity_id = entity_id
        self.entity = entity
        self.created_at = created_at

#  https://api-docs.affinity.co/#fields
class DropdownOption:
    def __init__(self, id: int, text: str, rank: int, color: int):
        self.id = id
        self.text = text
        self.rank = rank
        self.color = color

class Field:
    def __init__(self, id: int, name: str, list_id: int, allows_multiple: bool, dropdown_options: List[DropdownOption], value_type: int):
        self.id = id
        self.name = name
        self.list_id = list_id
        self.allows_multiple = allows_multiple
        self.dropdown_options = dropdown_options
        self.value_type = value_type

#  https://api-docs.affinity.co/#the-field-value-resource
class Location:
    def __init__(self, street_address: str, city: str, state: str, country: str):
        self.street_address = street_address
        self.city = city
        self.state = state
        self.country = country

class Value:
    def __init__(self, dropdown: Optional[str], number: Optional[int], person: Optional[int], organization: Optional[int], location: Optional[Location], date: Optional[dt.datetime], text: Optional[str]):
        self.dropdown = dropdown
        self.number = number
        self.person = person
        self.organization = organization
        self.location = location
        self.date = date
        self.text = text

class FieldValue:
    def __init__(self, id: int, field_id: int, entity_id: int, list_entry_id: int, value: Value):
        self.id = id
        self.field_id = field_id
        self.entity_id = entity_id
        self.list_entry_id = list_entry_id
        self.value = value

#  https://api-docs.affinity.co/#the-field-value-change-resource
class FieldValueChange:
    def __init__(self, id: int, field_id: int, entity_id: int, list_entry_id: int, action_type: ActionType, value: Value):
        self.id = id
        self.field_id = field_id
        self.entity_id = entity_id
        self.list_entry_id = list_entry_id
        self.action_type = action_type
        self.value = value

#  https://api-docs.affinity.co/#persons
class Interaction:
    def __init__(self, date: dt.datetime, person_ids: List[int]):
        self.date = date
        self.person_ids = person_ids

class Person:
    def __init__(self, id: int, type: PersonType, first_name: str, last_name: str, emails: List[str], primary_email: str, organization_ids: List[int], opportunity_ids: List[int], list_entries: List[ListEntry], interaction_dates: Dict[str, dt.datetime], interactions: Dict[str, Interaction]): 
        self.id = id
        self.type = type
        self.first_name = first_name
        self.last_name = last_name
        self.emails = emails
        self.primary_email = primary_email
        self.organization_ids = organization_ids
        self.opportunity_ids = opportunity_ids
        self.list_entries = list_entries
        self.interaction_dates = interaction_dates
        self.interactions = interactions

