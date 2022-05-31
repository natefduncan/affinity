from affinity.common.constants import ListType

# https://api-docs.affinity.co/#lists
class List: 
    def __init__(self, id: int, type: ListType, name: str, public: bool, owner_id: int, list_size: int):
        self.id = id
        self.type = type
        self.name = name
        self.public = public
        self.owner_id = owner_id
        self.list_size = list_size


