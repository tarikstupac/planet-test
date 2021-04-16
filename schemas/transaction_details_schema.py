from typing import Optional
from pydantic import BaseModel, constr, PositiveFloat, PositiveInt
from datetime import datetime

from schemas.tile_schema import Tile


class TransactionDetail(BaseModel):
    id : int
    unit_price : PositiveFloat
    transaction_id : int
    tile_id : int
    tile : Tile

    class Config:
        orm_mode = True