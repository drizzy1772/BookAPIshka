
📚 Library API
A modern REST API for managing a bookstore with authors, books, orders, and user authentication built with FastAPI and SQLAlchemy.

Tech Stack

FastAPI - Modern web framework
SQLAlchemy 2.0 - Async ORM
PostgreSQL - Primary database
Alembic - Database migrations
Pydantic - Data validation
JWT - Token-based authentication
pytest - Testing framework

 Prerequisites

Python 3.11+
PostgreSQL
pip or poetry

Clone repository

https://github.com/drizzy1772/LibraryAPI.git
cd LibraryAPI

Install dependencies

bash = pip install -r requirements.txt

Setup environment variables

bash = cp .env.example .env

try to edit.env with ur configurations

DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/bookstore
SECRET_KEY=your-secret-key-here
DEBUG=False
ACCESS_TOKEN_EXPIRE_MINUTES=40

Initialize database

alembic upgrade head

Start the server

uvicorn app.main:app --reload

Project Structure

bookstore-api/
├── alembic/                 # Database migrations
│   ├── versions/           # Migration files
│   └── env.py
├── app/
│   ├── routers/            # API routes
│   │   ├── auth.py
│   │   ├── authors.py
│   │   ├── books.py
│   │   └── orders.py
│   ├── config.py           # Configuration settings
│   ├── crud.py             # Database operations
│   ├── database.py         # Database connection
│   ├── dependencies.py     # FastAPI dependencies
│   ├── main.py             # Application entry point
│   ├── models.py           # SQLAlchemy models
│   ├── schemas.py          # Pydantic schemas
│   └── security.py         # Authentication utilities
├── tests/                  # Test suite
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_authors.py
│   ├── test_books.py
│   └── test_orders.py
├── .env.example
├── alembic.ini
├── requirements.txt
└── README.md

Authentication
Register a new user
bashPOST /auth/register
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secure_password"
}
Login
bashPOST /auth/login
{
  "username": "john_doe",
  "password": "secure_password"
}
Response:
json{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
Use the token in subsequent requests:
bashAuthorization: Bearer <your_token>
📖 API Endpoints
Authors
MethodEndpointDescriptionAuth RequiredGET/authorsList all authorsNoGET/authors/{id}Get author details with booksNoPOST/authorsCreate new authorAdmin only
Books
MethodEndpointDescriptionAuth RequiredGET/booksList all books (paginated)NoGET/books/{id}Get book detailsNoPOST/booksCreate new bookAdmin onlyPATCH/books/{id}Update bookAdmin onlyDELETE/books/{id}Delete bookAdmin only

