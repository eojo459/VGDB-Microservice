from uuid import UUID
from ninja import Schema

################
# MODEL SCHEMAS
################
class Genre(Schema):
    tmdb_id: int
    name: str
    type: int

class GenreOut(Schema):
    id: UUID
    tmdb_id: int
    name: str
    type: int