from sqlalchemy import func, distinct, join
from sqlalchemy.sql import label
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List
from models import tiles, countries
from schemas import tile_schema
from sqlalchemy.exc import SQLAlchemyError
from helpers import quadkey_parser

def get_tiles(db: Session, quadkeys : List[str]):
    quadints = [quadkey_parser.quadkey_to_quadint(quadkeys[i]) for i in range(len(quadkeys))]
    return db.query(tiles.Tile).filter(tiles.Tile.id.in_(quadints)).all()

def get_tiles_by_user_id(db: Session, user_id: int):
    return db.query(tiles.Tile).filter(tiles.Tile.user_id == user_id).all()

def get_number_of_tiles_by_country(db: Session, skip:int = 0, limit:int = 100):
    result = db.query(tiles.Tile.country_id, countries.Country.name, label('number_of_tiles', func.count(tiles.Tile.id))).\
        join(countries.Country).group_by(tiles.Tile.country_id, countries.Country.name).order_by(func.count(tiles.Tile.id).desc()).offset(skip).limit(limit).all()
    return result

def insert_tiles(db: Session, tiles_schema: List[tile_schema.TileInsert]):
    db_tiles = []
    for tile in tiles_schema:
        db_tile = tiles.Tile(
            id= quadkey_parser.quadkey_to_quadint(tile.id),
            base_price=tile.base_price,
            location=tile.location,
            available=tile.available,
            tile_class=tile.tile_class,
            for_sale=tile.for_sale,
            user_flag= tile.user_flag,
            date_changed=tile.date_changed,
            country_id=tile.country_id,
            user_id=tile.user_id
        )
        #db.add(db_tile)
        db_tiles.append(db_tile)
    try:
        db.bulk_save_objects(db_tiles)
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail="Problem while adding tiles, duplicate or invalid quadkeys! or " + str(type(e)))

def update_tile_flag(db: Session, user_flag:str, user_id: int):
    db_tiles = get_tiles_by_user_id(db, user_id)
    if len(db_tiles) < 1 :
        return
    if db_tiles[0].user_flag == user_flag:
        return

    for tile in db_tiles:
        tile.user_flag = user_flag
    try:
        db.bulk_save_objects(db_tiles)
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail="Problem while editing tile flags, " + str(type(e)))

def get_distinct_countries(db: Session, user_id: int):
    return db.query(tiles.Tile.country_id).distinct().filter(tiles.Tile.user_id==user_id).all()

def get_tiles_by_user_country(db: Session, user_id: int, country_id: str):
    return db.query(tiles.Tile).filter(tiles.Tile.user_id == user_id, tiles.Tile.country_id == country_id).all()

def get_tile_by_id(db: Session, id: str):
    """A function that queries the Tile table for tile matching the tile id (quadkey).

    This function queries the Tile table in the database and returns the tile
    with the id matching the one passed as an argument.

    :param db: SQLAlchemy database session object
    :type db: Session
    :param id: Id of the tile that will be used to query the Tiles table
    :type id: int
    :return: Tile model matching the id passed as an argument
    """
    parsed_id = quadkey_parser.quadkey_to_quadint(id)
    return db.query(tiles.Tile).filter(tiles.Tile.id == parsed_id).first()

def edit_tiles(db: Session, tiles: List[tile_schema.EditTile]):
    """A function that edits a list of tiles in the database

    This function edits a list of tile objects in the database. This function
    uses SQLAlchemy bulk_save_objects call to do bulk insert query.

    :param db: SQLAlchemy database session
    :type db: Session
    :param tiles_schema: A list of pydantic schema Tile objects to
    be updated in the database
    :type tiles_schema: List[tile_schema.Tile]
    :raises HTTPException: Error 400, this exception is raised during editing
    if there is something wrong
    :return: Returns a boolean value of True to indicate that the tiles were successfully
    updated
    :rtype: bool
    """
    db_tiles = []
    for tile in tiles:
        db_tile = get_tile_by_id(db, tile.id)
        update_data = tile.dict(exclude_unset=True)
        for key, value in update_data.items():
            if(value != db_tile.id):
                setattr(db_tile, key, value)
        db_tiles.append(db_tile)
    try:
        db.bulk_save_objects(db_tiles)
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Problem while updating tiles! or " + str(type(e)))