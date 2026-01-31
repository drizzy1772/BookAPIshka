#будет тут круд для оих книг
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import create_book, delete_book, get_author, get_book, get_books, update_book
from app.database import get_db
from app.dependencies import get_admin_user
from app.models import User
from app.schemas import BookCreate, BookResponse, BookUpdate, PaginatedBooks

router = APIRouter(prefix="/books", tags=["book"])

@router.get("", response_model=PaginatedBooks)
async def list_books(
    limit: int = 20,
    offset: int = 0,
    author_id: int | None = None,
    db: AsyncSession = Depends(get_db),
):
    books, total = await get_books(db, skip=offset, limit=limit, author_id=author_id)
    return PaginatedBooks(items=books, total=total, limit=limit, offset=offset)

@router.get("/{book_id}", response_model=BookResponse)
async def get_book_detail(
    book_id: int,
    db: AsyncSession = Depends(get_db),
):
    book = await get_book(db, book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book wasn't founded"
        )
    return book

@router.post("", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def add_book(
    book: BookCreate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_admin_user),
):
    author = await get_author(db, book.author_id)
    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The author of this book was not founded",
        )

    return await create_book(db, book)

@router.patch("/{book_id}", response_model=BookResponse)
async def modify_book(
    book_id: int,
    book_update: BookUpdate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_admin_user),
):
    book = await get_book(db, book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book wasnt found"
        )
    updated_book = await update_book(db, book_id, book_update)
    return updated_book

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_book(
    book_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_admin_user),
):
    deleted = await delete_book(db, book_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = "That book was not found"
        )