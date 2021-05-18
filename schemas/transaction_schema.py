"""A module containing all the pydantic schemas for Transaction SQLAlchemy model"""
from typing import Optional
from pydantic import BaseModel, constr, PositiveFloat, PositiveInt
from datetime import datetime


class Transaction(BaseModel):
    """A base pydantic schema for the SQLAlchemy transaction model

    :param BaseModel: A pydantic base model that this class has to inherit from
    :type BaseModel: BaseModel
    """
    id: int
    date_created: Optional[datetime]
    date_processed: Optional[datetime]
    status: int
    total_price: PositiveFloat
    total_tiles: PositiveInt
    user_id: int

    class Config:
        orm_mode = True


class InsertTransaction(BaseModel):
    date_created: Optional[datetime] = datetime.utcnow()
    date_processed: Optional[datetime] = datetime.utcnow()
    status: int = 0
    total_price: int = 0
    total_tiles: int = 0

    class Config:
        orm_mode = True


class EditTransaction(BaseModel):
    date_processed: Optional[datetime] = datetime.utcnow()
    status: Optional[int]
    total_price: Optional[int]
    total_tiles: Optional[int]

    class Config:
        orm_mode = True
