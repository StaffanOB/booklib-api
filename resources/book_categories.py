
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from models import BookModel, AuthorModel, CategoryModel
from schemas import BookSchema, BookUpdateSchema, CategorySchema, BookCategorySchema
from sqlalchemy.exc import SQLAlchemyError

blp = Blueprint("BooksCategories", "bookscategories", description="Operations on BooksCategories")


@blp.route("/books/<int:book_id>/categories")
class BookCategories(MethodView):
    @blp.response(200, CategorySchema(many=True))
    def get(self, book_id):
        book = BookModel.query.get_or_404(book_id)
        return book.categories

    @blp.arguments(BookCategorySchema)
    @blp.response(200, CategorySchema(many=True))
    def put(self, category_data, book_id):
        category_id = category_data.get("category_id")
        book = BookModel.query.get_or_404(book_id)
        category = CategoryModel.query.get_or_404(category_id)

        if category not in book.categories:
            book.categories.append(category)
            db.session.commit()

        return book.categories

    @blp.arguments(BookCategorySchema)
    @blp.response(200, CategorySchema(many=True))
    def delete(self, category_data, book_id):
        category_id = category_data.get("category_id")
        book = BookModel.query.get_or_404(book_id)
        category = CategoryModel.query.get_or_404(category_id)

        if category in book.categories:
            book.categories.remove(category)
            db.session.commit()

        return book.categories