from crud_operations.create_student import CreateStudent
from crud_operations.db import create_connection_with_retry, close_connection

RETRIES = 3
DELAY = 5  # seconds

# Initialize the connection as None
conn = None

try:
    # Establish the database connection
    conn = create_connection_with_retry(retries=RETRIES, delay=DELAY)

    if conn is None:
        raise Exception("Database connection failed.")

    # Create an instance of CreateStudent with the existing connection
    create_student_instance = CreateStudent(conn)

    # Create the table
    create_student_instance.create_student_table()

except Exception as e:
    print(f"Error connecting to the database: {e}")

finally:
    # Close the database connection if it was successfully created
    close_connection(conn)
