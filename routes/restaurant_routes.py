from dependencies import get_db
from typing import List

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from database import models, schemas
from database.repositories import restaurant_repository, review_repository

router = APIRouter()


@router.post("/restaurants/", response_model=schemas.Restaurant)
def create_restaurant(
    restaurant: schemas.RestaurantCreate, db: Session = Depends(get_db)
):
    return restaurant_repository.create_restaurant(db, restaurant=restaurant)


@router.get("/restaurants/", response_model=List[schemas.Restaurant])
def read_restaurants(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return restaurant_repository.get_restaurants(skip=skip, limit=limit, db=db)


@router.get("/restaurants/{restaurant_id}", response_model=schemas.Restaurant)
def read_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    db_restaurant = restaurant_repository.get_restaurant(
        db, restaurant_id=restaurant_id
    )
    if db_restaurant is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return db_restaurant


@router.get("/restaurants/reviews", response_model=List[schemas.Review])
def read_reviews_by_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    db_restaurant_reviews = review_repository.get_reviews_by_restaurant(
        db, restaurant_id=restaurant_id
    )
    if db_restaurant_reviews is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return db_restaurant_reviews