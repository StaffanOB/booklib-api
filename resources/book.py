from flask.views import MethodView
from flask_smorest import abort, Blueprint
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import jwt_required, get_jwt

from db import db
from models import BookModel
from schemas import BookSchema, BookUpdateSchema

blp = Blueprint("books", __name__, description="Operations on books")


@blp.route("/book/<string:book_id>")
class Book(MethodView):
    @blp.response(200, BookSchema)
    def get(self, book_id):
        book = BookModel.query.get_or_404(book_id)
        return book

    @jwt_required()
    @blp.arguments(BookUpdateSchema)
    @blp.response(200, BookSchema)
    def put(self, book_data, book_id):
        book = BookModel.query.get(book_id)

        if book:
            book.title = book_data["title"]
            book.author = book_data["author_id"]
        else:
            book = BookModel(id=book_id, **book_data)

        db.session.add(book)
        db.session.commit()

        return book

    @jwt_required()
    def delete(self, book_id):
        book = BookModel.query.get_or_404(book_id)
        db.session.delete(book)
        db.session.commit()

        return {"message": "book deleted"}


@blp.route("/books")
class BookInfo(MethodView):
    @blp.response(200, BookSchema(many=True))
    def get(self):
        return BookModel.query.all()


@blp.route("/book")
class BookList(MethodView):
    @blp.response(200, BookSchema(many=True))
    def get(self):
        return BookModel.query.all()

    @jwt_required()
    @blp.arguments(BookSchema)
    @blp.response(201, BookSchema)
    def post(self, book_data):
        '''
        Create a new book
        '''
        book = BookModel(**book_data)

        try:
            db.session.add(book)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A book with that name exists.")
        except SQLAlchemyError:
            abort(500, message="Something went wronge with the input of the strore")

        return book
