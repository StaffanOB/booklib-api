from flask import request
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import AuthorModel
from schemas import AuthorSchema, AuthorUpdateSchema

blp = Blueprint("authors", __name__, description="Operations on stores")


@blp.route("/author/<string:author_id>")
class Author(MethodView):
    @blp.response(200, AuthorSchema)
    def get(self, author_id):
        author = AuthorModel.query.get_or_404(author_id)
        return author

    @jwt_required()
    def delete(self, author_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege rerquired")

        author = AuthorModel.query.get_or_404(author_id)
        db.session.delete(author)
        db.session.commit()

        return {"message": "Author deleted"}

    @jwt_required()
    @blp.arguments(AuthorUpdateSchema)
    @blp.response(200, AuthorSchema)
    def put(self, author_data, author_id):
        author = AuthorModel.query.get(author_id)

        if author:
            author.price = author_data["price"]
            author.name = author_data["name"]
        else:
            author = AuthorModel(id=author_id, **author_data)

        db.session.add(author)
        db.session.commit()

        return author


@blp.route("/authors")
class AuthorInfo(MethodView):
    @blp.response(200, AuthorSchema(many=True))
#    def get(self):
#        return AuthorModel.query.all()
    def get(self):

        results = AuthorModel.query.all()
        return results


@blp.route("/author")
class AuthorList(MethodView):
    # @jwt_required(fresh=True)
    @blp.arguments(AuthorSchema)
    @blp.response(201, AuthorSchema)
    def post(self, author_data):
        author = AuthorModel(**author_data)

        try:
            db.session.add(author)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occured while inserting in to authors")

        return author
