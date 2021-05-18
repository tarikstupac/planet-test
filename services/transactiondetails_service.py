"""A module that contains all the calls to the database related to the Transaction details table"""
from sqlalchemy.orm import Session
from models import transaction_details
from helpers import quadkey_parser


def get_transaction_details(db: Session, trans_id):

    return db.query(transaction_details.TransactionDetail).filter(transaction_details.TransactionDetail.transaction_id == trans_id).all()


def get_transaction_details_for_tile(db: Session, tile_id):
    
    parsed_id = quadkey_parser.quadkey_to_quadint(tile_id)
    return db.query(transaction_details.TransactionDetail).filter(transaction_details.TransactionDetail.tile_id == parsed_id).all()


def get_transaction_detail_by_id(db: Session, transaction_details_id):

    return db.query(transaction_details.TransactionDetail).filter(transaction_details.TransactionDetail.id == transaction_details_id).first()
