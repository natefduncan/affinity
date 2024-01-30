> ## Note: This is a fork of Nathan Duncan's `affinity` library. Since the original library is no longer maintained, I've forked it and added some additional functionality to the library as well as fixing some bugs. Use at your own risk.

# Affinity
Python library for Affinity CRM REST API v1.0
> Note: Affinity is working on a new version of their API. This library is for the current version of the API (v1.0). It may be obsolete once the new version of the API is released.

## Installation
`pip install git+https://github.com/oneryalcin/affinity.git@main`

## Usage
```python
import affinity

client = affinity.Client(AFFINITY_TOKEN)
client.persons().list()
```

## Endpoints
- [x] [Lists](https://api-docs.affinity.co/#lists)
- [x] [List Entries](https://api-docs.affinity.co/#list-entries)
- [x] [Fields](https://api-docs.affinity.co/#fields)
- [x] [Field Values](https://api-docs.affinity.co/#field-values)
- [x] [Field Value Changes](https://api-docs.affinity.co/#field-value-changes)
- [x] [Persons](https://api-docs.affinity.co/#persons)
- [x] [Organizations](https://api-docs.affinity.co/#organizations) 
- [x] [Opportunities](https://api-docs.affinity.co/#opportunities)
- [ ] [Interactions](https://api-docs.affinity.co/#interactions) 
- [x] [Relationship Strengths](https://api-docs.affinity.co/#relationship-strengths)
- [x] [Notes](https://api-docs.affinity.co/#notes)
- [x] [Entity Files](https://api-docs.affinity.co/#entity-files)
- [x] [Reminders](https://api-docs.affinity.co/#reminders)
- [x] [Webhooks](https://api-docs.affinity.co/#webhooks)
- [x] [Whoami](https://api-docs.affinity.co/#whoami)

## Methods
```python
# Lists
client.lists().list()
client.lists().get(list_id: int)

# List Entries
client.list_entries(list_id: int).list(page_size: Optional[int] = None, page_token: Optional[str] = None)
client.list_entries(list_id: int).get(list_entry_id: int)
client.list_entries(list_id: int).create(entity_id: int, creator_id: Optional[int] = False)
client.list_entries(list_id: int).delete(list_entry_id: int)

# Fields
client.fields().list(list_id: Optional[int] = None, value_type: Optional[int] = None, with_modified_names: Optional[bool] = False)
client.fields().create(name: str, entity_type: EntityType, value_type: ValueType, list_id: Optional[int] = None, allows_multiple: Optional[bool] = None, is_list_specific: Optional[bool] = None, is_required : Optional[bool] = None)
client.fields().delete(field_id: int)

# Field Value
client.field_values().list(person_id: Optional[int] = None, organization_id: Optional[int] = None, opportunity_id: Optional[int] = None, list_entry_id: Optional[int] = None)
client.field_values().create(field_id: int, entity_id: int, value: models.Value, list_entry_id: Optional[int] = None)
client.field_values().update(field_value_id: int, value: models.Value)
client.field_values().delete(field_value_id: int)

# Persons
client.persons().list(term: Optional[str] = None, with_interaction_dates: Optional[bool] = None, with_current_organizations: Optional[bool] = None, with_opportunities: Optional[bool] = None, page_size: Optional[int] = None, page_token: Optional[str] = None)
client.persons().get(person_id: int, with_interaction_dates: Optional[bool] = None, with_interaction_persons: Optional[bool] = None, with_opportunities: Optional[bool] = None, with_current_organizations: bool = None)
client.persons().create(first_name: str, last_name: str, emails: List[str], organization_ids: List[int] = [])
client.persons().update(person_id: int, first_name: Optional[str] = None, last_name: Optional[str] = None, emails: List[str] = [], organization_ids: List[int] = [])
client.persons().delete(person_id: int)

# Organizations
client.organizations().fields()
client.organizations().list(term: Optional[str] = None, with_interaction_dates: Optional[bool] = None, with_interaction_persons: Optional[bool] = None, with_opportunities: Optional[bool] = None, page_size: Optional[int] = None, page_token: Optional[str] = None)
client.organizations().get(organization_id: int, with_interaction_dates: Optional[bool] = None, with_interaction_persons: Optional[bool] = None, with_opportunities: Optional[bool] = None)
client.organizations().get_by_domain(domain: str, with_interaction_dates: Optional[bool] = None, with_interaction_persons: Optional[bool] = None, with_opportunities: Optional[bool] = None)
client.organizations().create(name: str, domain: Optional[str] = None, person_ids: List[int] = [])
client.organizations().update(organization_id: int, name: Optional[str] = None, domain: Optional[str] = None, person_ids: List[int] = [])
client.organizations().delete(organization_id: int)

# Opportunities
client.opportunities().list(term: Optional[str] = None, page_size: Optional[int] = None, page_token: Optional[str] = None)
client.opportunities().get(opportunity_id: int)
client.opportunities().create(name: str, list_id: int, person_ids: List[int] = [], organization_ids: List[int] = [])
client.opportunities().update(opportunity_id: int, name: Optional[str], person_ids: List[int] = [], organization_ids: List[int] = [])
client.opportunities().delete(opportunity_id: int)

# Relationship Strength
client.relationships_strengths().list(external_id: int, internal_id: Optional[int] = None)

# Notes
client.notes().list(person_id: Optional[int] = None, organization_id: Optional[int] = None, opportunity_id: Optional[int] = None, creator_id: Optional[int] = None)
client.notes().get(note_id: int)
client.notes().create(person_ids: List[int] = [], organization_ids: List[int] = [], opportunity_ids: List[int] = [], content: Optional[str] = None, gmail_id: Optional[str] = None, creator_id: Optional[int] = None, created_at: Optional[dt.datetime] = None)
client.notes().update(note_id: int, content: str)
client.notes().delete(note_id: int)

# Entity Files
client.entity_files().list(opportunity_id: Optional[int] = None, person_id: Optional[int] = None, organization_id: Optional[int] = None, page_size: Optional[int] = None, page_token: Optional[str] = None)
client.entity_files().get(entity_file_id: int)
client.entity_files().download(entity_file_id: int, save_path: str)
client.entity_files().upload(files: Dict[str, io.IOBase], person_id: Optional[int] = None, organization_id: Optional[int] = None, opportunity_id : Optional[int] = None)

# Reminders
client.reminders().list(person_id: Optional[int] = None, organization_id: Optional[int] = None, opportunity_id: Optional[int] = None, creator_id: Optional[int] = None, owner_id: Optional[int] = None, completer_id: Optional[int] = None, type: Optional[int] = None, reset_type: Optional[int] = None, status: Optional[int] = None, due_before: Optional[str] = None, due_after: Optional[str] = None, page_size: Optional[int] = False, page_token: Optional[str] = None)
client.reminders().get(reminder_id: int)
client.reminders().create(owner_id: int, type: ReminderType, content: Optional[str] = None, reset_type: Optional[ReminderResetType] = None, person_id: Optional[int] = None, organization_id: Optional[int] = None, opportunity_id: Optional[int] = False, due_date : Optional[str] = None, reminder_days: Optional[int] = None, is_completed: Optional[int] = None)
client.reminders().update(reminder_id: int, owner_id: Optional[int] = None, type: Optional[ReminderType] = None, content: Optional[str] = None, reset_type: Optional[ReminderResetType] = None, person_id: Optional[int] = None, organization_id: Optional[int] = None, opportunity_id: Optional[int] = False, due_date : Optional[str] = None, reminder_days: Optional[int] = None, is_completed: Optional[int] = None)
client.reminders().delete(reminder_id: int)

# Who Am I
client.whoami().get()

# Webhooks
client.webhooks().list()
client.webhooks().get(webhook_subscription_id: int)
client.webhooks().create(webhook_url: str, subscriptions: List[str] = [])
client.webhooks().update(webhook_subscription_id: int, webhook_url: Optional[str] = None, subscriptions: List[str] = [], disabled: Optional[bool] = None)
client.webhooks().delete(webhook_subscription_id: int)
```
