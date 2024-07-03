from flask_smorest import Blueprint, abort
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import BookModel, CategoryModel, BookCategoryModel
from schemas import CategorySchema, CategoryUpdateSchema, BookSchema

blp = Blueprint("categories", "categories",
                description="Operations on categories")


@blp.route("/category")
class CategoryList(MethodView):
    @blp.response(200, CategorySchema(many=True))
    def get(self):
        """List all categories"""
        categories = CategoryModel.query.all()
        return categories

    @blp.arguments(CategorySchema)
    @blp.response(201, CategorySchema)
    def post(self, category_data):
        """Create a new category"""
        category = CategoryModel(**category_data)
        db.session.add(category)
        db.session.commit()
        return category, 201


@blp.route("/book/<int:book_id>/categories")
class BookCategories(MethodView):
    @blp.response(200, BookSchema(many=True))
    def get(self, category_id):
        book_categories = BookCategoryModel.query.filter_by(
            book_id=category_id).all()
        categories = [book_category.book for book_category in book_categories]
        return categories

    @blp.arguments(CategorySchema)
    @blp.response(201, CategorySchema)
    def post(self, book_id, category_data):
        book = BookModel.query.get_or_404(book_id)
        category = CategoryModel.query.get(category_data["id"])

        if not category:
            abort(404, message="Category not found")
            db.session.add(category)

        book_category = BookCategoryModel(
            book_id=book.id, category_id=category.id)
        db.session.add(book_category)
        db.session.commit()
        return book_category, 201

    @blp.arguments(CategoryUpdateSchema)
    def put(self, category_data, book_id):
        book = BookModel.query.get_or_404(book_id)
        category = CategoryModel.query.get(category_data["id"])

        book_category = BookCategoryModel.query.filter_by(
            book_id=book.id, category_id=category.id).first()
        if book_category:
            book_category.is_primary = category_data.get(
                "is_primary", book_category.is_primary)
        else:
            book_category = BookCategoryModel(
                book_id=book.id, category_id=category.id, is_primary=category_data.get("is_primary", False))
            db.session.add(book_category)
        db.session.commit()
        return book_category

    def delete(self, book_id, category_id):
        book_category = BookCategoryModel.query.filter_by(
            book_id=book_id, category_id=category_id).first()
        if not book_category:
            abort(404, message="Book category not found")
        db.session.delete(book_category)
        db.session.commit()
        return {"message": "Book category deleted"}, 204
