import datetime as dt
from dataclasses_json import config, dataclass_json
from dataclasses import dataclass, field
from typing import Dict, Optional, Any

from marshmallow import fields
from affinity.common.constants import (
    ListType,
    ActionType,
    PersonType,
    EntityType,
    InteractionType,
    DirectionType,
    LoggingType,
    ReminderType,
    ReminderResetType,
    ReminderStatusType,
    NoteCreationType,
    ValueType,
)



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
    enrichment_source: Optional[str]
    track_changes: bool
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
    creator_id: int
    fields: list[Field] = field(default_factory=list) 


#  https://api-docs.affinity.co/#list-entries
@dataclass
class ListEntry:
    id: int
    list_id: int
    creator_id: int
    entity_id: int
    entity_type: EntityType
    created_at: dt.datetime = field(
        metadata=config(
            encoder=dt.datetime.isoformat,
            decoder=dt.datetime.fromisoformat,
            mm_field=fields.DateTime(format="iso"),
        )
    )
    entity: Optional[Any] = None


#  https://api-docs.affinity.co/#the-field-value-resource
@dataclass
class Location:
    street_address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    country: Optional[str]
    continent: Optional[str]


@dataclass
class Value:
    dropdown: Optional[str] = None
    number: Optional[int] = None
    person: Optional[int] = None
    organization: Optional[int] = None
    location: Optional[Location] = None
    date: Optional[dt.datetime] = None
    text: Optional[str] = None
    opportunity: Optional[int] = None
    ranked_dropdown: Optional[str] = None


@dataclass
class FieldValue:
    id: int
    field_id: int
    entity_id: int
    list_entry_id: int
    value: Value


 #  https://api-docs.affinity.co/#persons
@dataclass
class ShortInteraction:
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
    organization_ids: list[int] = field(default_factory=list) 
    opportunity_ids: list[int] = field(default_factory=list)
    list_entries: list[ListEntry] = field(default_factory=list) 
    interaction_dates: Dict[str, dt.datetime] = field(default_factory=dict) 
    interactions: Dict[str, ShortInteraction] = field(default_factory=dict)
    current_organization_ids: list[int] = field(default_factory=list)


#  https://api-docs.affinity.co/#the-field-value-change-resource
@dataclass
class FieldValueChange:
    id: int
    field_id: int
    entity_id: int
    entity_attribute_id: int
    changer: Person
    changed_at: dt.datetime
    list_entry_id: int
    action_type: ActionType
    value: Value
    person: Optional[dict]
    company: Optional[dict]
    opp: Optional[dict]


@dataclass_json
@dataclass
class Organization:
    id: int
    name: str
    domain: str
    domains: list[str]
    crunchbase_uuid: Optional[str]
    global_: Optional[bool] = field(metadata=config(field_name="global"))
    # global_: Optional[bool] = field(alias="global")
    person_ids: list[int] = field(default_factory=list)
    opportunity_ids: list[int] = field(default_factory=list) 
    list_entries: list[ListEntry] = field(default_factory=list)
    interaction_dates: dict = field(default_factory=dict)
    interactions: dict = field(default_factory=dict)



@dataclass_json
@dataclass(frozen=True)     # make the dataclasses immutable and hashable by freezing.
class OrganizationFields:
    id: int
    name: str
    value_type: ValueType
    enrichment_source: Optional[str]
    list_id: Optional[int]
    allows_multiple: bool
    track_changes: bool
    dropdown_options: list[DropdownOption]


@dataclass_json
@dataclass(frozen=True)     # make the dataclasses immutable and hashable by freezing.
class PersonFields:
    id: int
    name: str
    value_type: ValueType
    enrichment_source: Optional[str]
    list_id: Optional[int]
    allows_multiple: bool
    track_changes: bool
    dropdown_options: list[DropdownOption]


@dataclass
class EmailInteraction:
    date: dt.datetime
    id: int
    subject: str
    type: InteractionType
    from_: Person = field(metadata=config(field_name="from"))
    to: list[Person] 
    cc: list[Person]
    direction: DirectionType


@dataclass
class Opportunity:
    id: int
    name: str
    person_ids: list[int] = field(default_factory=list)
    organization_ids: list[int] = field(default_factory=list)
    list_entries: list[ListEntry] = field(default_factory=list)


@dataclass
class RelationshipStrength:
    internal_id: int
    external_id: int
    strength: float


@dataclass
class Note:
    id: int
    creator_id: int
    parent_id: int
    content: str
    created_at: dt.datetime
    is_meeting: bool
    updated_at: Optional[dt.datetime] = None
    mentioned_person_ids: list = field(default_factory=list)
    person_ids: list[int] = field(default_factory=list)
    organization_ids: list[int] = field(default_factory=list)
    opportunity_ids: list[int] = field(default_factory=list)
    associated_person_ids: list[int] = field(default_factory=list)
    interaction_person_ids: list[int] = field(default_factory=list)
    interaction_id: Optional[int] = None
    interaction_type: Optional[InteractionType] = None
    type: Optional[NoteCreationType] = None


@dataclass
class EntityFile:
    id: int
    name: str
    size: int
    person_id: int
    organization_id: int
    opportunity_id: int
    uploader_id: int
    created_at: dt.datetime
    personId: Optional[int] = None # Duplicate in API response
    organizationId: Optional[int] = None # Duplicate in API response 
    opportunityId: Optional[int] = None # Duplicate in API response 
    createdAt: Optional[dt.datetime] = None # Duplicate in API repsonse
    uploaderId: Optional[int] = None # Duplicate in API response


@dataclass
class Reminder:
    id: int
    creator: Person
    owner: Person
    completer: Optional[Person]
    type: ReminderType
    reset_type: ReminderResetType
    status: ReminderStatusType
    created_at: dt.datetime
    content: str
    due_date: dt.datetime
    completed_at: Optional[dt.datetime]
    reminder_days: int
    person: Optional[Person]
    organization: Optional[Organization]
    opportunity: Optional[Opportunity]


@dataclass
class Webhook:
    id: int
    webhook_url: str
    subscriptions: list[str]
    created_by: int
    updated_at: dt.datetime
    disabled: bool
