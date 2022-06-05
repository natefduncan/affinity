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

class EntityType(Enum):
    person = 0
    organization = 1
    opportunity = 8

class InteractionType(Enum):
    meeting = 0
    call = 1
    chat_message = 2
    email = 3

class DirectionType(Enum):
    sent = 0
    received = 1

class LoggingType(Enum):
    all = 0
    manual = 1
