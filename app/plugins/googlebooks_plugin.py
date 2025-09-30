import requests
import logging

class GoogleBooksPlugin:
    def run(self, data):
        isbn = data.get('isbn')
        if not isbn:
            logging.warning('ISBN not provided to plugin')
            return {'error': 'ISBN required'}
        url = f'https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}'
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                result = resp.json()
                items = result.get('items', [])
                if not items:
                    return {'error': 'No book found in Google Books'}
                volume = items[0]['volumeInfo']
                title = volume.get('title')
                authors = volume.get('authors', [])
                description = volume.get('description')
                publish_year = volume.get('publishedDate')
                genres = volume.get('categories', [])
                series = None  # Google Books does not provide series info directly
                image_links = volume.get('imageLinks', {})
                cover_url = image_links.get('thumbnail')
                logging.info(f'Parsed book info from Google Books: title={title}, authors={authors}, publish_year={publish_year}, cover_url={cover_url}')
                return {
                    'title': title,
                    'authors': authors,
                    'description': description,
                    'series': series,
                    'publish_year': publish_year,
                    'genres': genres,
                    'cover_url': cover_url
                }
            else:
                logging.warning(f'Google Books API returned {resp.status_code} for ISBN {isbn}')
                return {'error': f'Google Books API returned {resp.status_code}'}
        except Exception as e:
            logging.error(f'Error fetching ISBN {isbn} from Google Books: {e}')
            return {'error': 'Exception during Google Books lookup'}
