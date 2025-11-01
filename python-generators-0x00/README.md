# Python Generators - Task 0: Database Seeding

This project contains a Python script, `seed.py`, designed to set up and populate a MySQL database. This serves as the data source for the subsequent generator tasks.

## `seed.py`

This script provides five main functions as specified by the project:

1.  `connect_db()`: Connects to the main MySQL server.
2.  `create_database(connection)`: Creates the `ALX_prodev` database if it doesn't exist.
3.  `connect_to_prodev()`: Connects specifically to the `ALX_prodev` database.
4.  `create_table(connection)`: Creates the `user_data` table if it doesn't exist.
5.  `insert_data(connection, data_file)`: Reads `user_data.csv` and populates the `user_data` table.

## Requirements

* Python 3
* `mysql-connector-python` (Install with `pip install mysql-connector-python`)
* A running MySQL server

## Environment Variables

The script uses the following environment variables for database credentials:

* `DB_HOST`: The database host (default: `localhost`)
* `DB_USER`: The database user (default: `root`)
* `DB_PASS`: The database password (default: *empty*)

## How to Run

1.  Make sure your `0-main.py` file is in the same directory and is executable:
    ```sh
    chmod +x 0-main.py
    ```
2.  Run the main file. It will import `seed.py` and execute the setup.
    ```sh
    ./0-main.py
    ```