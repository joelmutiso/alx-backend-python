import time
import sqlite3 
import functools

query_cache = {}

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

def cache_query(func):
    """Decorator to cache query results based on the query string."""
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        # The query string is passed as a keyword argument
        sql_query = kwargs['query']
        
        if sql_query in query_cache:
            return query_cache[sql_query]
        else:
            # Run the original function to fetch the data
            result = func(conn, *args, **kwargs)
            # Store the result in the cache
            query_cache[sql_query] = result
            return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")