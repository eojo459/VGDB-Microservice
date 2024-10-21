from datetime import date, datetime
from uuid import UUID
from ninja import Schema

################
# MODEL SCHEMAS
################

class Store(Schema):
    id: UUID
    rawg_id: int
    name: str
    slug: str 
    games_count: int
    background_image: str | None = None
    domain: str