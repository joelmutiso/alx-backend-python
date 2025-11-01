from seed import connect_to_prodev
import mysql.connector

def stream_users():
    """
    Fetches rows one by one from the user_data table.
    Yields each row as a dictionary.
    """
    connection = None
    cursor = None
    try:
        connection = connect_to_prodev()
        if connection is None:
            print("Could not connect to database.")
            return

        # The key: dictionary=True makes the cursor return
        # dicts instead of tuples, matching the main file's output.
        cursor = connection.cursor(dictionary=True)
        
        query = "SELECT * FROM user_data;"
        cursor.execute(query)

        # This is the single loop.
        # The cursor itself is an iterator. It fetches
        # rows from the database one by one as the loop asks.
        for row in cursor:
            yield row

    except mysql.connector.Error as e:
        print(f"Database Error: {e}")
    finally:
        # This part is crucial!
        # It ensures the connection is closed no matter what.
        if cursor:
            cursor.close()
        if connection:
            connection.close()