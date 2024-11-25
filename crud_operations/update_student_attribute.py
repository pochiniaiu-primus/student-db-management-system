import logging
from tkinter import messagebox

import psycopg2
from psycopg2 import sql

logging.basicConfig(level=logging.INFO)


class UpdateStudentAttribute:
    """
    Provides methods for updating specific student attributes in the database.
    """

    def __init__(self, db_connection, table_name='students2_1'):
        """
        Initialize the UpdateStudentAttribute class.
        Args:
            db_connection: Active connection to the PostgreSQL database.
            table_name (str): Name of the student records table.
        """
        self.connection = db_connection
        self.table_name = table_name

    def update_student_field(self, student_id: int, field_choice: str, value):
        """
        Update a specific field of a student record in the database.

        Args:
            student_id (int): ID of the student to update.
            field_choice (str): Field to be updated ('name', 'address', 'age', 'number').
            value: New value for the field.
        """
        valid_fields = ['name', 'address', 'age', 'number']

        if field_choice not in valid_fields:
            logging.error(f'Invalid field choice: {field_choice}')
            messagebox.showerror('Error', f'Invalid field: {field_choice}. Please choose a valid field.')
            return

        try:
            # Prepare SQL query to update the selected field
            query = sql.SQL("""
                UPDATE {table_name}
                SET {field} = %s
                WHERE id = %s
            """).format(
                table_name=sql.Identifier(self.table_name),
                field=sql.Identifier(field_choice)
            )

            # Execute the query
            with self.connection.cursor() as cursor:
                cursor.execute(query, (value, student_id))

                # Commit the transaction to make sure the data is saved to the database
                self.connection.commit()

                # Provide feedback to the user
                if cursor.rowcount > 0:
                    logging.info(f'{field_choice.capitalize()} updated successfully for student with ID: {student_id}.')
                    messagebox.showinfo('Success', f'{field_choice.capitalize()} updated successfully!')
                else:
                    logging.warning(f'No student found with ID {student_id}.')
                    messagebox.showerror('Error', f'Student with ID {student_id} not found.')

        except psycopg2.Error as e:
            logging.error(f'Database error during update: {e}')
            self.connection.rollback()
            messagebox.showerror('Database Error', f'Could not update student attribute: {e}')

    def find_student_by_id(self, student_id: int) -> bool:
        """
        Check if a student exists by ID.

        Args:
            student_id (int): The student's ID.

        Returns:
            bool: True if the student exists, False otherwise.
        """
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
            logging.error(f'Error checking student existence: {e}')
            self.connection.rollback()
            messagebox.showerror('Database Error', f'Could not check student ID: {e}')
            return False
