from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from models import CategoryModel
from schemas import CategorySchema, CategoryUpdateSchema
from sqlalchemy.exc import SQLAlchemyError

blp = Blueprint("Categories", "categories",
                description="Operations on categories")


@blp.route("/categories")
class CategoryList(MethodView):
    @blp.response(200, CategorySchema(many=True))
    def get(self):
        return CategoryModel.query.all()

    @blp.arguments(CategorySchema)
    @blp.response(201, CategorySchema)
    def post(self, category_data):
        category = CategoryModel(**category_data)
        try:
            db.session.add(category)
            db.session.commit()
        except SQLAlchemyError:
            abort(500,
                  message="An error occurred while inserting the category.")
        return category


@blp.route("/category/<int:category_id>")
class Category(MethodView):
    ''' Operations on a single category '''
    @blp.response(200, CategorySchema)
    def get(self, category_id):
        return CategoryModel.query.get_or_404(category_id)

    @blp.arguments(CategoryUpdateSchema)
    @blp.response(200, CategorySchema)
    def put(self, category_data, category_id):
        category = CategoryModel.query.get_or_404(category_id)
        if category:
            category.name = category_data.get("name", category.name)
            db.session.commit()
        return category

    @blp.response(200)
    def delete(self, category_id):
        category = CategoryModel.query.get_or_404(category_id)
        db.session.delete(category)
        db.session.commit()
        return {"message": "Category deleted"}
