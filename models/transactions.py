from database import Base
from sqlalchemy import Column, Integer, String, SmallInteger, ForeignKey, Float
from sqlalchemy import DateTime, func
from datetime import datetime
from sqlalchemy.orm import relationship
from models.users import User


class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True)
    date_created = Column(DateTime, nullable=False, default=datetime.utcnow)
    date_processed = Column(DateTime, nullable=False)
    status = Column(SmallInteger, nullable=False)
    total_price = Column(Float, nullable=False)
    total_tiles = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    user = relationship("User", backref="transactions")

    def __init__(self, date_created, date_processed, status, total_price, total_tiles, user_id):
        self.date_created = date_created
        self.date_processed = date_processed
        self.status = status
        self.total_price = total_price
        self.total_tiles = total_tiles
        self.user_id = user_id
    
    def __repr__(self):
        return """<Transaction(date_created'{0}', date_processed'{1}', status'{2}', total_price'{3}',
            total_tiles'{4}', user_id'{5}'>""".format(
            self.date_created, self.date_processed, self.status, self.total_price, self.total_tiles,
            self.user_id)


Base.metadata.create_all()
