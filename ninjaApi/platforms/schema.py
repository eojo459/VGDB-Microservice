from datetime import date, datetime
from uuid import UUID
from ninja import Schema

################
# MODEL SCHEMAS
################

class Platform(Schema):
    id: UUID
    rawg_id: int
    name: str
    slug: str 