from typing import List
from sqlalchemy.orm import Session

from database import models, schemas


def get_restaurant(db: Session, restaurant_id: int) -> models.Restaurant:
    return (
        db.query(models.Restaurant)
        .filter(models.Restaurant.id == restaurant_id)
        .first()
    )


def get_restaurants(
    db: Session, skip: int = 0, limit: int = 100
) -> List[models.Restaurant]:
    return db.query(models.Restaurant).offset(skip).limit(limit).all()


def get_restaurants_by_name(db: Session, name: str) -> List[models.Restaurant]:
    return db.query(models.Restaurant).filter(models.Restaurant.name.like(name)).all()


def create_restaurant(
    db: Session, restaurant: schemas.RestaurantCreate
) -> models.Restaurant:
    db_restaurant = models.Restaurant(
        name=restaurant.name,
        address=restaurant.address,
    )
    db.add(db_restaurant)
    db.commit()
    db.refresh(db_restaurant)
    return db_restaurant