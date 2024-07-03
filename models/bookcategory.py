from db import db
'''
Defines a many-to-many relationship between books and categories., including a
flag to indicate if a category is the primary category of a book.
'''


class BookCategoryModel(db.Model):
    __tablename__ = 'bookcategory'

    book_id = db.Column(db.Integer, db.ForeignKey(
        'books.id'), primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey(
        'categories.id'), primary_key=True)
    is_primary = db.Column(db.Boolean, default=False, nullable=False)
    book = db.relationship('BookModel', back_populates='categories')
    category = db.relationship('CategoryModel', back_populates='books')
