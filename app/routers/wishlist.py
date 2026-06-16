








from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.dependencies import get_current_user
from app.models import User
from app.crud import add_to_wishlist, get_wishlist, remove_from_wishlist
from app.schemas import WishListItemCreate, WishListItemResponse



router = APIRouter(tags=["wishlist"])

@router.post("/wishlist/{book_id}", response_model=WishListItemResponse, status_code=status.HTTP_201_CREATED)
async def add_to_wishlist_router(
    book_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await add_to_wishlist(
        db,
        current_user.id,
        book_id
    )


@router.get("/wishlist", response_model=list[WishListItemResponse])
async def get_wishlist_router(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await get_wishlist(db, current_user.id)


@router.delete("/wishlist/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_from_wishlist_router(
    book_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    remover = await remove_from_wishlist(
        db,
        current_user.id,
        book_id,
    )
    if not remover:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="book was not removed from wishlist"
        )



