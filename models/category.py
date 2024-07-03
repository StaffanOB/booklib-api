from db import db
'''
Define a category with a unique name for the categories table in the database.
'''


class CategoryModel(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    books = db.relationship('BookCategoryModel', back_populates='category')
