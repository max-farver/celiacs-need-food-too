from sqlalchemy.orm import column_property
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, func, select
from sqlalchemy.orm import relationship
from sqlalchemy.util.langhelpers import hybridproperty
from sqlalchemy_utils import aggregated

from statistics import mean
import enum

from .database import Base


# class RatingScore(enum.Enum):
#     one = 1
#     two = 2
#     three = 3
#     four = 4
#     five = 5


# class PriceLevel(enum.Enum):
#     cheap = 1
#     average = 2
#     expensive = 3


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    reviews = relationship("Review", back_populates="author")


class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    address = Column(String, index=True)

    reviews = relationship("Review", back_populates="restaurant")

    @hybridproperty
    def avg_rating(self):
        return mean(review.rating for review in self.reviews) if self.reviews else 0

    @hybridproperty
    def avg_price(self):
        return mean(review.price for review in self.reviews) if self.reviews else 0


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey("users.id"))
    author = relationship("User", back_populates="reviews")
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    restaurant = relationship("Restaurant", back_populates="reviews")
    rating = Column(Integer, default=3, index=True)
    price = Column(Integer, default=2, index=True)
