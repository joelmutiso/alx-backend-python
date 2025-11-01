import mysql.connector
from mysql.connector import Error, errorcode
import os
from decimal import Decimal  # Import Decimal to handle DECIMAL type from SQL

# Get credentials from environment variables
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASS = os.getenv('DB_PASS', '')
DB_NAME = 'ALX_prodev'


def stream_user_ages():
    """
    Generator that yields user ages one by one from the database.
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
        # Use dictionary=True to access by column name 'age'
        # Use buffered=True to fetch all results
        cursor = connection.cursor(dictionary=True, buffered=True)
        
        # Optimization: Only select the 'age' column
        query = "SELECT age FROM user_data"
        cursor.execute(query)
        
        # Loop 1: Iterate over cursor and yield ages
        for row in cursor:
            yield row['age']  # This will be a Decimal object
            
    except Error as e:
        if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif e.errno == errorcode.ER_BAD_DB_ERROR:
            print(f"Database {DB_NAME} does not exist")
        else:
            print(f"Error while streaming: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
    
    return


def calculate_average_age():
    """
    Calculates the average age by iterating over the stream_user_ages generator.
    """
    # Initialize as Decimal objects for precision
    total_age = Decimal(0)
    user_count = 0
    
    # Loop 2: Iterate over the generator
    for age in stream_user_ages():
        total_age += age  # Decimal arithmetic
        user_count += 1
        
    if user_count == 0:
        return Decimal(0)  # Avoid division by zero
        
    # Division will also be Decimal
    average = total_age / Decimal(user_count)
    return average


if __name__ == "__main__":
    # This block runs when the script is executed directly
    
    avg = calculate_average_age()
    
    # Print in the requested format, rounding to 2 decimal places for clean output
    print(f"Average age of users: {avg:.2f}")