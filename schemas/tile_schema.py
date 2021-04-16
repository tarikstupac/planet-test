from typing import Optional
from pydantic import BaseModel, constr, PositiveFloat
from datetime import datetime

from schemas.country_schema import Country
from schemas.user_schema import User


class Tile(BaseModel):
    id : constr(min_length=21, max_length=21)
    base_price : PositiveFloat
    location : constr(min_length=1, max_length=150) 
    available : int
    tile_class : int
    for_sale : int
    date_changed : Optional[datetime]
    country_id : int
    user_id : int
    

    class Config:
        orm_mode = True