






from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import create_user, get_user_email, get_user_name
from app.database import get_db
from app.schemas import LoginRequest, Token, UserCreate, UserResponse
from app.security import create_access_token, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def registered(user: UserCreate, db: AsyncSession = Depends(get_db)):
    if await get_user_name(db, user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this name already registered"   
        )

    if await get_user_email(db, user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail = "Email already exists",
        )
    
    return await create_user(db, user)

@router.post("/login", response_model=Token)
async def login(credentials: LoginRequest, db: AsyncSession = Depends(get_db)):
    user = await get_user_name(db, credentials.username)

    if not user or not verify_password(credentials.password, user.password):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Thats password is unauthorized",
        )

    access_token = create_access_token(data={'sub': str(user.id)})
    return Token(access_token=access_token)