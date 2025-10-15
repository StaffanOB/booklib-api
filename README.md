# BookLib API

A Flask-based REST API for managing a book library system with user authentication, reviews, ratings, comments, tags, and external plugin integrations.

## ✨ Features

- **User Management**: Registration, login with JWT authentication
- **Book Management**: Full CRUD operations for books with author information
- **Reviews & Ratings**: Users can write reviews with reading format (paperback, audiobook, ebook) and rate books
- **Comments**: Threaded commenting system on books
- **Tags**: Organize books with custom tags
- **Plugin Architecture**: Extensible plugin system for integrating external book services (Goodreads, Google Books)
- **API Documentation**: Interactive Swagger/OpenAPI documentation
- **Database Migrations**: Alembic-based schema versioning
- **Production Ready**: Docker containerization with Jenkins CI/CD pipeline

## � Documentation

- **[README_DEV.md](README_DEV.md)** - Complete local development setup guide
- **[README_DEPLOYMENT.md](README_DEPLOYMENT.md)** - Production deployment with Docker and Jenkins

## 🚀 Quick Start

### Local Development

```bash
# 1. Clone and setup
git clone https://github.com/StaffanOB/booklib-api.git
cd booklib-api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
# Edit .env with your database settings

# 3. Run migrations
alembic upgrade head

# 4. Start the API
python app/main.py
```

Visit http://localhost:5000/docs for interactive API documentation.

**For detailed setup instructions, see [README_DEV.md](README_DEV.md)**

### Production Deployment

The API includes automated deployment via Jenkins to a standalone Docker container with PostgreSQL.

**For complete deployment guide, see [README_DEPLOYMENT.md](README_DEPLOYMENT.md)**

## 🏗️ Architecture

```
booklib-api/
├── app/
│   ├── models/          # SQLAlchemy database models
│   │   ├── user.py
│   │   ├── book.py
│   │   ├── review.py    # New: Reviews with reading format
│   │   ├── rating.py
│   │   ├── comment.py
│   │   └── tag.py
│   ├── routes/          # API endpoint handlers
│   │   ├── users.py
│   │   ├── books.py
│   │   ├── reviews.py   # New: Review management
│   │   ├── ratings.py
│   │   ├── comments.py
│   │   ├── tags.py
│   │   └── plugins.py
│   ├── plugins/         # External service integrations
│   └── static/          # Swagger specification
├── migrations/          # Alembic database migrations
├── tests/              # Pytest test suite
├── Dockerfile          # Production container image
├── docker-compose.yml  # Standalone deployment config
└── Jenkinsfile         # CI/CD pipeline

```

## 🔌 API Endpoints

### Authentication

- `POST /users/register` - Register new user
- `POST /users/login` - Login and get JWT token

### Books

- `GET /books` - List all books
- `POST /books` - Create book (authenticated)
- `GET /books/{id}` - Get book details
- `PUT /books/{id}` - Update book (authenticated)
- `DELETE /books/{id}` - Delete book (authenticated)

### Reviews

- `GET /reviews` - List all reviews
- `POST /reviews` - Create review (authenticated)
- `GET /reviews/{id}` - Get review details
- `GET /reviews/book/{book_id}` - Get reviews for a book
- `GET /reviews/user/{user_id}` - Get reviews by user
- `PUT /reviews/{id}` - Update review (authenticated)
- `DELETE /reviews/{id}` - Delete review (authenticated)

### Ratings, Comments, Tags

- Full CRUD operations available
- See `/docs` endpoint for complete API reference

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test suite
pytest tests/unit/
pytest tests/integration/
```

## 🛠️ Technology Stack

- **Framework**: Flask 3.0+
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT (PyJWT)
- **Migrations**: Alembic
- **API Documentation**: Swagger/OpenAPI
- **Testing**: Pytest
- **Containerization**: Docker
- **CI/CD**: Jenkins
- **WSGI Server**: Gunicorn

## 📊 Database Schema

The API uses PostgreSQL with the following main tables:

- `users` - User accounts and authentication
- `books` - Book catalog with titles and authors
- `reviews` - User reviews with reading format tracking
- `ratings` - Numerical ratings (1-5 stars)
- `comments` - User comments on books
- `tags` - Book categorization tags
- `book_tags` - Many-to-many relationship

## 🔐 Environment Variables

| Variable         | Description                          | Required |
| ---------------- | ------------------------------------ | -------- |
| `DATABASE_URL`   | PostgreSQL connection string         | Yes      |
| `SECRET_KEY`     | Flask secret key                     | Yes      |
| `JWT_SECRET_KEY` | JWT token signing key                | Yes      |
| `FLASK_ENV`      | Environment (development/production) | No       |
| `DEBUG`          | Enable debug mode                    | No       |

## 📝 License

This project is part of the BookLib ecosystem.

## 🤝 Related Repositories

- **booklib-db** - Database setup and initialization
- **booklib-tests** - Robot Framework integration tests

---

For detailed information:

- Development setup: [README_DEV.md](README_DEV.md)
- Production deployment: [README_DEPLOYMENT.md](README_DEPLOYMENT.md)
