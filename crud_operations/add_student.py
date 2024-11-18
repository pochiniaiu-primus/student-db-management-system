from psycopg2 import sql
from tkinter import messagebox


class AddStudent:

    def __init__(self, db_connection, table_name='students2_1'):
        self.connection = db_connection
        self.table_name = table_name

    def add_student(self, name, address, age, number):
        """
        Inserts a new student record into the students table.
        Args:
            name (str): Name of the student.
            address (str): Address of the student.
            age (int): Age of the student.
            number (str): Contact number of the student.
        """
        if not self.is_valid_phone_number(number):
            messagebox.showerror('Invalid Phone Number',
                                 'Please enter a valid phone number.')
            return

        try:
            # Create cursor for database interaction
            cursor = self.connection.cursor()

            # SQL insert query using parameterized inputs
            insert_data = sql.SQL("""
                 INSERT INTO {table_name} (name, address, age, number)
                 VALUES (%s, %s, %s, %s)
                    """).format(table_name=sql.Identifier(self.table_name))

            # Execute query with parameters
            cursor.execute(insert_data, (name, address, age, number))

            # Commit the transaction to make sure the data is saved to the database
            self.connection.commit()
            messagebox.showinfo('Success', 'Student added successfully!')

        except Exception as e:
            messagebox.showerror('Database Error,' f"Error inserting data: {e}")
            self.connection.rollback()  # Rollback on error to maintain consistency

        finally:
            # Close the cursor
            cursor.close()

    def is_valid_phone_number(self, number):
        """Validates that the phone number has 10 digits."""
        return len(number) == 10 and number.isdigit()
