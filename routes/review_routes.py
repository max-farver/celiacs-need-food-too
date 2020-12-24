from dependencies import get_db
from typing import List

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from database import schemas
from database.repositories import review_repository

router = APIRouter()


@router.post("/reviews/", response_model=schemas.Review)
def create_restaurant(review: schemas.ReviewCreate, db: Session = Depends(get_db)):
    return review_repository.create_review(db, review=review)


@router.get("/reviews/", response_model=List[schemas.Review])
def read_reviews(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return review_repository.get_reviews(skip=skip, limit=limit, db=db)


@router.get("/reviews/{review_id}", response_model=schemas.Review)
def read_review(review_id: int, db: Session = Depends(get_db)):
    db_review = review_repository.get_review(db, review_id=review_id)
    if db_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return db_review