from sqlalchemy import Column, Integer, String, SmallInteger, Float, func
from sqlalchemy.orm import relationship
from database import Base

class Country(Base):
    __tablename__ = "countries"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True, index=True)
    locked = Column(SmallInteger, index=True)
    code = Column(String(10), unique=True, nullable=False)
    price_multiplier = Column(Float)

    def __init__(self, name, locked, code, price_multiplier):
        self.name = name
        self.locked = locked
        self.code = code
        self.price_multiplier = price_multiplier

    def __repr__(self):
        return "<Country(name'{0}', locked'{1}', code'{2}', price_multiplier'{3}'>".format(
            self.name, self.locked, self.code, self.price_multiplier)


Base.metadata.create_all()