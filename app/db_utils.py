"""
Database connection utilities with graceful error handling
"""
import logging
from functools import wraps
from flask import jsonify
from sqlalchemy.exc import OperationalError, DatabaseError
from app import db

logger = logging.getLogger(__name__)

def handle_db_errors(f):
    """
    Decorator to handle database connection errors gracefully
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except OperationalError as e:
            logger.error(f"Database connection error: {e}")
            return jsonify({
                'error': 'Database temporarily unavailable',
                'message': 'The service is experiencing database connectivity issues. Please try again later.',
                'status': 'service_degraded'
            }), 503
        except DatabaseError as e:
            logger.error(f"Database error: {e}")
            return jsonify({
                'error': 'Database error',
                'message': 'A database error occurred. Please try again later.',
                'status': 'service_degraded'
            }), 503
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return jsonify({
                'error': 'Internal server error',
                'message': 'An unexpected error occurred. Please try again later.',
                'status': 'error'
            }), 500
    return decorated_function

def check_db_connection():
    """
    Check if database connection is available
    Returns: (is_connected: bool, error_message: str)
    """
    try:
        # Simple query to test connection
        db.session.execute(db.text('SELECT 1'))
        db.session.commit()
        return True, None
    except OperationalError as e:
        logger.warning(f"Database connection check failed: {e}")
        return False, str(e)
    except Exception as e:
        logger.error(f"Unexpected error during database check: {e}")
        return False, str(e)

def get_health_status():
    """
    Get comprehensive health status including database connectivity
    """
    db_connected, db_error = check_db_connection()
    
    status = {
        'status': 'healthy' if db_connected else 'degraded',
        'database': {
            'connected': db_connected,
            'error': db_error if not db_connected else None
        },
        'timestamp': None
    }
    
    # Add timestamp
    from datetime import datetime, timezone
    status['timestamp'] = datetime.now(timezone.utc).isoformat()
    
    return status