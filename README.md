# Booklib API


The Audiobook Management System is a Flask application designed to manage audiobooks, inspired by the functionality of goodreads.com. It allows users to keep track of their audiobook collection, rate audiobooks, and discover new ones.

## Features

- User Registration and Authentication
- Audiobook CRUD Operations (Create, Read, Update, Delete)
- User Ratings and Reviews
- Discover New Audiobooks
- Dockerized Application with PostgreSQL Database

## Technologies Used

- Flask: A micro web framework for Python
- SQLAlchemy: SQL toolkit and Object-Relational Mapping (ORM) library
- Docker: Containerization platform
- PostgreSQL: Relational database management system
- Flask-Security: Flask extension for handling security-related tasks
- Flask-Migrate: Flask extension for database migrations
- Other dependencies: See `requirements.txt`

## Getting Started

## Docker compose

To rebuild the application with docker compose, run the following command:
```bash
docker compose up --build --force-recreate --no-deps
```

### Prerequisites

- Docker
- Docker Compose
- Python (for development)

### Setup

1. Clone the repository:

### Configure Environment Variables
In the .env file, you can set the following environment variables:

#### Inititate the database
```bash
flask db init
```

#### Migrate the database
```bash
flask db migrate
```

#### Upgrade the database
```bash
flask db upgrade
```
#### Run the application
```bash	

flask run
```
DATABASE_URL=postgresql://[user]:[password]@localhost:5432/[database_name]
