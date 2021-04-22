from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas import tile_schema
from services import tiles_service
import json

router = APIRouter(prefix='/tiles', tags=["Tiles"])

@router.get("/country", response_description=status.HTTP_200_OK)
def get_tiles_by_country(db: Session = Depends(get_db)):
    result = tiles_service.get_number_of_tiles_by_country(db)
    if result is None or len(result) < 1 :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Couldn't get any tiles by country.")
    return {result}

@router.post("/gettilesbyquadkeys", response_model=List[tile_schema.Tile], status_code=status.HTTP_200_OK)
def get_tiles(quadkeys: List[str], db: Session = Depends(get_db)):
    if len(quadkeys) < 1 or quadkeys is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No quadkeys found in the request.")
    tiles = tiles_service.get_tiles(db, quadkeys=quadkeys)
    if len(tiles) < 1 :
        raise HTTPException(status_code=status.HTTP_200_OK, detail="No tiles with specified quadkeys found!")
    return tiles

@router.get("/{user_id}", response_model=List[tile_schema.Tile], status_code=status.HTTP_200_OK)
def get_tiles_by_user_id(user_id: int, db: Session = Depends(get_db)):
    tiles = tiles_service.get_tiles_by_user_id(db, user_id=user_id)
    if tiles is None or len(tiles) < 1:
        raise HTTPException(status_code=status.HTTP_200_OK, detail="No tiles found for user id or user with the id doesn't exist!")
    return tiles

@router.post("/", status_code=status.HTTP_201_CREATED, response_description="Successfully added tiles!")
def insert_tiles(tiles: List[tile_schema.Tile], db: Session = Depends(get_db)):
    if tiles is None or len(tiles) < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No tiles supplied!")
    tiles_service.insert_tiles(db, tiles)