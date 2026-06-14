import enum
from datetime import date, datetime

from sqlalchemy import ForeignKey, Index, String, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional

from app.database import Base

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"

class Author(Base):
    __tablename__ = "authors"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    bio: Mapped[str | None] = mapped_column(Text)
    birth_date: Mapped[date]
    books: Mapped[list["Book"]] = relationship(back_populates="author", lazy="selectin")

class Book(Base):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    description: Mapped[str | None] = mapped_column(Text)
    price: Mapped[int]
    stock_quantity: Mapped[int] = mapped_column(default=0)

    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"), nullable=False)

    author: Mapped['Author'] = relationship(back_populates='books', lazy="joined")

    __table_args__ = (Index("ix_books_author_id", "author_id"),)

    orders: Mapped[list["Order"]] = relationship(back_populates="book")

    wishlist_items: Mapped[list["WishList"]] = relationship(back_populates="book")

    reviews: Mapped[list["Review"]] = relationship(
        back_populates="book",
        cascade="all, delete-orphan"
    )

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(100), unique=True)
    full_name: Mapped[str | None] = mapped_column(String(255), default=None, nullable=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    email_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable = False)
    password: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    role: Mapped[UserRole] = mapped_column(default=UserRole.USER)
    delete_at: Mapped[datetime | None] = mapped_column(default=None)

    orders: Mapped[list["Order"]] = relationship(back_populates="user", lazy="selectin")

    wishlist_items: Mapped[list["WishList"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )
    reviews: Mapped[list["Review"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    quantity: Mapped[int]
    total_price: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="orders", lazy="joined")
    book: Mapped["Book"] = relationship(back_populates="orders", lazy="joined")

class WishList(Base):
    __tablename__ = "wishlists"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    added_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="wishlist_items")
    book: Mapped["Book"] = relationship(back_populates="wishlist_items")

class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    rating: Mapped[int]
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)


    user: Mapped["User"] = relationship(back_populates="reviews")
    book: Mapped["Book"] = relationship(back_populates="reviews")
