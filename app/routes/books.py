from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Book, Comment, Rating, Author
import logging
import os

books_bp = Blueprint('books', __name__)

LOG_DIR = os.path.join(os.path.dirname(__file__), '..', 'logs')
LOG_PATH = os.path.join(LOG_DIR, 'app.log')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

logging.basicConfig(
    level=logging.DEBUG,  # Changed to DEBUG
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
    handlers=[
        logging.FileHandler(LOG_PATH),
        logging.StreamHandler()
    ]
)

@books_bp.route('/books', methods=['GET'])
def get_books():
    """Get all books
    ---
    tags:
      - Books
    """
    books = Book.query.all()
    return jsonify([
        {
            'id': b.id,
            'title': b.title,
            'authors': [a.name for a in b.authors],
            'description': b.description,
            'publish_year': b.publish_year,
            'series': b.series
        } for b in books
    ]), 200

@books_bp.route('/books/<int:id>/full', methods=['GET'])
def get_book_full(id):
    """Get book info, ratings, and comments
    ---
    tags:
      - Books
    """
    book = Book.query.get_or_404(id)
    ratings = Rating.query.filter_by(book_id=id).all()
    comments = Comment.query.filter_by(book_id=id).all()
    avg_rating = None
    if ratings:
        avg_rating = sum(r.rating for r in ratings) / len(ratings)
    return jsonify({
        'id': book.id,
        'title': book.title,
        'author': ', '.join([a.name for a in book.authors]),
        'description': book.description,
        'publish_year': book.publish_year,
        'series': book.series,
        'cover_url': book.cover_url,
        'average_rating': avg_rating,
        'ratings': [{'id': r.id, 'user_id': r.user_id, 'rating': r.rating} for r in ratings],
        'comments': [{'id': c.id, 'user_id': c.user_id, 'content': c.content} for c in comments]
    }), 200


