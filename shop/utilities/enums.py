from enum import Enum

class Status(Enum):
    CREATED = 1
    PENDING = 2
    COMPLETED = 3

class Role(Enum):
    Owner = 1
    Customer = 2
    Courier = 3