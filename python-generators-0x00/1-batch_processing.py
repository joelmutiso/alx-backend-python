import mysql.connector
from mysql.connector import Error, errorcode
import os

# Get credentials from environment variables
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASS = os.getenv('DB_PASS', '')
DB_NAME = 'ALX_prodev'


def stream_users_in_batches(batch_size=1000):
    """
    A generator that connects to the user_data table
    and yields rows in batches (lists) of a specified size.
    """
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME
        )
        
        # Use a buffered, dictionary cursor
        cursor = connection.cursor(dictionary=True, buffered=True)
        
        query = "SELECT user_id, name, email, age FROM user_data"
        cursor.execute(query)
        
        batch = []
        # --- LOOP 1: Iterates over all rows in the database ---
        for row in cursor:
            batch.append(row)
            if len(batch) == batch_size:
                yield batch
                batch = []  # Reset the batch
        
        # Yield any remaining users in the last batch
        if batch:
            yield batch
            
    except Error as e:
        if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif e.errno == errorcode.ER_BAD_DB_ERROR:
            print(f"Database {DB_NAME} does not exist")
        else:
            print(f"Error while streaming: {e}")
    finally:
        # Ensure resources are closed
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def batch_processing(batch_size):
    """
    Fetches user batches and processes them.
    Filters users to find those over 25 and prints them.
    """
    # --- LOOP 2: Iterates over the batches (lists) from the generator ---
    for batch in stream_users_in_batches(batch_size):
        
        # --- LOOP 3: Iterates over users (dictionaries) in a single batch ---
        for user in batch:
            # Process: filter users over the age of 25
            if user['age'] > 25:
                # The main script expects this to be printed
                print(user)