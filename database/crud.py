from typing import List
from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int) -> models.User:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> models.User:
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[models.User]:
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# ----------------------------------------------------------------
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
    db_restaurant = models.Restaurant(name=restaurant.name, address=restaurant.address)
    db.add(db_restaurant)
    db.commit()
    db.refresh(db_restaurant)
    return db_restaurant


# ----------------------------------------------------------------
def get_review(db: Session, review_id: int) -> models.Review:
    return db.query(models.Review).filter(models.Review.id == review_id).first()


def get_reviews(db: Session, skip: int = 0, limit: int = 100) -> List[models.Review]:
    return db.query(models.Review).offset(skip).limit(limit).all()


def get_reviews_by_restaurant(db: Session, restaurant_id: int) -> List[models.Review]:
    return (
        db.query(models.Review)
        .filter(models.Review.restaurant.id == restaurant_id)
        .first()
    )


def get_reviews_by_author(db: Session, author_id: int) -> List[models.Review]:
    return db.query(models.Review).filter(models.Review.author.id == author_id).all()


def create_review(db: Session, review: schemas.ReviewCreate) -> models.Review:
    db_review = models.Review(
        author_id=review.author_id,
        restaurant_id=review.restaurant_id,
        body=review.body,
        rating=review.rating,
        price=review.price,
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review