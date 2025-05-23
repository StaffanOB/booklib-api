'''
Booklib API - Is the backdend of the Booklib project. It is a RESTful API that
provides endpoints for managing audio books. The API is built with Flask and
uses Flask-Restful for creating the endpoints. The API is secured with JWT
tokens and uses SQLAlchemy for the ORM. The API is also documented with
Flask-Smorest and uses Flask-Migrate for database migrations.
'''
import os

from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from sqlalchemy.orm import identity
from dotenv import load_dotenv

from db import db
import models
from blocklist import BLOCKLIST

from resources.book import blp as BookBlueprint
from resources.author import blp as AuthorBlueprint
from resources.category_list import blp as CategoryBlueprint
from resources.user import blp as UserBlueprint


def create_app(db_url=None):
    """
    Creates the Flask app and configure it in a factory pattern.
    """

    app = Flask(__name__)
    load_dotenv()

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Booklib API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config[
        "SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True
    db.init_app(app)
    migrate = Migrate(app, db)
    api = Api(app)

    app.config["JWT_SECRET_KEY"] = "staffan"
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blicklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "The token has beenrevoked.", "error": "token_revoked"}
            ),
            401,
        )

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "description": "The token is not fresh.",
                    "error": "fresh_token_required",
                }
            ),
            401,
        )

    @jwt.additional_claims_loader
    def add_claims_to_jwt(indentity):
        # TODO:  <18-10-23, sob> # add a db look up for the user

        if identity == 1:
            return {"is_admin": True}
        return {"is_admin": False}

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired.",
                    "error": "token_expired"}),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )

#    with app.app_context():
#        db.create_all()

    api.register_blueprint(BookBlueprint)
    api.register_blueprint(AuthorBlueprint)
    api.register_blueprint(CategoryBlueprint)
    api.register_blueprint(UserBlueprint)

    return app


app = create_app()
