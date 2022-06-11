from enum import IntEnum

class ListType(IntEnum):
    person = 0
    organization = 1
    opportunity = 8

class ActionType(IntEnum):
    create = 0
    delete = 1
    update = 2

class PersonType(IntEnum):
    external = 0
    internal = 1

class EntityType(IntEnum):
    person = 0
    organization = 1
    opportunity = 8

class InteractionType(IntEnum):
    meeting = 0
    call = 1
    chat_message = 2
    email = 3

class DirectionType(IntEnum):
    sent = 0
    received = 1

class LoggingType(IntEnum):
    all = 0
    manual = 1

class ValueType(IntEnum):
    person = 0
    organization = 1
    dropdown = 2
    number = 3
    date = 4
    location = 5
    text = 6
    ranked_dropdown = 7
    opportunity = 8

class ReminderType(IntEnum):
    one_time = 0
    recurring = 1

class ReminderResetType(IntEnum):
    interaction = 0
    email = 1
    meeting = 2

class ReminderStatusType(IntEnum):
    completed = 0
    active = 1
    overdue = 2
