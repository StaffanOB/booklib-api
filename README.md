# BookLib API

A lightweight REST API for managing books, users, tags, comments, ratings, and plugins.

## Features
- User registration/login (JWT)
- CRUD for books, tags, comments, ratings
- Plugin architecture
- Swagger/OpenAPI docs
- Docker & Jenkins ready

## Installation

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd booklib-api_ai
```

### 2. Create a Python virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Alembic migrations (optional, for DB setup)
```bash
alembic upgrade head
```

### 5. Initialize the database tables (required for first run)
If you are not using Alembic migrations, the tables will be created automatically when you start the app. To manually create tables, run:
```bash
python app/main.py
```
This will create all tables in the configured database (default: SQLite file `booklib.db`).

## Running the API

### 1. Start the Flask app
```bash
python app/main.py
```

The API will be available at `http://127.0.0.1:5000/`

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
