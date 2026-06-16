#моя точка входа

from fastapi import FastAPI
from app.database import engine, Base

from app.routers.auth import router as auth_router
from app.routers.authors import router as authors_router
from app.routers.books import router as books_router
from app.routers.orders import router as orders_router
from app.routers.reviews import router as reviews_router
from app.routers.wishlist import router as wishlist_router

app = FastAPI(
    title="BookStoreApishka",
    description="REST API for ordering, managing books with authors also",
    version="1.0"
)
app.include_router(auth_router)
app.include_router(authors_router)
app.include_router(books_router)
app.include_router(orders_router)
app.include_router(reviews_router)
app.include_router(wishlist_router)

@app.get("/")
async def root():
    return {
        "message": "BookStoreApishka",
        "docs": "docs",
        "endpoints": {
            "books": "/books",
            "authors": "/authors",
            "auth": "/auth/register, /auth/login",
            "orders": "/orders"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "ok"}











