"""A module containing the router and routes related to the transactions endpoint"""
from helpers.quadkey_parser import quadint_to_quadkey
from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from sqlalchemy.orm import Session
from database import get_db
from schemas import transaction_schema, tile_schema, user_schema
from services import transactions_service, users_service, transactiondetails_service
from helpers import authentication
from routers.oauth2 import check_credentials
from redis_conf import token_watcher as r


router = APIRouter(prefix='/transactions', tags=['Transactions'])

def check_token_validity(user_id: int, token:str):
    if r.exists(f'{user_id}_access_token') != 0:
        redis_token = r.get(f'{user_id}_access_token')
        if redis_token.decode('utf-8') == token:
            return True
        else:
            return False
    else:
        return False


@router.get("/", response_model=List[transaction_schema.Transaction], status_code=status.HTTP_200_OK)
def get_all_transactions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

    transactions = transactions_service.get_all_transactions(db, skip, limit)
    if transactions is None or len(transactions) < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="No transactions found!")
    return transactions


@router.get("/user/{user_id}", status_code=status.HTTP_200_OK)
def get_transactions_by_user_id(user_id: int, skip:int = 0, limit:int = 100, db: Session = Depends(get_db), token: str = Depends(authentication.oauth2_scheme)):

    token_data = check_credentials(token)
    user_exists = users_service.get_by_email(db, token_data.username)
    if user_exists is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have required permissions for this action!")
    token_valid = check_token_validity(user_exists.id, token)
    if token_valid is False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not logged in or your session has expired!")

    transactions = transactions_service.get_transactions_by_user_id(
        db, user_id, skip, limit)
    if transactions is None or len(transactions) < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Transactions are not found")
    return transactions


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=user_schema.User)
def insert_transaction(tiles: List[tile_schema.TileInsert],  db: Session = Depends(get_db), token: str = Depends(authentication.oauth2_scheme)):

    token_data = check_credentials(token)
    user_exists = users_service.get_by_email(db, token_data.username)
    if user_exists is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have required permissions for this action!")

    token_valid = check_token_validity(user_exists.id, token)
    if token_valid is False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not logged in or your session has expired!")

    if tiles is None or len(tiles) < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No tiles supplied!")
    transaction = transaction_schema.InsertTransaction()
    user = transactions_service.insert_transaction(
        db, transaction, tiles, user_exists.id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Something went wrong while saving changes in database")

    return user


@router.put("/{trans_id}", status_code=status.HTTP_202_ACCEPTED)
def update_transaction(trans_id: int, transaction: transaction_schema.EditTransaction, db: Session = Depends(get_db), token: str = Depends(authentication.oauth2_scheme)):

    token_data = check_credentials(token)
    user_exists = users_service.get_by_email(db, token_data.username)

    if user_exists is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")

    token_valid = check_token_validity(user_exists.id, token)
    if token_valid is False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not logged in or your session has expired!")

    edited_trans = transactions_service.update_transaction(
        db, transaction, trans_id)

    if edited_trans is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Something went wrong while saving changes in database")

    return edited_trans


@router.get("/{trans_id}", status_code=status.HTTP_200_OK)
def get_transaction_details(trans_id: int, db: Session = Depends(get_db), token: str = Depends(authentication.oauth2_scheme)):

    token_data = check_credentials(token)
    user_exists = users_service.get_by_email(db, token_data.username)

    if user_exists is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")

    token_valid = check_token_validity(user_exists.id, token)
    if token_valid is False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not logged in or your session has expired!")

    transactions = transactions_service.get_by_id(
        db, trans_id=trans_id)

    if transactions is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Transactions are not found")

    transaction_details = transactiondetails_service.get_transaction_details(
        db, trans_id)
    if transaction_details is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Transaction details are not found")

    for detail in transaction_details:
        detail.tile_id = quadint_to_quadkey(detail.tile_id)

    obj = {'id': transactions.id,
           'date_created': transactions.date_created,
           'status': transactions.status,
           'total_price': transactions.total_price,
           'user_id': transactions.user_id,
           'date_processed': transactions.date_processed,
           'total_tiles': transactions.total_tiles,
           'transaction_details': transaction_details}

    return obj


@router.get("/tile/{tile_id}", status_code=status.HTTP_200_OK)
def get_transaction_details_for_tile(tile_id: str, db: Session = Depends(get_db)):

    transaction_details = transactiondetails_service.get_transaction_details_for_tile(
        db, tile_id)

    if transaction_details is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Transaction details are not found")
    
    for detail in transaction_details:
        detail.tile_id = quadint_to_quadkey(detail.tile_id)

    return transaction_details


@router.get("/details/{transaction_details_id}", status_code=status.HTTP_200_OK)
def get_transaction_detail_by_id(transaction_details_id: int, db: Session = Depends(get_db)):

    transaction_detail = transactiondetails_service.get_transaction_detail_by_id(
        db, transaction_details_id)

    if transaction_detail is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Transaction details are not found")
    transaction_detail.tile_id = quadint_to_quadkey(transaction_detail.tile_id)

    return transaction_detail
