import sqlite3 
import functools

def with_db_connection(func):
    """Decorator to handle opening and closing DB connection."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db") 
        try:
            result = func(conn, *args, **kwargs) # pass conn to wrapped function
        finally:
            conn.close() # ensure connection is always closed
        return result
    return wrapper

def transactional(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
        except Exception:
            conn.rollback()
            raise
        else:
            conn.commit()
            return result
    return wrapper

@with_db_connection 
@transactional 
def update_user_email(conn, user_id, new_email): 
    cursor = conn.cursor() 
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id)) 

#### Update user's email with automatic transaction handling 
update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')