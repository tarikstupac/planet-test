from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List
from models import tiles
from schemas import tile_schema

def get_tiles(db: Session, quadkeys : List[str]):
    return db.query(tiles.Tile).filter(tiles.Tile.id.in_(quadkeys)).all()

def get_tiles_by_user_id(db: Session, user_id: int):
    return db.query(tiles.Tile).filter(tiles.Tile.user_id == user_id).all()

def insert_tiles(db: Session, tiles: List[tile_schema.Tile]):
    for tile in tiles:
        db.add(tile)
    try:
        db.commit()
    except:
        db.rollback()
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail="Problem while adding tiles, duplicate or invalid quadkeys!")
