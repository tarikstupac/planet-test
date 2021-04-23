from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from sqlalchemy.orm import Session
from database import get_db
from schemas import country_schema
from services import country_service

router = APIRouter(prefix='/countries',tags=['Countries'])


@router.get("/", response_model=List[country_schema.Country], status_code=status.HTTP_200_OK)
def get_countries(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    countries = country_service.get_all(db, skip, limit)
    if countries is None or len(countries) < 1:
        raise HTTPException(status_code=status.HTTP_200_OK, detail="No countries found!")
    return countries

@router.get("/{country_id}", response_model=country_schema.Country, status_code=status.HTTP_200_OK)
def get_country_by_id(country_id: str, db: Session = Depends(get_db)):
    country = country_service.get_by_id(db, country_id==country_id)
    if country is None:
        raise HttpException(status_code=status.HTTP_200_OK, detail="Country not found")
    return country