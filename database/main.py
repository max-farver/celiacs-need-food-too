from typing import List

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)  # type: ignore

router = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------------- Users ---------------------------------
@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@router.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/users/reviews", response_model=List[schemas.Review])
def read_reviews_by_author(author_id: int, db: Session = Depends(get_db)):
    db_author_reviews = crud.get_reviews_by_author(db, author_id=author_id)
    if db_author_reviews is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return db_author_reviews


# --------------------------- Restaurants -----------------------------------
@router.post("/restaurants/", response_model=schemas.Restaurant)
def create_restaurant(
    restaurant: schemas.RestaurantCreate, db: Session = Depends(get_db)
):
    return crud.create_restaurant(db, restaurant=restaurant)


@router.get("/restaurants/", response_model=List[schemas.Restaurant])
def read_restaurants(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_restaurants(skip=skip, limit=limit, db=db)


@router.get("/restaurants/{restaurant_id}", response_model=schemas.Restaurant)
def read_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    db_restaurant = crud.get_restaurant(db, restaurant_id=restaurant_id)
    if db_restaurant is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return db_restaurant


@router.get("/restaurants/reviews", response_model=List[schemas.Review])
def read_reviews_by_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    db_restaurant_reviews = crud.get_reviews_by_restaurant(
        db, restaurant_id=restaurant_id
    )
    if db_restaurant_reviews is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return db_restaurant_reviews


# ---------------------------- Reviews -----------------------------------
@router.post("/reviews/", response_model=schemas.Review)
def create_restaurant(
    restaurant: schemas.RestaurantCreate, db: Session = Depends(get_db)
):
    return crud.create_restaurant(db, restaurant=restaurant)


@router.get("/reviews/", response_model=List[schemas.Review])
def read_reviews(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_reviews(skip=skip, limit=limit, db=db)


@router.get("/reviews/{review_id}", response_model=schemas.Review)
def read_review(review_id: int, db: Session = Depends(get_db)):
    db_review = crud.get_review(db, review_id=review_id)
    if db_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return db_review