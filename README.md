# BookLib API

A lightweight REST API for managing books, users, tags, comments, ratings, and plugins.

## Features
- User registration/login (JWT)
- CRUD for books, tags, comments, ratings
- Plugin architecture
- Swagger/OpenAPI docs
- Docker & Jenkins ready

## 🚀 Local Development Guide

**For detailed local development setup instructions, see [README_DEV.md](README_DEV.md)**

## Quick Start for Local Development

### Prerequisites
- Python 3.11+
- Docker and Docker Compose (for database)
- Git

### 1. Setup Development Environment
```bash
# Clone all related repositories
git clone https://github.com/StaffanOB/booklib-api.git
git clone https://github.com/StaffanOB/booklib-db.git
cd booklib-api

# Create Python virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Start Database Services
```bash
# Start the database (from booklib-db repository)
cd ../booklib-db
./scripts/setup.sh

# Or start manually
docker-compose up -d db

# Wait for database to be ready
./scripts/wait-for-db.sh
```

### 3. Configure Environment
```bash
cd ../booklib-api

# Create .env file for local development
cat > .env << EOF
# Database Configuration
DATABASE_URL=postgresql://booklib_user:dev_password@localhost:5432/booklib_dev

# Application Configuration  
FLASK_ENV=development
DEBUG=true
SECRET_KEY=dev-secret-key

# JWT Configuration
JWT_SECRET_KEY=dev-jwt-secret

# Optional: External Services
REDIS_URL=redis://localhost:6379/0
EOF
```

### 4. Initialize Database
```bash
# Run database migrations
alembic upgrade head

# Load sample data (optional)
python -c "
from app import create_app, db
from app.models import User, Book, Tag

app = create_app()
with app.app_context():
    # Create sample user
    user = User(username='dev', email='dev@booklib.com')
    user.set_password('password')
    db.session.add(user)
    
    # Create sample book
    book = Book(title='Sample Book', author='Dev Author', description='A sample book for development')
    db.session.add(book)
    
    db.session.commit()
    print('Sample data created!')
"
```

### 5. Run the API
```bash
# Start the development server
python app/main.py

# Or with hot reload
export FLASK_APP=app.main:app
export FLASK_ENV=development
flask run --host=0.0.0.0 --port=5000
```

### 6. Access the API
- **API Base URL**: http://localhost:5000
- **API Documentation**: http://localhost:5000/docs
- **Health Check**: http://localhost:5000/health

### 7. Development Workflow
```bash
# Run tests
pytest tests/

# Run specific test file
pytest tests/unit/test_books.py -v

# Run with coverage
pytest --cov=app tests/

# Lint code
flake8 app/

# Format code
black app/
```

## Integration with Other Services

### Database Integration
This API requires the `booklib-db` service:
```bash
# Make sure database is running
cd ../booklib-db && docker-compose ps

# If not running, start it
docker-compose up -d db
```

### Testing Integration  
Run tests against your local API:
```bash
# From booklib-tests repository
cd ../booklib-tests
robot --variable BASE_URL:http://localhost:5000 robot/api/
```

## Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `DATABASE_URL` | PostgreSQL connection string | `sqlite:///booklib.db` | Yes |
| `SECRET_KEY` | Flask secret key | None | Yes |
| `JWT_SECRET_KEY` | JWT signing secret | None | Yes |
| `FLASK_ENV` | Flask environment | `production` | No |
| `DEBUG` | Enable debug mode | `false` | No |
| `REDIS_URL` | Redis connection string | None | No |

## Docker Development

### Build and Run with Docker
```bash
# Build Docker image
docker build -t booklib-api:dev .

# Run with database
docker-compose -f ../booklib-deployment/docker-compose.yml up -d

# Or run API only (requires external database)
docker run -p 5000:5000 \
  -e DATABASE_URL=postgresql://booklib_user:dev_password@host.docker.internal:5432/booklib_dev \
  booklib-api:dev
```

## Troubleshooting

### Database Connection Issues
```bash
# Check if database is running
docker ps | grep postgres

# Test database connection
python -c "
import psycopg2
try:
    conn = psycopg2.connect('postgresql://booklib_user:dev_password@localhost:5432/booklib_dev')
    print('✅ Database connection successful')
    conn.close()
except Exception as e:
    print(f'❌ Database connection failed: {e}')
"
```

### Migration Issues
```bash
# Check migration status
alembic current

# Show migration history  
alembic history

# Reset database (⚠️ destroys data)
alembic downgrade base
alembic upgrade head
```

### Import/Module Issues
```bash
# Check Python path
python -c "import sys; print('\n'.join(sys.path))"

# Install in development mode
pip install -e .
```

### 2. View Swagger/OpenAPI docs
Visit: [http://127.0.0.1:5000/docs](http://127.0.0.1:5000/docs)

## Docker

### Build and run with Docker
```bash
docker build -t booklib-api .
docker run -p 5000:5000 booklib-api
```

## Testing

### Run unit tests
```bash
pytest tests/
```

## CI/CD

Jenkins pipeline is defined in `Jenkinsfile`.

---
For more details, see `prd.md`.
