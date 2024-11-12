import time

import psycopg2

db_params = {
    "dbname": "studentdb",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": "5432"
}


def create_connection():
    """Create a database connection to the PostgreSQL database."""
    try:
        connection = psycopg2.connect(**db_params)
        print("Connection to PostgreSQL established.")
        return connection

    except Exception as error:
        print(f"Error: Unable to connect to the database\n{error}")
        return None


def close_connection(conn):
    """Close the database connection."""
    if conn:
        try:
            conn.close()
            print("Connection closed.")
        except Exception as e:
            print(f"Error while closing connection: {e}")


def create_connection_with_retry(retries=3, delay=5):
    """Attempt to create a connection with retries."""
    for _ in range(retries):
        conn = create_connection()
        if conn:
            return conn
        print(f'Retrying in {delay} seconds...')
        time.sleep(delay)
    print("Failed to establish a connection after several retries.")
    return None
