import sqlite3

class ExecuteQuery:
    def __init__(self, db_name, query, params=()):
        self.db_name = db_name
        self.query = query
        self.params = params
        self.conn = None # Initialize connection as None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        cursor = self.conn.cursor()
        cursor.execute(self.query, self.params)
        results = cursor.fetchall()
        return results

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Clean up: always close the connection.
        """
        if self.conn:
            self.conn.close()

# --- Using the Context Manager ---
print("--- Executing Context Manager ---")

# The query and parameters as requested
sql_query = "SELECT * FROM users WHERE age > ?"
query_params = (25,) # Note: (25,) is a tuple, which sqlite3 requires
DB_FILE = 'users.db' # Define the database file to use

try:
    with ExecuteQuery(DB_FILE, sql_query, query_params) as results:
        # 'results' here is the list returned from __enter__
        print("Query successful. Results:")
        for row in results:
            print(row)

except sqlite3.OperationalError as e:
    # This will likely fail if the 'users.db' file and 'users' table don't exist
    print(f"Query failed: {e}")