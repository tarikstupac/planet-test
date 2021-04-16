from database import Base
from sqlalchemy import Column, Integer, ForeignKey, Float, String
from sqlalchemy import DateTime, func
from sqlalchemy.orm import relationship
from models.transactions import Transaction
from models.tiles import Tile


class TransactionDetail(Base):
    __tablename__ = "transaction_details"
    id = Column(Integer, primary_key=True)
    unit_price = Column(Float)
    transaction_id = Column(Integer, ForeignKey('transactions.id'), nullable=False)
    transaction = relationship("Transaction", backref="transaction_details")
    tile_id = Column(String, ForeignKey('tiles.id'), nullable=False)
    tile = relationship("Tile", backref="transaction_details")

    def __init__(self, unit_price, transaction_id, tile_id):
        self.unit_price = unit_price
        self.transaction_id = transaction_id
        self.tile_id = tile_id

    def __repr__(self):
        return """<TransactionDetail(unit_price'{0}', transaction_id'{1}', tile_id'{2}'>""".format(
            self.unit_price, self.transaction_id, self.tile_id)


Base.metadata.create_all()