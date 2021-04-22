from sqlalchemy import Column, Integer, String, SmallInteger, Float, func
from sqlalchemy.orm import relationship
from database import Base

class Country(Base):
    __tablename__ = "countries"
    id = Column(String(2), primary_key=True)
    name = Column(String(50), nullable=False, unique=True, index=True)
    locked = Column(SmallInteger, index=True)
    price_multiplier = Column(Float)

    def __init__(self, id, name, locked, price_multiplier):
        self.id = id
        self.name = name
        self.locked = locked
        self.price_multiplier = price_multiplier

    def __repr__(self):
        return "<Country(id'{0}', name'{1}', locked'{2}', price_multiplier'{3}'>".format(
            self.id, self.name, self.locked, self.price_multiplier)
