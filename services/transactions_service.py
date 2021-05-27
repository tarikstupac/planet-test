"""A module that contains all the calls to the database related to the Transactions table"""
from models.transactions import Transaction
from sqlalchemy import desc
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List
from models import transactions, tiles, transaction_details
from schemas import transaction_schema, tile_schema
from services import country_service, users_service
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from helpers import quadkey_parser

def insert_transaction(db: Session, transaction: transaction_schema.InsertTransaction, tiles_schema: List[tile_schema.TileInsert], userid: int):

    db_tiles = []
    db_transaction_details = []
    totalprice = 0

    if tiles_schema is None or len(tiles_schema) < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Something went wrong with tiles")

    db_transaction = transactions.Transaction(
        date_created=transaction.date_created,
        date_processed=transaction.date_processed,
        status=transaction.status,
        total_price=transaction.total_price,
        total_tiles=transaction.total_tiles,
        user_id=userid
    )
    if db_transaction is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Something went wrong with transaction")

    for tile in tiles_schema:
        if tile.country_id is None or tile.country_id == '' or tile.country_id == 'SEA':
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='You can only buy tiles on land!')

        db_tile = tiles.Tile(
            id=quadkey_parser.quadkey_to_quadint(tile.id),
            base_price=tile.base_price,
            location=tile.location,
            available=tile.available,
            tile_class=tile.tile_class,
            for_sale=tile.for_sale,
            user_flag=tile.user_flag,
            date_changed=tile.date_changed,
            country_id=tile.country_id,
            user_id=tile.user_id
        )
        db_tiles.append(db_tile)

        country = country_service.get_by_id(db, tile.country_id)
        unitprice = tile.base_price * country.price_multiplier
        db_transaction_detail = transaction_details.TransactionDetail(
            unit_price=unitprice,
            transaction_id=db_transaction.id,
            tile_id=quadkey_parser.quadkey_to_quadint(tile.id)
        )
        db_transaction_details.append(db_transaction_detail)

        if db_transaction_details is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Something went wrong with transaction details")

        totalprice += unitprice

    totaltiles = len(db_tiles)

    new_trans_data = {
        "date_processed": datetime.utcnow(),
        "status": 1,
        "total_price": totalprice,
        "total_tiles": totaltiles
    }

    db_user = users_service.get_by_id(db, db_transaction.user_id)
    if db_user.credit < totalprice:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="There is not enough credits for transaction")

    try:
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)
        for db_transaction_detail in db_transaction_details:
            db_transaction_detail.transaction_id = db_transaction.id
        db.bulk_save_objects(db_tiles)
        db.bulk_save_objects(db_transaction_details)
        update_transaction(db, new_trans_data, db_transaction.id)
        db_user.credit -= totalprice
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    except SQLAlchemyError as e:
        db.rollback()
        delete_transaction(db, db_transaction.id)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Transaction failed : " + str(type(e)))


def get_by_id(db: Session, trans_id: int):

    return db.query(transactions.Transaction).filter(transactions.Transaction.id == trans_id).first()


def update_transaction(db: Session, transaction: transaction_schema.EditTransaction, trans_id: int):

    db_transaction = get_by_id(db, trans_id)

    if db_transaction is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Transaction not found")
    if(type(transaction) != dict):
        update_data = transaction.dict(exclude_unset=True)
    else:
        update_data = transaction
    for key, value in update_data.items():
        setattr(db_transaction, key, value)

    try:
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)
        return db_transaction
    except SQLAlchemyError as e:
        db.rollback()
        return None


def get_transactions_by_user_id(db: Session, user_id: int, skip: int, limit: int):

    return db.query(transactions.Transaction).filter(transactions.Transaction.user_id == user_id).order_by(desc(transactions.Transaction.id)).offset(skip).limit(limit).all()


def get_all_transactions(db: Session, skip: int = 0, limit: int = 100):

    return db.query(transactions.Transaction).order_by(desc(Transaction.date_created)).offset(skip).limit(limit).all()


def delete_transaction(db: Session, trans_id: int):

    try:
        db.query(transactions.Transaction).filter(transactions.Transaction.id == trans_id).delete()
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        return None
    
