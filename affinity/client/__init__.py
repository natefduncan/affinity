from affinity.core.models import *
from affinity.client.endpoints import Lists, ListEntries, Fields, Notes, Persons, Organizations, Interactions, FieldValues, Opportunities, RelationshipsStrengths, Notes, EntityFiles, Reminders, Webhooks, WhoAmI, FieldValueChanges
from affinity.common.constants import InteractionType

class Client:
    def __init__(self, token: str):
        self.token = token
        
    def lists(self):
        return Lists(self.token)

    def list_entries(self, list_id: int):
        return ListEntries(token=self.token, list_id=list_id)

    def fields(self):
        return Fields(self.token)

    def persons(self):
        return Persons(self.token)

    def organizations(self):
        return Organizations(self.token)

    def opportunities(self):
        return Opportunities(self.token)

    def interactions(self, type: InteractionType):
        return Interactions(self.token, type)

    def field_values(self):
        return FieldValues(self.token)

    def relationships_strengths(self):
        return RelationshipsStrengths(self.token)

    def notes(self):
        return Notes(self.token)

    def entity_files(self):
        return EntityFiles(self.token)

    def reminders(self):
        return Reminders(self.token)

    def whoami(self):
        return WhoAmI(self.token)

    def field_value_changes(self):
        return FieldValueChanges(self.token)

    def webhooks(self):
        return Webhooks(self.token)
