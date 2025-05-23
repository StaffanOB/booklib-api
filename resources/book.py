
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from models import BookModel, AuthorModel, CategoryModel
from services.book_service import add_book_with_authors_and_categories
from schemas import BookSchema, BookUpdateSchema, CategorySchema, BookCategorySchema
from sqlalchemy.exc import SQLAlchemyError

blp = Blueprint("Books", "books", description="Operations on books")


@blp.route("/books")
class BookList(MethodView):
    @blp.response(200, BookSchema(many=True))
    def get(self):
        return BookModel.query.all()

    @blp.arguments(BookSchema)
    @blp.response(201, BookSchema)
    def post(self, book_data):
        book = add_book_with_authors_and_categories(
            book_title=book_data["title"],
            author_names=book_data.get("author_ids", []),
            category_names=book_data.get("category_ids", [])
        )
#        book = BookModel(title=book_data["title"])
#        if 'author_ids' in book_data:
#            book.authors = AuthorModel.query.filter(
#                AuthorModel.id.in_(book_data['author_ids'])).all()
#        if 'category_ids' in book_data:
#            book.categories = CategoryModel.query.filter(
#                CategoryModel.id.in_(book_data['category_ids'])).all()
#        try:
#            db.session.add(book)
#            db.session.commit()
#        except SQLAlchemyError:
#            abort(500, message="An error occurred while inserting the book.")
        return book


@blp.route("/book/<int:book_id>")
class Book(MethodView):
    @blp.response(200, BookSchema)
    def get(self, book_id):
        return BookModel.query.get_or_404(book_id)

    @blp.arguments(BookUpdateSchema)
    @blp.response(200, BookSchema)
    def put(self, book_data, book_id):
        book = BookModel.query.get_or_404(book_id)
        if book:
            if "title" in book_data:
                book.title = book_data["title"]
            if "author_ids" in book_data:
                book.authors = AuthorModel.query.filter(
                    AuthorModel.id.in_(book_data["author_ids"])).all()
            if "category_ids" in book_data:
                book.categories = CategoryModel.query.filter(
                    CategoryModel.id.in_(book_data["category_ids"])).all()
            db.session.commit()
        return book

    @blp.response(200)
    def delete(self, book_id):
        book = BookModel.query.get_or_404(book_id)
        db.session.delete(book)
        db.session.commit()
        return {"message": "Book deleted"}
