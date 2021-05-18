from typing import Optional, List
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
    user_flag : Optional[str]
    date_changed : Optional[datetime]
    country_id : str
    user_id : int
    

    class Config:
        orm_mode = True


class TileByCountry(BaseModel):
    id: str
    name: str
    tiles: List

class EditTile(BaseModel):
    """A base pydantic model for tile that reflects the SQLAlchemy model.

    :param BaseModel: Pydantic base model that this class has to inherit from
    :type BaseModel: BaseModel
    """
    id: constr(min_length=21, max_length=21)
    base_price: Optional[PositiveFloat]
    available: Optional[int]
    tile_class: Optional[int]
    for_sale: Optional[int]
    user_flag: Optional[str]
    date_changed: Optional[datetime] = datetime.utcnow()
    user_id: Optional[int]

    class Config:
        orm_mode = True