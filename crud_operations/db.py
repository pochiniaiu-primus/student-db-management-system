import time
import os
from tkinter import messagebox
import logging

import psycopg2

# Set up logging to log errors to a file
logging.basicConfig(filename='app.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Get database connection parameters from environment variables
try:
    db_params = {
        "dbname": os.environ["DBNAME"],
        "user": os.environ["USER"],
        "password": os.environ["PASSWORD"],
        "host": os.environ["HOST"],
        "port": os.environ["PORT"]
    }
except KeyError as e:
    logging.error(f'Missing environment variable: {e}')
    raise Exception(f'Missing environment variable: {e}')


def create_connection():
    """Create a database connection to the PostgreSQL database."""
    try:
        # Establishing connection using the predefined parameters
        connection = psycopg2.connect(**db_params)
        print("Connection to PostgreSQL established.")
        return connection
    except Exception as error:
        logging.error(f"Error: Unable to connect to the database\n{error}")
        return None


def close_connection(conn):
    """Close the database connection."""
    # Check if the conn variable is not None.
    if conn:
        try:
            conn.close()
            print("Connection closed.")
        except Exception as e:
            logging.error(f"Error while closing connection: {e}")


def create_connection_with_retry(retries=3, delay=5):
    """Attempt to create a connection with retries."""
    for _ in range(retries):
        conn = create_connection()
        if conn:
            return conn
        print(f'Retrying in {delay} seconds...')
        time.sleep(delay)
    logging.error("Failed to establish a connection after several retries.")
    messagebox.showerror("Database Connection", "Failed to connect to the database. Exiting.")
    return None
