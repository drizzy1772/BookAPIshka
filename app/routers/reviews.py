



from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.dependencies import get_current_user
from app.models import User
from app.crud import create_review, get_book_reviews, delete_review, get_book
from app.schemas import ReviewResponse, ReviewCreate


router = APIRouter(tags=["reviews"])

@router.post("/books/{book_id}/reviews", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
async def add_review(
    book_id: int,
    review: ReviewCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    book = await get_book(db, book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book wasnt found"
        )
    
    review = await create_review(
        db=db,
        user_id=current_user.id,
        book_id=book_id,
        rating=review.rating,
        comment=review.comment
        
    )
    
    return review

@router.get("/books/{book_id}/reviews", response_model=list[ReviewResponse])
async def list_reviews(
    book_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await get_book_reviews(
        db=db,
        book_id=book_id,
    )


@router.delete("/reviews/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_reviewss(
    review_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    reviews = await delete_review(db, review_id, current_user.id)
    if not reviews:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="review was not founded"
        )
