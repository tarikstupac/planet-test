from fastapi import APIRouter, Depends, status, HTTPException
from database import get_db
from schemas import user_schema
from services import users_service

router = APIRouter(prefix='/users',tags=['Users'])

@router.get("/", response_model=user_schema.User, status_code=status.HTTP_200_OK)
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = users_service.get_all(db, skip, limit)
    if users is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return users

@router.get("/{user_id}", response_model=user_schema.User, status_code=status.HTTP_200_OK)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = users_service.get_by_id(db, user_id=user_id)
    if user is None:
        raise HttpException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user