from app import db

class BookTag(db.Model):
    __tablename__ = "book_tags"
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), primary_key=True)
