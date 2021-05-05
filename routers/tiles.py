from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List

from starlette.status import HTTP_401_UNAUTHORIZED
from database import get_db
from schemas import tile_schema
from services import tiles_service, country_service, users_service
from helpers import authentication
from routers.oauth2 import check_credentials
from redis_conf import token_watcher as r

router = APIRouter(prefix='/tiles', tags=["Tiles"])

def check_token_validity(user_id: int, token:str):
    if r.exists(f'{user_id}_access_token') != 0:
        redis_token = r.get(f'{user_id}_access_token')
        if redis_token.decode('utf-8') == token:
            return True
        else:
            return False
    else:
        return False


@router.get("/country", response_description=status.HTTP_200_OK)
def get_tiles_by_country(db: Session = Depends(get_db)):
    result = tiles_service.get_number_of_tiles_by_country(db)
    if result is None or len(result) < 1 :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Couldn't get any tiles by country.")
    country_list = [dict(result[i]).items() for i in range(0, len(result))]
    return country_list

@router.post("/", status_code=status.HTTP_201_CREATED, response_description="Successfully added tiles!")
def insert_tiles(tiles: List[tile_schema.Tile], db: Session = Depends(get_db), token: str = Depends(authentication.oauth2_scheme)):
    token_data = check_credentials(token)
    user = users_service.get_by_email(db, token_data.username)
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have required permissions for this action!")

    token_valid = check_token_validity(user.id, token)
    if token_valid is False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not logged in or your session has expired!")

    if tiles is None or len(tiles) < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No tiles supplied!")
    tiles_service.insert_tiles(db, tiles)

@router.post("/gettilesbyquadkeys", response_model=List[tile_schema.Tile], status_code=status.HTTP_200_OK)
def get_tiles(quadkeys: List[str], db: Session = Depends(get_db)):
    if len(quadkeys) < 1 or quadkeys is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No quadkeys found in the request.")
    tiles = tiles_service.get_tiles(db, quadkeys=quadkeys)
    if len(tiles) < 1 :
        raise HTTPException(status_code=status.HTTP_200_OK, detail="No tiles with specified quadkeys found!")
    return tiles

@router.get("/{user_id}", response_model=List[tile_schema.Tile], status_code=status.HTTP_200_OK)
def get_tiles_by_user_id(user_id: int, db: Session = Depends(get_db), token: str = Depends(authentication.oauth2_scheme)):
    token_data = check_credentials(token)
    user = users_service.get_by_email(db, token_data.username)

    token_valid = check_token_validity(user.id, token)
    if token_valid is False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not logged in or your session has expired!")

    if user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have required permissions for this action!")
    
    tiles = tiles_service.get_tiles_by_user_id(db, user_id=user_id)
    if tiles is None or len(tiles) < 1:
        raise HTTPException(status_code=status.HTTP_200_OK, detail="No tiles found for user id or user with the id doesn't exist!")
    return tiles

@router.get("/{user_id}/country", status_code=status.HTTP_200_OK)
def get_tiles_for_user_by_country(user_id: int, db: Session = Depends(get_db), token: str = Depends(authentication.oauth2_scheme)):
    token_data = check_credentials(token)
    user = users_service.get_by_email(db, token_data.username)

    token_valid = check_token_validity(user.id, token)
    if token_valid is False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not logged in or your session has expired!")


    if user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have required permissions for this action!")
    
    tiles_by_country = []
    distinct_countries = tiles_service.get_distinct_countries(db, user_id=user_id)
    if distinct_countries is None or len(distinct_countries) < 1:
         raise HTTPException(status_code=status.HTTP_200_OK, detail="No tiles found for user id or user with the id doesn't exist!")
    for country in distinct_countries:
        temp = country_service.get_by_id(db, country['country_id'])
        tile_list = tiles_service.get_tiles_by_user_country(db, user_id, temp.id)
        obj = {'id': temp.id, 'name' : temp.name,"tiles" : tile_list}
        tiles_by_country.append(obj)
    if tiles_by_country is None or len(tiles_by_country) < 1 :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Can't fetch tiles by country for the given user")
    return tiles_by_country
    




