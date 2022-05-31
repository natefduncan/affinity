import datetime as dt
from affinity.common.constants import ListType

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
class Field:
    def __init__(self, id: int, name: str, list_id: int, allows_multiple: bool, dropdown_options: List[DropdownOption], value_type: int):
        self.id = id
        self.name = name
        self.list_id = list_id
        self.allows_multiple = allows_multiple
        self.dropdown_options = dropdown_options
        self.value_type = value_type
