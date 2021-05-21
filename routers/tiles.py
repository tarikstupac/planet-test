from os import stat
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import oauth2
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy.sql.expression import distinct

from starlette.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from database import get_db
from schemas import tile_schema
from services import tiles_service, country_service, users_service
from helpers import authentication
from routers.oauth2 import check_credentials
from redis_conf import token_watcher as r
#from redis_conf import country_watcher as cr
from helpers import quadkey_parser

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
def get_tiles_by_country(db: Session = Depends(get_db), skip:int = 0, limit: int = 100):
    result = tiles_service.get_number_of_tiles_by_country(db, skip, limit)
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

@router.post("/gettilesbyquadkeys", status_code=status.HTTP_200_OK)
def get_tiles(quadkeys: List[str], db: Session = Depends(get_db)):
    tiles_list = []
    if len(quadkeys) < 1 or quadkeys is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No quadkeys found in the request.")
    #Checking locked keys in tile38
    #creating pipeline and executing intersects with quadkeys
    # pipe = cr.pipeline(transaction=False)
    # for key in quadkeys:
    #     pipe.execute_command('INTERSECTS','countries', 'COUNT', 'QUADKEY', key)
    # tile38_objects = pipe.execute()
    #checking response list for keys in locked countries
    #by checking the count object returned by tile38
    # for i in range(0, len(quadkeys)):
    #     if tile38_objects[i] == 1:
    #         tiles_list.append({"id":quadkeys[i], "available":0})
    
    tiles = tiles_service.get_tiles(db, quadkeys=quadkeys)
    for tile in tiles:
        tile.id = quadkey_parser.quadint_to_quadkey(tile.id)
    #adding found tiles in db to the list of locked tiles
    tiles_list.extend([tiles[i] for i in range(0, len(tiles))])
    if len(tiles_list) < 1 :
        raise HTTPException(status_code=status.HTTP_200_OK, detail="No tiles with specified quadkeys found and no locked tiles found!")
    return tiles_list

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
    for tile in tiles:
            tile.id = quadkey_parser.quadint_to_quadkey(tile.id)
    return tiles

@router.get("/{user_id}/country", status_code=status.HTTP_200_OK)
def get_tiles_for_user_by_country(user_id: int, db: Session = Depends(get_db), token: str = Depends(authentication.oauth2_scheme)):
    token_data = check_credentials(token)
    user = users_service.get_by_email(db, token_data.username)
    if user is None:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail="No user exists.")
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
        for tile in tile_list:
            tile.id = quadkey_parser.quadint_to_quadkey(tile.id)
        obj = {'id': temp.id, 'name' : temp.name,"tiles" : tile_list}
        tiles_by_country.append(obj)
    if tiles_by_country is None or len(tiles_by_country) < 1 :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Can't fetch tiles by country for the given user")
    return tiles_by_country

@router.get('{user_id}/details', status_code=status.HTTP_200_OK, response_description="Successfully fetched tile details for user")
def get_tile_details_for_user(user_id:int, db: Session = Depends(get_db)):
    user = users_service.get_by_id(db, user_id)

    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No user exists for specified parameters.")
    
    distinct_countries = tiles_service.get_distinct_countries(db, user_id)
    list_of_tiles = tiles_service.get_tiles_by_user_id(db, user_id)

    obj = {"number_of_tiles":len(list_of_tiles), "number_of_countries":len(distinct_countries)}
    return obj
    
    
@router.put("/", status_code=status.HTTP_202_ACCEPTED, response_description="Successfully updated tiles.")
def edit_tiles(tiles: List[tile_schema.EditTile], db: Session = Depends(get_db), token: str = Depends(authentication.oauth2_scheme)):
    token_data = check_credentials(token)
    user = users_service.get_by_email(db, token_data.username)
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have required permissions for this action!")

    token_valid = check_token_validity(user.id, token)
    if token_valid is False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not logged in or your session has expired!")

    if len(tiles) < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="No tiles found in the request.")

    tiles = tiles_service.edit_tiles(db, tiles)





