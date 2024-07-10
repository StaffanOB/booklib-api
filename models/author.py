from db import db
from associations import book_author


class AuthorModel(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    books = db.relationship(
        'BookModel', secondary=book_author, back_populates='authors')
