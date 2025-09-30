from app import db

class BookTag(db.Model):
    __tablename__ = "book_tags"
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey("tag.id"), primary_key=True)
