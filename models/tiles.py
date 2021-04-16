from database import Base
from sqlalchemy import Column, Integer, String, SmallInteger, Float, ForeignKey
from sqlalchemy import DateTime, func
from datetime import datetime
from sqlalchemy.orm import relationship
from models.countries import Country
from models.users import User


class Tile(Base):
    __tablename__ = "tiles"
    id = Column(String, primary_key=True)
    base_price = Column(Float, nullable=False)
    location = Column(String(150))
    available = Column(SmallInteger)
    tile_class = Column(SmallInteger)
    for_sale = Column(SmallInteger)
    date_changed = Column(DateTime, nullable=False, default=datetime.utcnow)
    country_id = Column(Integer, ForeignKey('countries.id'), nullable=False)
    country = relationship("Country", backref="tiles")
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    user = relationship("User", backref="tiles")

    def __init__(self, id, base_price, location, available, tile_class, for_sale, date_changed, country_id, user_id):
        self.id = id
        self.base_price = base_price
        self.location = location
        self.available = available
        self.tile_class = tile_class
        self.for_sale = for_sale
        self.date_changed = date_changed
        self.country_id = country_id
        self.user_id = user_id

    def __repr__(self):
        return """<Tile(base_price'{0}', location'{1}', available'{2}', tile_class'{3}',
            for_sale'{4}', date_changed'{5}', country_id'{6}', user_id'{7}'>""".format(
            self.base_price, self.location, self.available, self.tile_class, self.for_sale,
            self.date_changed, self.country_id, self.user_id)


Base.metadata.create_all()