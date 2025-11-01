import mysql.connector
from mysql.connector import Error, errorcode
import os
import csv
import uuid 

# --- Database Credentials ---
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASS = os.getenv('DB_PASS', '')
DB_NAME = 'ALX_prodev'


def connect_db():
    """Connects to the MySQL database server."""
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS
        )
        return connection
    except Error as e:
        if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        else:
            print(f"Error connecting to MySQL server: {e}")
        return None


def create_database(connection):
    """Creates the database ALX_prodev if it does not exist."""
    try:
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME};")
        cursor.close()
    except Error as e:
        print(f"Error creating database: {e}")


def connect_to_prodev():
    """Connects to the ALX_prodev database in MYSQL."""
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME
        )
        return connection
    except Error as e:
        if e.errno == errorcode.ER_BAD_DB_ERROR:
            print(f"Database {DB_NAME} does not exist.")
        else:
            print(f"Error connecting to database {DB_NAME}: {e}")
        return None


def create_table(connection):
    """Creates a table user_data if it does not exist."""
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL(3, 0) NOT NULL
        );
        """
        cursor.execute(create_table_query)
        print("Table user_data created successfully")
        cursor.close()
    except Error as e:
        print(f"Error creating table: {e}")


def insert_data(connection, data_file):
    """
    Inserts data from a 3-COLUMN CSV file (name, email, age)
    and generates a UUID for the user_id.
    """
    try:
        cursor = connection.cursor()
        
        insert_query = """
        INSERT IGNORE INTO user_data (user_id, name, email, age)
        VALUES (%s, %s, %s, %s);
        """
        
        data_to_insert = []
        with open(data_file, mode='r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip header
            
            for row in csv_reader:
                try:
                    if row: 
                        # row[0] is name, row[1] is email, row[2] is age
                        user_id = str(uuid.uuid4()) # Generate the missing user_id
                        name = row[0]
                        email = row[1]
                        age = int(row[2])
                        
                        # Add the 4-column tuple
                        data_to_insert.append((user_id, name, email, age))
                except (ValueError, IndexError):
                    # This will catch rows with missing age, etc.
                    print(f"Skipping malformed row: {row}")

        if data_to_insert:
            cursor.executemany(insert_query, data_to_insert)
            connection.commit()
        
        cursor.close()

    except Error as e:
        print(f"Error inserting data: {e}")
        connection.rollback()
    except FileNotFoundError:
        print(f"Error: The file {data_file} was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        connection.rollback()