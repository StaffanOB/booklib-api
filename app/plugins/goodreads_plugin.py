import os
import requests
import json
import logging

class OpenLibraryPlugin:
    def run(self, data):
        isbn = data.get('isbn')
        if not isbn:
            logging.warning('ISBN not provided to plugin')
            return {'error': 'ISBN required'}
        url = f'https://openlibrary.org/isbn/{isbn}.json'
        headers = {'User-Agent': 'BookLibAPI/1.0 (contact: your@email.com)'}
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            if resp.status_code == 200:
                record = resp.json()
                return self._parse_record(record)
            else:
                logging.warning(f'Open Library API returned {resp.status_code} for ISBN {isbn}')
                return {'error': f'Open Library API returned {resp.status_code}'}
        except Exception as e:
            logging.error(f'Error fetching ISBN {isbn} from Open Library: {e}')
            return {'error': 'Exception during Open Library lookup'}

    def _parse_record(self, record):
        title = record.get('title')
        author_ids = []
        author_names = []
        if 'authors' in record and isinstance(record['authors'], list):
            for a in record['authors']:
                if 'key' in a:
                    author_url = f'https://openlibrary.org{a["key"]}.json'
                    try:
                        resp = requests.get(author_url, headers={'User-Agent': 'BookLibAPI/1.0'}, timeout=5)
                        if resp.status_code == 200:
                            author_data = resp.json()
                            author_names.append(author_data.get('name', ''))
                    except Exception:
                        continue
        description = record.get('description')
        if isinstance(description, dict):
            description = description.get('value')
        series = record.get('series')
        if isinstance(series, list):
            series = series[0]
        publish_year = record.get('publish_date')
        genres = record.get('subjects', [])
        logging.info(f'Parsed book info from API: title={title}, authors={author_names}, series={series}, publish_year={publish_year}')
        return {
            'title': title,
            'authors': author_names,
            'description': description,
            'series': series,
            'publish_year': publish_year,
            'genres': genres
        }
