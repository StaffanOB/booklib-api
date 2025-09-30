# Product Requirements Document (PRD)
**Project Name:** Book REST API  
**Owner:** Staffan (with AI Co-Pilot)  
**Version:** 0.4 Draft  

---

## 1. Overview  
A lightweight REST API for managing books users have read or want to read.  
The API will be built with:  
- **Python 3**  
- **Flask (latest)**  
- **SQLAlchemy + Alembic**  
- **pytest** (unit tests)  
- **Robot Framework + RequestsLibrary** (API tests)  
- **Docker** for containerization  
- **Jenkins** for CI/CD  
- **GitHub** for source control  

The API enforces **authentication (JWT)** for all write operations. Reading books and comments is public.  

---

## 2. Goals  
- Secure book management API with user authentication.  
- CRUD operations for users, books, tags, comments, and ratings.  
- Plugin architecture to extend functionality and integrate with external APIs.  
- Automated testing and deployment.  

---

## 3. Features  

### 3.1 User Management  
- Register (`username`, `email`, `password`)  
- Login/logout (JWT token)  
- Update user details  
- Delete user (hard delete)  
- Remove user (soft delete/archive)  

### 3.2 Book Management  
- Add book (title, author, description, publish year, series, tags)  
- Update book details  
- Delete book (hard delete)  
- Remove book (soft delete/archive)  
- Public: View books (list/search/detail)  

### 3.3 Categories & Tags  
- Assign tags to books  
- Create/manage categories/tags  
- Filter/search books by tag  

### 3.4 Comments  
- Public: Read comments  
- Authenticated users:  
  - Add comment  
  - Update own comment  
  - Delete own comment  

### 3.5 Ratings  
- Authenticated users:  
  - Rate book (1–5)  
  - Update rating  
- API calculates & displays average rating per book  

### 3.6 Plugins & Integrations  
- Define plugin interface (Python modules)  
- Dynamically load/unload plugins  
- Enable external API integrations (e.g., Goodreads, Google Books)  

---

## 4. Technical Requirements  

### 4.1 Functional  
- RESTful endpoints (JSON)  
- JWT authentication for protected operations  
- Input validation & error handling  
- Swagger/OpenAPI documentation  
- SQLAlchemy models + Alembic migrations  

### 4.2 Non-Functional  
- Secure password storage (bcrypt/argon2)  
- Public endpoints read-only, private endpoints require auth  
- CI/CD: automated test & deploy via Jenkins + Docker  
- ≥80% code coverage (pytest + Robot Framework)  
- API stable under 100+ concurrent requests  

---

## 5. Example API Endpoints  

### User  
- `POST /users/register`  
- `POST /users/login`  
- `POST /users/logout`  
- `PUT /users/{id}` (auth required)  
- `DELETE /users/{id}` (hard delete, auth required)  

### Books  
- `GET /books` (public)  
- `GET /books/{id}` (public)  
- `POST /books` (auth required)  
- `PUT /books/{id}` (auth required)  
- `DELETE /books/{id}` (auth required)  

### Tags  
- `GET /tags` (public)  
- `POST /tags` (auth required)  
- `PUT /tags/{id}` (auth required)  
- `DELETE /tags/{id}` (auth required)  

### Comments  
- `GET /books/{id}/comments` (public)  
- `POST /books/{id}/comments` (auth required)  
- `PUT /books/{id}/comments/{comment_id}` (auth required, owner only)  
- `DELETE /books/{id}/comments/{comment_id}` (auth required, owner only)  

### Ratings  
- `GET /books/{id}/ratings` (average rating, public)  
- `POST /books/{id}/ratings` (auth required)  
- `PUT /books/{id}/ratings/{rating_id}` (auth required, owner only)  

### Plugins  
- `GET /plugins` (list active plugins)  
- `POST /plugins/load` (auth required, admin only)  
- `POST /plugins/unload` (auth required, admin only)  

---

## 6. Database Schema Design  

### Entity-Relationship Overview  

**Users** – Manage authentication and ownership of comments/ratings.  
**Books** – Core entity with metadata and linked to tags, comments, and ratings.  
**Tags** – Many-to-many relationship with Books.  
**Comments** – Linked to both Users and Books.  
**Ratings** – Linked to both Users and Books. Each user can rate a book once.  
**Plugins** – Stored metadata about active integrations.  

---

### Tables  

#### Users  
- id (PK)  
- username (unique)  
- email (unique)  
- password_hash  
- created_at  
- updated_at  
- is_active  

#### Books  
- id (PK)  
- title  
- author  
- description  
- publish_year  
- series  
- created_at  
- updated_at  
- is_active  

#### Tags  
- id (PK)  
- name (unique)  

**BookTags (junction table)**  
- book_id (FK)  
- tag_id (FK)  

#### Comments  
- id (PK)  
- book_id (FK)  
- user_id (FK)  
- content  
- created_at  
- updated_at  

#### Ratings  
- id (PK)  
- book_id (FK)  
- user_id (FK, unique with book_id)  
- rating (1–5)  
- created_at  
- updated_at  

#### Plugins  
- id (PK)  
- name (unique)  
- description  
- is_enabled  
- created_at  

---

## 7. Data Models (SQLAlchemy ORM)  

```python
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    comments = db.relationship("Comment", backref="user", lazy=True)
    ratings = db.relationship("Rating", backref="user", lazy=True)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    publish_year = db.Column(db.Integer)
    series = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    comments = db.relationship("Comment", backref="book", lazy=True)
    ratings = db.relationship("Rating", backref="book", lazy=True)
    tags = db.relationship("Tag", secondary="book_tags", back_populates="books")


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    books = db.relationship("Book", secondary="book_tags", back_populates="tags")


class BookTag(db.Model):
    __tablename__ = "book_tags"
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey("tag.id"), primary_key=True)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    __table_args__ = (
        db.UniqueConstraint("book_id", "user_id", name="unique_book_user_rating"),
    )


class Plugin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    is_enabled = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```
---

## 8. Success Metrics  
- All CRUD operations functional and tested.  
- Authentication required for all protected operations.  
- Swagger/OpenAPI docs generated and usable.  
- Jenkins pipeline: build → test → deploy passing.  
- Plugin loader working with at least one sample integration.  

---

## 9. Risks  
- Plugin system complexity → start minimal (just load/unload Python modules).  
- Security risks (passwords, JWT handling) → use strong hashing + token expiry.  
- External API reliability → use caching/fallbacks.  