# Add new book endpoint
@books_bp.route('/books', methods=['POST'])
@jwt_required()
def add_book():
    """Add a new book
    ---
    tags:
      - Books
    """
    from app.plugin_loader import load_plugins
    from app.models import Tag, BookTag
    data = request.get_json()
    isbn = data.get('isbn')

    # Ensure default author exists
    default_author = Author.query.filter_by(name='No Author').first()
    if not default_author:
        default_author = Author(name='No Author')
        db.session.add(default_author)
        db.session.commit()

    author_ids = []
    from app.plugin_loader import load_plugins
    plugins = load_plugins()
    plugin_name = data.get('plugin', 'GoogleBooksPlugin')
    if plugin_name == 'GoodreadsPlugin':
        plugin_name = 'OpenLibraryPlugin'
    plugin = plugins.get(plugin_name)
    gr_data = None
    if isbn and plugin:
        gr_data = plugin.run({'isbn': isbn})
        logging.debug(f'Enriched data from plugin {plugin_name} for ISBN {isbn}: {gr_data}')
        if 'error' not in gr_data:
            data['title'] = gr_data.get('title', data.get('title', ''))
            data['description'] = gr_data.get('description', data.get('description', ''))
            data['series'] = gr_data.get('series', data.get('series', ''))
            
            # Handle publish_year - extract year from date string if needed
            publish_year_raw = gr_data.get('publish_year', data.get('publish_year'))
            if publish_year_raw:
                if isinstance(publish_year_raw, str):
                    # Extract year from date string like "2016-10-18"
                    try:
                        data['publish_year'] = int(publish_year_raw.split('-')[0])
                    except (ValueError, IndexError):
                        data['publish_year'] = None
                else:
                    data['publish_year'] = publish_year_raw
            else:
                data['publish_year'] = None
                
            data['tags'] = gr_data.get('genres', data.get('tags', []))
            # Handle authors
            author_names = gr_data.get('authors', [])
            author_ids = []
            for name in author_names:
                author = Author.query.filter_by(name=name).first()
                if not author:
                    author = Author(name=name)
                    db.session.add(author)
                    db.session.commit()
                author_ids.append(author.id)
    
    # Handle authors from request data if no plugin authors found
    if not author_ids:
        author_names = data.get('authors', [])
        for name in author_names:
            if name and name.strip():
                author = Author.query.filter_by(name=name.strip()).first()
                if not author:
                    author = Author(name=name.strip())
                    db.session.add(author)
                    db.session.commit()
                author_ids.append(author.id)
    # If no author found, use default
    if not author_ids:
        author_ids = [default_author.id]
    if not data or not data.get('title'):
        return jsonify({'msg': 'Missing title'}), 400
    # Check for at least one author
    if not author_ids:
        return jsonify({'msg': 'Missing author'}), 400
    if not data['title'].strip():
        return jsonify({'msg': 'Title cannot be empty'}), 400
    # Check for duplicate book with same title and authors
    existing_books = Book.query.filter_by(title=data['title']).all()
    for book in existing_books:
        book_author_ids = set(a.id for a in book.authors)
        if set(author_ids) == book_author_ids:
            return jsonify({'msg': 'Author and book already exist'}), 400
    # Check for duplicate ISBN
    isbn_value = data.get('isbn')
    if isbn_value:
        existing_books = Book.query.filter_by(isbn=isbn_value).all()
        if existing_books:
            book = existing_books[0]
            author_names = ', '.join([a.name for a in book.authors])
            return jsonify({'msg': f'ISBN already exist. It belongs to {author_names}, {book.title}'}), 400
    book = Book(
        title=data['title'],
        isbn=isbn_value,
        description=data.get('description', ''),
        publish_year=data.get('publish_year'),
        series=data.get('series'),
        cover_url=gr_data.get('cover_url') if gr_data and 'cover_url' in gr_data else data.get('cover_url')
    )
    db.session.add(book)
    db.session.commit()
    # Link authors to book
    for author_id in author_ids:
        author = Author.query.get(author_id)
        if author and author not in book.authors:
            book.authors.append(author)
    db.session.commit()
    # Add tags (genres) if present
    tag_names = data.get('tags', [])
    for tag_name in tag_names:
        clean_tag = tag_name.strip() if isinstance(tag_name, str) else str(tag_name)
        if not clean_tag:
            continue
        tag = Tag.query.filter_by(name=clean_tag).first()
        if not tag:
            tag = Tag(name=clean_tag)
            db.session.add(tag)
            db.session.commit()
        if tag not in book.tags:
            book.tags.append(tag)
    # If enriched genres exist, add them as tags
    if gr_data and 'genres' in gr_data and gr_data['genres']:
        for genre in gr_data['genres']:
            clean_genre = genre.strip() if isinstance(genre, str) else str(genre)
            if not clean_genre:
                continue
            tag = Tag.query.filter_by(name=clean_genre).first()
            if not tag:
                tag = Tag(name=clean_genre)
                db.session.add(tag)
                db.session.commit()
            if tag not in book.tags:
                book.tags.append(tag)
    db.session.commit()
    return jsonify({'id': book.id, 'title': book.title}), 201

# Get book by ID endpoint
@books_bp.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    """Get a book by ID
    ---
    tags:
      - Books
    """
    book = Book.query.get_or_404(id)
    return jsonify({
        'id': book.id,
        'title': book.title,
        'author': ', '.join([a.name for a in book.authors]),
        'description': book.description,
        'publish_year': book.publish_year,
        'series': book.series,
        'cover_url': book.cover_url
    }), 200

