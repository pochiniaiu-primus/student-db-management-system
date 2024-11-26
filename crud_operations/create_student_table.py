from psycopg2 import sql, OperationalError
from tkinter import messagebox
import logging

# Set up logging
logging.basicConfig(filename='app.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class CreateStudent:
    """
    Class to manage the creation of a student table in a PostgreSQL database.
    """

    def __init__(self, db_connection, table_name='students2_1'):
        """
        Initialize the CreateStudent instance.

        Args:
            db_connection: A connection object to the PostgreSQL database.
            table_name (str): The name of the table to create.
        """
        self.connection = db_connection
        self.table_name = table_name

    def create_student_table(self):
        """
        Create the student table in the PostgreSQL database if it doesn't already exist.
        """
        try:
            # Initialize cursor to execute SQL queries
            with self.connection.cursor() as cursor:
                # Construct the SQL query for creating the table.
                create_table_query = sql.SQL("""
                    CREATE TABLE IF NOT EXISTS {table_name} (
                        id SERIAL PRIMARY KEY,
                        name TEXT NOT NULL,
                        address TEXT NOT NULL,
                        age INT NOT NULL CHECK (age >= 0),  -- Ensures age is non-negative.
                        number TEXT NOT NULL
                    );
                """).format(table_name=sql.Identifier(self.table_name))

                # Execute the SQL query to create the table
                cursor.execute(create_table_query)

                # Commit the transaction after executing the query to make the changes persistent.
                self.connection.commit()

                print(f'Table {self.table_name} created or verified successfully.')

        except OperationalError as op_err:
            # Handle operational database errors
            logging.error(f'Operational error while creating table {self.table_name}: {op_err}')
            messagebox.showerror('Database Error', f'Operational error: {op_err}')
            self.connection.rollback()

        except Exception as e:
            # Handle unexpected errors
            logging.error(f'Error creating table {self.table_name}: {e}')
            messagebox.showerror('Database Error,' f"Error creating table: {e}")
            self.connection.rollback()  # Rollback in case of error
