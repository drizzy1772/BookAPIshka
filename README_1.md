# 📚 BookStore API

A modern REST API for managing a bookstore with authors, books, orders, and user authentication built with FastAPI and SQLAlchemy.

## ✨ Features

- **User Authentication & Authorization**
  - JWT-based authentication
  - Role-based access control (Admin/User)
  - Secure password hashing with bcrypt

- **Book Management**
  - CRUD operations for books
  - Stock quantity tracking
  - Pagination support
  - Filter by author

- **Author Management**
  - Author profiles with biography
  - Book associations
  - Admin-only creation

- **Order System**
  - Place orders with automatic stock reduction
  - Order history tracking
  - Stock validation

- **Reviews & Wishlists** (Models ready for implementation)
  - User reviews for books
  - Wishlist functionality

## 🛠 Tech Stack

- **FastAPI** - Modern web framework
- **SQLAlchemy 2.0** - Async ORM
- **PostgreSQL** - Primary database
- **Alembic** - Database migrations
- **Pydantic** - Data validation
- **JWT** - Token-based authentication
- **pytest** - Testing framework

## 📋 Prerequisites

- Python 3.11+
- PostgreSQL
- pip or poetry

## 🚀 Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/bookstore-api.git
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

The API will be available at `http://localhost:8000`

## 📚 API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔐 Authentication

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

## 📖 API Endpoints

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

## 💡 Usage Examples

### Create an Author (Admin only)
```bash
curl -X POST "http://localhost:8000/authors" \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "J.K. Rowling",
    "bio": "British author, best known for Harry Potter series",
    "birth_date": "1965-07-31"
  }'
```

### Create a Book (Admin only)
```bash
curl -X POST "http://localhost:8000/books" \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Harry Potter and the Philosopher Stone",
    "description": "The first book in the Harry Potter series",
    "price": 2500,
    "stock_quantity": 100,
    "author_id": 1
  }'
```

### List Books with Pagination
```bash
curl "http://localhost:8000/books?limit=20&offset=0"
```

### Filter Books by Author
```bash
curl "http://localhost:8000/books?author_id=1"
```

### Place an Order
```bash
curl -X POST "http://localhost:8000/orders" \
  -H "Authorization: Bearer <user_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "book_id": 1,
    "quantity": 2
  }'
```

## 🧪 Testing

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

## 📁 Project Structure

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

## 🗄 Database Schema

### Users
- id, username, email, password (hashed)
- role (ADMIN/USER), is_active, email_verified

### Authors
- id, name, bio, birth_date

### Books
- id, title, description, price, stock_quantity
- author_id (FK to Authors)

### Orders
- id, user_id, book_id, quantity, total_price
- created_at

### Reviews
- id, user_id, book_id, rating, comment, created_at

### Wishlists
- id, user_id, book_id, added_at

## 🔄 Database Migrations

Create a new migration after model changes:
```bash
alembic revision --autogenerate -m "Description of changes"
```

Apply migrations:
```bash
alembic upgrade head
```

Rollback last migration:
```bash
alembic downgrade -1
```

## 🛡 Security Features

- Password hashing with bcrypt
- JWT token-based authentication
- Role-based access control
- Protected admin endpoints
- SQL injection prevention via ORM
- Input validation with Pydantic

## ⚙️ Configuration

Key settings in `app/config.py`:
- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - JWT signing key
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Token expiration time
- `DEFAULT_PAGE_SIZE` - Default pagination size
- `MAX_PAGE_SIZE` - Maximum items per page

## 🐛 Troubleshooting

### Database connection issues
```bash
# Check PostgreSQL is running
sudo service postgresql status

# Check connection string in .env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/bookstore
```

### Migration errors
```bash
# Clean database (WARNING: deletes all data)
python clean_db.py

# Re-run migrations
alembic upgrade head
```

## 📝 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📧 Contact

Your Name - your.email@example.com

Project Link: [https://github.com/yourusername/bookstore-api](https://github.com/yourusername/bookstore-api)

---

Made with ❤️ using FastAPI
