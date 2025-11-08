import time
import sqlite3 
import functools

def with_db_connection(func):
    """Decorator to handle opening and closing DB connection."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db") 
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close() 
        return result
    return wrapper


def retry_on_failure(retries, delay):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(conn, *args, **kwargs):
            for i in range(retries):
                try:
                    return func(conn, *args, **kwargs)
                except Exception as e:
                    if i == retries - 1:
                        print(f"Final attempt failed. Raising error: {e}")
                        raise
                    
                    print(f"Attempt {i+1} failed. Retrying in {delay}s...")
                    time.sleep(delay)
        return wrapper
    return decorator

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
print(users)