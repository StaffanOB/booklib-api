# CONTRIBUTING

## How to build docker image
docker build -t flask-smorest-api .

## How to run Docker locally
'''
docker run -dp 5000:5000 -w /app -v "$(pwd):/app" flask-smorest-api sh -c "flask run --host 0.0.0.0"
'''
## Environments


### Local 
add .env file with the variable for the database url. Example in the repo

### Produciton
docker_entry_point file runs at app starup and ensures that that the database
migaration is run to update the database.

production have to have environmet variables set to beable to connect to the 
database.


## Development

### Adding a New Endpoint
To add a new endpoint that interacts with the database, follow these steps:

1. Define the Model:
   * Create a new SQLAlchemy model in models.py or in a separate file in the models directory.
2. Define the Schema:
   * Create a new Marshmallow schema in schemas.py or in a separate file in the schemas directory. This schema will handle serialization and deserialization of the data.
3. Create the Resource:
   * Create a new resource class in the resources directory. This class will handle HTTP requests for the new endpoint.
   * Use Flask-Smorest to define routes and handle requests.
4. Register the Blueprint:
   * Register the new blueprint in the create_app function in app.py.

### Examples
Here’s an example of adding a new endpoint for Publishers.

**Step 1:** Define the Model
```python
# models/publisher.py
from db import db

class PublisherModel(db.Model):
    __tablename__ = "publishers"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    books = db.relationship("BookModel", back_populates="publisher")
```

**Step 2:** Define the Schema
```python
# schemas/publisher.py
from marshmallow import Schema, fields

class PublisherSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
```

**Step 3:** Create the Resource
```python
# resources/publisher.py
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError
from db import db
from models.publisher import PublisherModel
from schemas.publisher import PublisherSchema

blp = Blueprint("publishers", __name__, description="Operations on publishers")

@blp.route("/publishers")
class PublisherList(MethodView):
    @blp.response(200, PublisherSchema(many=True))
    def get(self):
        return PublisherModel.query.all()

    @blp.arguments(PublisherSchema)
    @blp.response(201, PublisherSchema)
    def post(self, publisher_data):
        publisher = PublisherModel(**publisher_data)
        try:
            db.session.add(publisher)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the publisher.")
        return publisher
```

**Step 4:** Register the Blueprint
```python
# app.py
from resources.publisher import blp as PublisherBlueprint

def create_app(db_url=None):
    # ... existing configuration ...
    
    api.register_blueprint(PublisherBlueprint)
    
    return app
```
_____________________
## Setup database

'''
flask db init
'''

### Migrate new changes
'''
flsk db migrate
flak db upgrade
'''
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
In the .env file, you can set the following environment variables in docker compose:

#### Inititate the database
```bash
docker compose exec api flask db init
```

#### Migrate the database
```bash
flask db migrate
docker compose exec api flask db migrate
```

#### Upgrade the database
```bash
docker compose exec api flask db upgrade
```
#### Run the application
```bash	

flask run
```
DATABASE_URL=postgresql://[user]:[password]@localhost:5432/[database_name]

## Run tests
Unite tests are written using pytest. Use pytest-watch to run tests
automatically when a file changes.

To run the tests, run the following command:
```bash
pytest tests/
or
ptw tests/current_test.py
```
