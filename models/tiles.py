from database import Base
from sqlalchemy import Column, Integer, String, SmallInteger, Float, ForeignKey, Numeric
from sqlalchemy import DateTime, func
from datetime import datetime
from sqlalchemy.orm import relationship
from models.countries import Country
from models.users import User


class Tile(Base):
    __tablename__ = "tiles"
    id = Column(Numeric(20,0), primary_key=True)
    base_price = Column(Float, nullable=False)
    location = Column(String(150))
    available = Column(SmallInteger)
    tile_class = Column(SmallInteger)
    for_sale = Column(SmallInteger)
    user_flag = Column(String(10), nullable=True)
    date_changed = Column(DateTime, nullable=False, default=datetime.utcnow)
    country_id = Column(String, ForeignKey('countries.id'), nullable=False)
    country = relationship("Country", backref="tiles")
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    user = relationship("User", backref="tiles")

    def __init__(self, id, base_price, location, available, tile_class, for_sale, user_flag, date_changed, country_id, user_id):
        self.id = id
        self.base_price = base_price
        self.location = location
        self.available = available
        self.tile_class = tile_class
        self.for_sale = for_sale
        self.user_flag = user_flag
        self.date_changed = date_changed
        self.country_id = country_id
        self.user_id = user_id

    def __repr__(self):
        return """<Tile(base_price'{0}', location'{1}', available'{2}', tile_class'{3}',
            for_sale'{4}', user_flag'{5}', date_changed'{6}', country_id'{7}', user_id'{8}'>""".format(
            self.base_price, self.location, self.available, self.tile_class, self.for_sale,
            self.user_flag, self.date_changed, self.country_id, self.user_id)