# Update book endpoint
@books_bp.route('/books/<int:id>', methods=['PUT'])
@jwt_required()
def update_book(id):
    """Update a book
    ---
    tags:
      - Books
    """
    book = Book.query.get_or_404(id)
    data = request.get_json()
    if not data:
        return jsonify({'msg': 'No data provided'}), 400
    if 'title' in data:
        if not data['title'].strip():
            return jsonify({'msg': 'Title cannot be empty'}), 400
        book.title = data['title']
    if 'author' in data:
        author_names = data['author']
        if isinstance(author_names, str):
            author_names = [author_names]
        author_names = [name.strip() for name in author_names if name.strip()]
        if not author_names:
            return jsonify({'msg': 'Author cannot be empty'}), 400
        book.authors.clear()
        for name in author_names:
            author = Author.query.filter_by(name=name).first()
            if not author:
                author = Author(name=name)
                db.session.add(author)
                db.session.commit()
            book.authors.append(author)
    if 'description' in data:
        book.description = data['description']
    if 'publish_year' in data:
        # Handle publish_year - extract year from date string if needed
        publish_year_raw = data['publish_year']
        if publish_year_raw:
            if isinstance(publish_year_raw, str):
                try:
                    book.publish_year = int(publish_year_raw.split('-')[0])
                except (ValueError, IndexError):
                    book.publish_year = None
            else:
                book.publish_year = publish_year_raw
        else:
            book.publish_year = None
    if 'series' in data:
        book.series = data['series']
    db.session.commit()
    return jsonify({'msg': 'Book updated'}), 200

# Delete book endpoint
@books_bp.route('/books/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_book(id):
        """Delete a book
        ---
        tags:
            - Books
        """
        book = Book.query.get_or_404(id)
        db.session.delete(book)
        db.session.commit()
        return jsonify({'msg': 'Book deleted'}), 200

@books_bp.route('/books/<int:id>/recheck', methods=['POST'])
@jwt_required()
def recheck_book_info(id):
    """Recheck and update book info by ID
    ---
    tags:
      - Books
    """
    from app.plugin_loader import load_plugins
    from app.models import Author, Tag
    book = Book.query.get_or_404(id)
    data = request.get_json() or {}
    isbn = book.isbn
    plugin_name = data.get('plugin', 'GoogleBooksPlugin')
    plugins = load_plugins()
    if plugin_name == 'GoodreadsPlugin':
        plugin_name = 'OpenLibraryPlugin'
    plugin = plugins.get(plugin_name)
    if not plugin:
        return jsonify({'msg': f'Plugin {plugin_name} not found'}), 400
    if not isbn:
        return jsonify({'msg': 'Book does not have an ISBN'}), 400
    gr_data = plugin.run({'isbn': isbn})
    logging.debug(f'Rechecked data from plugin {plugin_name} for ISBN {isbn}: {gr_data}')
    if 'error' in gr_data:
        return jsonify({'msg': gr_data['error']}), 400
    # Update book fields
    book.title = gr_data.get('title', book.title)
    book.description = gr_data.get('description', book.description)
    book.series = gr_data.get('series', book.series)
    
    # Handle publish_year - extract year from date string if needed
    publish_year_raw = gr_data.get('publish_year', book.publish_year)
    if publish_year_raw and publish_year_raw != book.publish_year:
        if isinstance(publish_year_raw, str):
            try:
                book.publish_year = int(publish_year_raw.split('-')[0])
            except (ValueError, IndexError):
                pass  # Keep existing value if parsing fails
        else:
            book.publish_year = publish_year_raw
    # Update tags from enriched genres
    if gr_data.get('genres'):
        for genre in gr_data['genres']:
            clean_genre = genre.strip() if isinstance(genre, str) else str(genre)
            if not clean_genre:
                continue
            tag = Tag.query.filter_by(name=clean_genre).first()
            if not tag:
                tag = Tag(name=clean_genre)
                db.session.add(tag)
                db.session.commit()
            if tag not in book.tags:
                book.tags.append(tag)
    # Update authors
    author_names = gr_data.get('authors', [])
    book.authors.clear()
    for name in author_names:
        author = Author.query.filter_by(name=name).first()
        if not author:
            author = Author(name=name)
            db.session.add(author)
            db.session.commit()
        book.authors.append(author)
    db.session.commit()
    return jsonify({'msg': 'Book info rechecked and updated', 'id': book.id, 'title': book.title}), 200
