from db import db
from associations import book_category


class CategoryModel(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    books = db.relationship('BookModel', secondary=book_category, back_populates='categories')
