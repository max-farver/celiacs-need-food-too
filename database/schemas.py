from typing import List, Optional

from pydantic import BaseModel


class ReviewBaseModel(BaseModel):
    author_id: int
    body: str
    rating: int
    price: int
    restaurant_id: int


class ReviewCreate(ReviewBaseModel):
    pass


class Review(ReviewBaseModel):
    id: int

    class Config:
        orm_mode = True


# ------------------------------------------------------------------------
class RestaurantBase(BaseModel):
    name: str
    address: str


class RestaurantCreate(RestaurantBase):
    pass


class Restaurant(RestaurantBase):
    id: int
    avg_price: int
    reviews: List[int] = []

    class Config:
        orm_mode = True


# ------------------------------------------------------------------------
class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    reviews: List[int] = []

    class Config:
        orm_mode = True
