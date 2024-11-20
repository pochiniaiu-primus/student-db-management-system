import psycopg2
from tkinter import messagebox


class StudentDataReader:
    """
    Class for querying and fetching student data from the database.
    """

    def __init__(self, db_connection, table_name='students2_1'):
        """
        Initialize with a database connection and table name.
        Args:
            db_connection: Active database connection.
            table_name (str): Name of the database table.
        """
        self.connection = db_connection
        self.table_name = table_name  # Stores the name of the table from which the data will be fetched.

    def fetch_records(self):
        """Retrieve all records from the table in the database"""
        try:
            # Initialize a cursor to interact with the database
            cursor = self.connection.cursor()

            # Execute the SQL query to retrieve all rows in the table
            cursor.execute(f"SELECT * FROM {self.table_name};")

            # Fetch all results from the query
            students = cursor.fetchall()
            return students

        except psycopg2.DatabaseError as error:
            messagebox.showerror('Database Error', f'Failed to fetch records: {error}')
            return []

        finally:
            # Close the cursor
            cursor.close()
