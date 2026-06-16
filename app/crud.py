









from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.orm import lazyload
from app.models import Author, Book, Order, User, Review, WishList
from app.schemas import AuthorCreate, BookCreate, BookUpdate, OrderCreate, UserCreate
from app.security import get_password_hash
from fastapi import HTTPException


async def get_author(db: AsyncSession, author_id: int) -> Author | None:
    result = await db.execute(
        select(Author).options(selectinload(Author.books)).where(Author.id == author_id)
    )
    return result.scalar_one_or_none()

async def get_author_by_name(db: AsyncSession, name: str) -> Author | None:
    result = await db.execute(select(Author).where(Author.name == name))
    return result.scalar_one_or_none()


async def get_user_email(db:AsyncSession, email: str):
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()

async def get_user_name(db: AsyncSession, username: str):
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()

#RETURN WITH PAGI
async def get_authors(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100
) -> list[Author]:
    result = await db.execute(
        select(Author).offset(skip).limit(limit)
    )
    return list(result.scalars().all())

async def create_author(db: AsyncSession, author: AuthorCreate) -> Author:
    db_author = Author(**author.model_dump())
    db.add(db_author)
    await db.flush()
    await db.refresh(db_author)
    return db_author

async def get_book(db: AsyncSession, book_id: int) -> Book | None:
    result = await db.execute(select(Book).where(Book.id == book_id))
    return result.scalar_one_or_none()

async def get_books(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        author_id: int | None = None,
) ->    tuple[list[Book], int]:
        query = select(Book)
        count_query = select(func.count(Book.id))

        if author_id:
            query = query.where(Book.author_id == author_id)
            count_query = count_query.where(Book.author_id == author_id)
        
        total_result = await db.execute(count_query)
        total = total_result.scalar_one()
    
        result = await db.execute(query.offset(skip).limit(limit))
        return list(result.scalars().all()), total

async def create_book(db: AsyncSession, book: BookCreate) -> Book:
    db_book = Book(**book.model_dump())
    db.add(db_book)
    await db.flush()
    await db.refresh(db_book)
    return db_book

async def update_book(db: AsyncSession, book_id: int, book_update: BookUpdate) -> Book | None:
    db_book = await get_book(db, book_id)
    if not db_book:
        return None

    update_data = book_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_book, field, value)
    
    await db.flush()
    await db.refresh(db_book)
    return db_book

async def delete_book(db: AsyncSession, book_id: int) -> bool:
    book = await get_book(db, book_id)
    if not book:
        return False
    
    await db.delete(book)
    await db.flush()
    return True

async def get_user(db: AsyncSession, user_id: int) -> User | None:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()

async def get_user_by_username(db: AsyncSession, username: str) -> User | None:
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()

async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()

async def create_user(db: AsyncSession, user:UserCreate) -> User:
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password,
    )
    db.add(db_user)
    await db.flush()
    await db.refresh(db_user)
    return db_user

async def get_book_for_update(db:AsyncSession, book_id: int) -> Book | None:
    result = await db.execute(
        select(Book)
        .options(lazyload(Book.author))
        .where(Book.id == book_id)
        .with_for_update()
    )
    return result.scalar_one_or_none()

async def create_order(
        db: AsyncSession,
        user_id: int,
        order_data: OrderCreate,
) -> Order:
    book = await get_book_for_update(db, order_data.book_id)
    if not book:
        raise ValueError("Book not found")
    
    if book.stock_quantity < order_data.quantity:
        raise ValueError(
            f"Not enough stock available: {book.stock_quantity}, requested: {order_data.quantity}"
        )
    
    book.stock_quantity -= order_data.quantity

    order = Order(
        user_id=user_id,
        book_id=order_data.book_id,
        quantity=order_data.quantity,
        total_price=book.price * order_data.quantity,
    )
    db.add(order)
    await db.flush()
    await db.refresh(order)
    return order

async def create_review(
    db: AsyncSession,
    user_id: int,
    book_id: int,
    rating: int,
    comment: str | None,
) -> Review:
    
    review = Review(
        user_id=user_id,
        book_id=book_id,
        rating=rating,
        comment=comment
    )
    db.add(review)
    await db.flush()
    await db.refresh(review)
    return review

async def get_book_reviews(db: AsyncSession, book_id: int) -> list[Review]:
    result = await db.execute(
        select(Review).where(Review.book_id == book_id)
    )
    
    return result.scalars().all()

async def delete_review(db: AsyncSession, review_id: int, user_id: int) -> bool:
    result = await db.execute(
        select(Review).where(Review.id == review_id, Review.user_id == user_id)
    )
    review = result.scalar_one_or_none()
    if not review:
        return False
    
    await db.delete(review)
    await db.flush()
    return True

async def delete_review(db: AsyncSession, review_id: int, user_id: int) -> bool:
    result = await db.execute(
        select(Review).where(Review.id == review_id, Review.user_id == user_id)
    )
    review = result.scalar_one_or_none()
    if not review:
        return False
    
    await db.delete(review)
    await db.flush()
    return True

async def add_to_wishlist(db: AsyncSession, user_id: int, book_id: int) -> WishList:
    wishlist = WishList(
        user_id=user_id,
        book_id=book_id
    )
    db.add(wishlist)
    await db.flush()
    await db.refresh(wishlist)
    return wishlist

async def get_wishlist(db: AsyncSession, user_id: int) -> list[WishList]:
    result = await db.execute(
        select(WishList).where(WishList.user_id == user_id)
    )
    
    return result.scalars().all()

async def remove_from_wishlist(db: AsyncSession, user_id: int, book_id: int) -> bool:
    result = await db.execute(
        select(WishList).where(WishList.user_id == user_id, WishList.book_id == book_id)
    )
    review = result.scalar_one_or_none()
    if not review:
        return False
    
    await db.delete(review)
    await db.flush()
    return True

