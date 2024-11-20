from tkinter import messagebox

from psycopg2 import sql


class DeleteStudent:
    """
    Class to handle the deletion of a student record from the database.
    """

    def __init__(self, db_connection, table_name='students2_1'):
        """
        Initialize with a database connection and table name.
        Args:
            db_connection: Active database connection.
            table_name (str): Name of the database table.
        """
        self.connection = db_connection
        self.table_name = table_name  # Table name for deleting records

    def delete_student(self, student_id):
        """
        Delete a student record from the database by ID.
        Args:
            student_id (int): ID of the student to delete.
        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        try:
            with self.connection.cursor() as cursor:
                # Check if the student exists in the database
                find_student_query = sql.SQL("""
                             SELECT id FROM {table_name}
                             WHERE id = %s
                                """).format(
                    table_name=sql.Identifier(self.table_name)
                )
                cursor.execute(find_student_query, (student_id,))
                student = cursor.fetchone()

                if not student:
                    return False  # Student not found

                # Proceed to delete the student if found
                delete_query = sql.SQL("""
                     DELETE FROM {table_name} 
                     WHERE id = %s
                        """).format(
                    table_name=sql.Identifier(self.table_name)
                )
                cursor.execute(delete_query, (student_id,))

                # Commit the transaction
                self.connection.commit()

                return True  # Successfully deleted

        except Exception as e:
            # Handle errors and rollback transaction if necessary
            self.connection.rollback()
            messagebox.showerror('Database Error', f'Error deleting student: {e}')
            return False
