# BookStore API

A modern REST API for managing a bookstore with authors, books, orders, and user authentication built with FastAPI and SQLAlchemy.

## Features

## Tech Stack

- **FastAPI** 
- **SQLAlchemy 2.0**
- **PostgreSQL**
- **Alembic**
- **Pydantic**
- **JWT**
- **pytest**

## Prerequisites

- Python 3.11+
- PostgreSQL
- pip or poetry

## Visualisation idea
<img width="634" height="430" alt="Untitled Diagram drawio(9)" src="https://github.com/user-attachments/assets/b7691196-63f7-4553-91fb-08ed24eaf578" />


## Installation

1. **Clone the repository**
```bash
git clone https://github.com/drizzy1772/libraryAPI-api.git
cd bookstore-api
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup environment variables**
```bash
cp .env.example .env
```

Edit `.env` with your configuration:
```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/bookstore
SECRET_KEY=your-secret-key-here
DEBUG=False
ACCESS_TOKEN_EXPIRE_MINUTES=40
```

5. **Initialize database**
```bash
# Run migrations
alembic upgrade head
```

6. **Start the server**
```bash
uvicorn app.main:app --reload
```

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc


## Authentication instruction and image
<img width="1445" height="970" alt="Untitled(2)" src="https://github.com/user-attachments/assets/9f9d8645-1330-481d-ae2c-a3d4353ec0db" />

### Register a new user
```bash
POST /auth/register
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secure_password"
}
```

### Login
```bash
POST /auth/login
{
  "username": "john_doe",
  "password": "secure_password"
}
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

Use the token in subsequent requests:
```bash
Authorization: Bearer <your_token>
```

## API Endpoints

### Authors

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/authors` | List all authors | No |
| GET | `/authors/{id}` | Get author details with books | No |
| POST | `/authors` | Create new author | Admin only |

### Books

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/books` | List all books (paginated) | No |
| GET | `/books/{id}` | Get book details | No |
| POST | `/books` | Create new book | Admin only |
| PATCH | `/books/{id}` | Update book | Admin only |
| DELETE | `/books/{id}` | Delete book | Admin only |

### Orders

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/orders` | Place an order | User |

## Testing

Run the test suite:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=app tests/
```

Run specific test file:
```bash
pytest tests/test_books.py
```

## Project Structure

```
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
```
## Configuration

Key settings in `app/config.py`:
- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - JWT signing key
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Token expiration time
- `DEFAULT_PAGE_SIZE` - Default pagination size
- `MAX_PAGE_SIZE` - Maximum items per page
