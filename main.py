import psycopg2
from crud_operations.create_student import CreateStudent

db_params = {
    "dbname": "studentdb",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": "5432"
}

conn = None
try:
    # Establish the connection to the PostgreSQL database
    conn = psycopg2.connect(**db_params)

    # Create an instance of CreateStudent with the existing connection
    create_student_instance = CreateStudent(conn)

    # Create the table
    create_student_instance.create_student_table()

except Exception as e:
    print(f"Error connecting to the database: {e}")

finally:
    # Close the database connection after the operations, only if it's established
    if conn:
        conn.close()
        print("Connection closed.")