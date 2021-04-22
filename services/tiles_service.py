from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List
from models import tiles
from schemas import tile_schema
from sqlalchemy.exc import SQLAlchemyError

def get_tiles(db: Session, quadkeys : List[str]):
    return db.query(tiles.Tile).filter(tiles.Tile.id.in_(quadkeys)).all()

def get_tiles_by_user_id(db: Session, user_id: int):
    return db.query(tiles.Tile).filter(tiles.Tile.user_id == user_id).all()

def insert_tiles(db: Session, tiles_schema: List[tile_schema.Tile]):
    for tile in tiles_schema:
        db_tile = tiles.Tile(
            id=tile.id,
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
        db.add(db_tile)
    try:
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail="Problem while adding tiles, duplicate or invalid quadkeys! or " + str(type(e)))
