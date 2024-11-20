from psycopg2 import sql
from tkinter import messagebox


class AddStudent:
    """
    Class responsible for adding a new student record to the database.
    """

    def __init__(self, db_connection, table_name='students2_1'):
        """
         Initialize with database connection and optional table name.
         Args:
             db_connection: Active connection to the database.
             table_name (str): The database table name (default is 'students2_1').
         """
        self.connection = db_connection
        self.table_name = table_name

    def add_student(self, name, address, age, number):
        """
        Inserts a new student record into the database.
        Args:
            name (str): Name of the student.
            address (str): Address of the student.
            age (int): Age of the student.
            number (str): Contact number of the student.
        """
        # Validate the phone number format
        if not self.is_valid_phone_number(number):
            messagebox.showerror('Invalid Phone Number',
                                 'Please enter a valid phone number.')
            return

        try:
            # Create a cursor for executing SQL queries
            cursor = self.connection.cursor()

            # Prepare the SQL query for insertion with parameterized inputs
            insert_data = sql.SQL("""
                 INSERT INTO {table_name} (name, address, age, number)
                 VALUES (%s, %s, %s, %s)
                    """).format(table_name=sql.Identifier(self.table_name))

            # Execute the query with parameters
            cursor.execute(insert_data, (name, address, age, number))

            # Commit the changes to the database
            self.connection.commit()
            messagebox.showinfo('Success', 'Student added successfully!')

        except Exception as e:
            # Handle any errors during the database operation
            messagebox.showerror('Database Error,' f"Error inserting data: {e}")
            self.connection.rollback()  # Rollback if an error occurs to maintain data integrity

        finally:
            # Close the cursor
            cursor.close()

    def is_valid_phone_number(self, number):
        """Validates that the phone number has 10 digits."""
        return len(number) == 10 and number.isdigit()
