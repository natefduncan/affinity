from enum import Enum

class ListType(Enum):
    person = 0
    organization = 1
    opportunity = 8

class ActionType(Enum):
    create = 0
    delete = 1
    update = 2

class PersonType(Enum):
    external = 0
    internal = 1
    
