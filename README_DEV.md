# BookLib API - Local Development Guide

## Overview
The BookLib API is a Flask-based REST API for managing a book library system with user authentication, book management, ratings, comments, and tags.

## Prerequisites
- Python 3.12+
- PostgreSQL (via Docker recommended)
- Git

## Quick Setup

### 1. Clone and Setup
```bash
git clone <repository-url>
cd booklib-api
```

### 2. Create Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy the sample environment file and configure:
```bash
cp .env.example .env
# Edit .env with your settings
```

Required environment variables:
```bash
# Database Configuration
DATABASE_URL=postgresql://booklib_user:dev_password@localhost:5432/booklib_dev

# Application Configuration  
FLASK_ENV=development
DEBUG=true
SECRET_KEY=your-secret-key

# JWT Configuration
JWT_SECRET_KEY=your-jwt-secret
```

### 5. Start Database
Make sure PostgreSQL is running. If using the booklib-db repository:
```bash
# In ../booklib-db directory
docker-compose up -d
```

### 6. Run Database Migrations
```bash
flask --app wsgi db upgrade
```

### 7. Start Development Server
```bash
# Option 1: Using Flask CLI
FLASK_APP=wsgi python -m flask run --host=0.0.0.0 --port=5000

# Option 2: Using development script (recommended)
python run_dev.py
```

The API will be available at `http://localhost:5000`

## Development Workflow

### Running Tests
```bash
# Unit tests
python -m pytest tests/unit/

# Integration tests
python -m pytest tests/integration/

# All tests
python -m pytest
```

### Code Style
```bash
# Format code
black .

# Check linting
flake8 app/
```

### Database Operations
```bash
# Create migration
flask --app wsgi db migrate -m "Description"

# Apply migrations
flask --app wsgi db upgrade

# Downgrade migration
flask --app wsgi db downgrade
```

## API Endpoints

### Authentication
- `POST /users/register` - Register new user
- `POST /users/login` - User login
- `GET /users/profile` - Get user profile (authenticated)

### Books
- `GET /books` - List all books
- `POST /books` - Create new book (authenticated)
- `GET /books/{id}` - Get book details
- `PUT /books/{id}` - Update book (authenticated)
- `DELETE /books/{id}` - Delete book (authenticated)

### Health Check
- `GET /health` - API health status

## Project Structure
```
booklib-api/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── config.py            # Configuration settings
│   ├── models/              # SQLAlchemy models
│   ├── routes/              # API route handlers
│   └── static/              # Static files (Swagger)
├── tests/                   # Test suite
├── migrations/              # Database migrations
├── .venv/                   # Virtual environment
├── requirements.txt         # Python dependencies
├── wsgi.py                 # WSGI entry point
├── run_dev.py              # Development server script
└── .env                    # Environment variables
```

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   ```bash
   # Check if PostgreSQL is running
   docker-compose -f ../booklib-db/docker-compose.yml ps
   
   # Verify database exists
   psql postgresql://booklib_user:dev_password@localhost:5432/booklib_dev -c "\dt"
   ```

2. **Import Errors**
   ```bash
   # Ensure virtual environment is activated
   source .venv/bin/activate
   
   # Verify dependencies are installed
   pip list | grep Flask
   ```

3. **Port Already in Use**
   ```bash
   # Find process using port 5000
   lsof -i :5000
   
   # Kill process if needed
   kill <PID>
   ```

4. **Environment Variables Not Loading**
   ```bash
   # Verify python-dotenv is installed
   pip list | grep python-dotenv
   
   # Check .env file exists and has correct format
   cat .env
   ```

### Development Tips

1. **Auto-reload**: Use `python run_dev.py` for automatic code reloading
2. **Database Reset**: Drop and recreate database for clean start
3. **Log Level**: Set `FLASK_ENV=development` for detailed logging
4. **API Testing**: Use tools like Postman or curl for endpoint testing

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Related Repositories
- `booklib-db`: Database setup and migrations
- `booklib-tests`: Test suites and automation
- `booklib-deployment`: Docker and deployment configurations