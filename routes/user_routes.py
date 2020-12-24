from dependencies import get_db
from typing import List

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from database import schemas
from database.repositories import user_repository, review_repository

router = APIRouter()


@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = user_repository.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_repository.create_user(db=db, user=user)


@router.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = user_repository.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_repository.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/users/reviews", response_model=List[schemas.Review])
def read_reviews_by_author(author_id: int, db: Session = Depends(get_db)):
    db_author_reviews = review_repository.get_reviews_by_author(db, author_id=author_id)
    if db_author_reviews is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return db_author_reviews