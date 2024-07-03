from db import db


class BookModel(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey(
        "authors.id"), nullable=False)
    author = db.relationship("AuthorModel", back_populates="books")
    categories = db.relationship("BookCategoryModel", back_populates="book")
