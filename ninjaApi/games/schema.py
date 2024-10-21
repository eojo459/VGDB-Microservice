from datetime import date, datetime
from uuid import UUID
from ninja import Schema
from typing import List
from requirements.schema import Requirement
from platforms.schema import Platform

################
# MODEL SCHEMAS
################

class Game(Schema):
    id: UUID
    rawg_id: int
    bg_image: str | None = None
    tba: bool
    name: str
    rating: float | None = None
    rating_top: float | None = None
    ratings_count: int
    reviews_count: str
    released: date
    metacritic: float | None = None
    playtime: float | None = None
    esrb_rating: str
    last_updated: datetime
    enabled: bool
    expires: datetime | None = None
    platforms: List[Platform] | None = None
    requirements: List[Requirement] | None = None
    archived: bool