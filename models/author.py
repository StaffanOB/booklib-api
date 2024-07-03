from db import db


class AuthorModel(db.Model):
    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=True, nullable=False)
    biography = db.Column(db.Text)
    books = db.relationship("BookModel", back_populates="author", lazy="dynamic")
