import psycopg2
from psycopg2 import sql
from tkinter import messagebox
import logging

logging.basicConfig(level=logging.INFO)


class UpdateStudent:

    def __init__(self, db_connection, table_name='students2_1'):
        self.connection = db_connection
        self.table_name = table_name

    def update_all_student_fields(self, student_id, name, address, age, number):
        """ Update the fields of a student record identified by their student_id.
        This method updates the name, address, age, and number of a student.
        """
        try:
            # Initialize a cursor to interact with the database
            cursor = self.connection.cursor()

            # Construct the update query
            update_query = sql.SQL("""
                 UPDATE {table_name} 
                 SET name = %s, address = %s, age = %s, number = %s
                 WHERE id = %s 
                    """).format(table_name=sql.Identifier(self.table_name))

            # Execute the query with the parameters
            cursor.execute(update_query, (name, address, age, number, student_id))

            # Check if the student was updated
            if cursor.rowcount > 0:
                logging.info(f'Student woth ID {student_id} updated successfully.')
                messagebox.showinfo('Success',
                                    f'Student with ID {student_id} updated successfully.')
            else:
                logging.warning(f'Student with ID {student_id} not found.')
                messagebox.showwarning('Not Found', f'Student with ID {student_id} not found.')

            # Commit the transaction to make sure the data is saved to the database
            self.connection.commit()

            print("Data updated successfully.")

        except psycopg2.Error as e:
            logging.error(f'Database error: {e}')
            self.connection.rollback()
            messagebox.showerror('Database Error', f'Could not update student: {e}')

        finally:
            # Close the cursor
            cursor.close()

    def find_student_by_id(self, student_id):
        """Check if a student exists by ID."""
        query = sql.SQL("""
            SELECT id FROM {table_name}
            WHERE id = %s
        """).format(table_name=sql.Identifier(self.table_name))
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, (student_id,))
                return cursor.fetchone() is not None

        except psycopg2.Error as e:
            # Handle errors and rollback transaction if necessary
            self.connection.rollback()
            messagebox.showerror('Database Error', f'Could not fetch student: {e}')
            logging.error(f'Database error: {e}')
            return False
