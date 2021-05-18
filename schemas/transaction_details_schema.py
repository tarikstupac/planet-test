"""A module containing all pydantic schemas related to transaction details model
of SQLAlchemy."""
from typing import Optional
from pydantic import BaseModel, constr, PositiveFloat, PositiveInt
from datetime import datetime

from schemas.tile_schema import Tile


class TransactionDetail(BaseModel):
    """A pydantic schema for the base TransactionDetail model

    :param BaseModel: Base pydantic model that this class has to inherit from
    :type BaseModel: BaseModel
    """
    id: int
    unit_price: PositiveFloat
    transaction_id: int
    tile_id: str
    tile: Tile

    class Config:
        orm_mode = True


class InsertTransactionDetails(BaseModel):
    """A pydantic schema for the base TransactionDetail model

    :param BaseModel: Base pydantic model that this class has to inherit from
    :type BaseModel: BaseModel
    """
    id: int
    unit_price: PositiveFloat
    transaction_id: int
    tile_id: str
    tile: Tile

    class Config:
        orm_mode = True
