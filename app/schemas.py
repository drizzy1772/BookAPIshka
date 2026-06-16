


from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
from app.models import UserRole

class AuthorBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=260)
    bio: str | None = None
    birth_date: date

    @field_validator("birth_date")
    @classmethod
    def birth_date_not_in_future(cls, v: date) -> date:
        if v > date.today():
            raise ValueError("sorr, that birth_date cannot be entered")
        return v

class AuthorCreate(AuthorBase):
    pass

class AuthorResponse(AuthorBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

class BookBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=300)
    description: str | None = None
    price: int = Field(..., ge=0)
    stock_quantity: int = Field(default=0, ge=0)
    author_id: int

class BookCreate(BaseModel):
    title: str
    price: float
    author_id: int

class BookUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    stock_quantity: int | None = None

class BookResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    price: int
    stock_quantity: int
    author_id: int

class BookListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    title: str
    description: str | None
    price: int
    stock_quantity: int
    author_id: int
    created_at: datetime | None

class OrderStatistics(BaseModel):
    total_orders: int
    total_revenue: int
    average_order_value: float
    popular_books: list[BookListResponse]

class OrderWithBook(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    book_id: int
    quantity: int
    total_price: int
    created_at: datetime
    book: BookListResponse

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str
    role: UserRole

class UserOrderHistory(BaseModel):
    user: UserResponse
    orders: list[OrderWithBook]
    total_spent: int

class WishListItemCreate(BaseModel):
    book_id: int

class WishListItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    book_id: int
    added_at: datetime


class AuthorWithBooksResponse(AuthorResponse):
    books: list[BookListResponse] = []

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=200)
    email: EmailStr
    password: str = Field(..., min_length=6)

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str
    role: UserRole

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: int | None = None

class LoginRequest(BaseModel):
    username: str
    password: str

class OrderCreate(BaseModel):
    book_id: int
    quantity: int = Field(..., gt=0) 

class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    book_id: int
    quantity: int
    total_price: int
    created_at: datetime

class PaginatedBooks(BaseModel):
    items: list[BookResponse]
    total: int
    limit: int
    offset: int
    
class ReviewResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    user_id: int
    book_id: int
    rating: int
    comment: str | None
    created_at: datetime


class ReviewCreate(BaseModel):
    rating: int = Field(ge=1, le=5)
    comment: str | None