import mysql.connector
from mysql.connector import Error, errorcode
import os

# Get credentials from environment variables
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASS = os.getenv('DB_PASS', '')
DB_NAME = 'ALX_prodev'


def stream_users():
    """
    A generator that connects to the user_data table
    and yields rows one by one as dictionaries.
    """
    connection = None
    cursor = None
    try:
        # Connect to the database
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME
        )
        
        # Add buffered=True to fetch all results at once
        # This prevents the "Unread result" error when islice stops early
        cursor = connection.cursor(dictionary=True, buffered=True)
        
        # Define the query
        query = "SELECT user_id, name, email, age FROM user_data"
        
        # Execute the query
        cursor.execute(query)
        
        # Iterate over the buffered results
        for row in cursor:
            yield row
            
    except Error as e:
        # Handle potential errors
        if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif e.errno == errorcode.ER_BAD_DB_ERROR:
            print(f"Database {DB_NAME} does not exist")
        else:
            print(f"Error while streaming: {e}")
    finally:
        # This block is crucial.
        if cursor:
            cursor.close()
        if connection:
            connection.close()