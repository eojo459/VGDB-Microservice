from datetime import date, datetime
from enum import Enum
from uuid import UUID
from ninja import Schema

################
# MODEL SCHEMAS
################

class RequirementType(Enum):
    MINIMUM = 0
    RECOMMENDED = 1
    UNKNOWN = 2

class Requirement(Schema):
    id: UUID
    type: int # minimum or recommended
    name: str
    description: str