from app import db

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)

class BookAuthor(db.Model):
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), primary_key=True)
