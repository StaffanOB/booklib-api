from models import BookModel, authorModel, CategoryModel
from db import db


def add_book_with_authors_and_categories(book_title, author_names, category_names):
    book = BookModel(title=book_title)

    # Retrieve or create authors by name
    authors = []
    for name in author_names:
        author = authorModel.query.filter_by(name=name).first()
        if not author:
            author = authorModel(name=name)
        authors.append(author)

    # Retrieve or create categories by name
    categories = []
    for name in category_names:
        category = CategoryModel.query.filter_by(name=name).first()
        if not category:
            category = CategoryModel(name=name)
        categories.append(category)

    # Associate authors and categories with the book
    book.authors = authors
    book.categories = categories

    # add the book with its relationships to the session and commit
    try:
        db.session.add(book)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
    finally:
        db.session.close()

    return book
