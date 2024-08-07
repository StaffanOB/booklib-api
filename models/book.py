from db import db
from associations import book_author, book_category


class BookModel(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    authors = db.relationship(
        'AuthorModel', secondary=book_author, back_populates='books')
