from typing import List
from sqlalchemy.orm import Session

from database import models, schemas


def get_review(db: Session, review_id: int) -> models.Review:
    return db.query(models.Review).filter(models.Review.id == review_id).first()


def get_reviews(db: Session, skip: int = 0, limit: int = 100) -> List[models.Review]:
    return db.query(models.Review).offset(skip).limit(limit).all()


def get_reviews_by_restaurant(db: Session, restaurant_id: int) -> List[models.Review]:
    return (
        db.query(models.Review)
        .filter(models.Review.restaurant_id == restaurant_id)
        .first()
    )


def get_reviews_by_author(db: Session, author_id: int) -> List[models.Review]:
    return db.query(models.Review).filter(models.Review.author_id == author_id).all()


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