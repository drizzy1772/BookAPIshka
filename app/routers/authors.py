from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import create_author, get_author, get_author_by_name, get_authors
from app.database import get_db
from app.dependencies import get_admin_user
from app.models import User
from app.schemas import AuthorCreate, AuthorResponse, AuthorWithBooksResponse

router = APIRouter(prefix="/authors", tags=["authors"])


@router.get("", response_model=list[AuthorResponse])
async def list_authors(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    return await get_authors(db, skip=skip, limit=limit)


@router.post("", response_model=AuthorResponse, status_code=status.HTTP_201_CREATED)
async def add_author(
    author: AuthorCreate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_admin_user),
):
    if await get_author_by_name(db, author.name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Author with this name is already registered",
        )

    return await create_author(db, author)


@router.get("/{author_id}", response_model=AuthorWithBooksResponse)
async def get_author_detail(
    author_id: int,
    db: AsyncSession = Depends(get_db),
):
    author = await get_author(db, author_id)
    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Author not found",
        )
    return author