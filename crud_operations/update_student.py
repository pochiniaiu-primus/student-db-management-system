from psycopg2 import sql


class UpdateStudent:

    def __init__(self, db_connection):
        self.connection = db_connection

    def update_all_student_fields(self):
        """ Update the fields of a student record identified by their student_id.
        This method updates the name, address, age, and number of a student.
        """
        try:
            # Accept data from the user
            while True:
                try:
                    student_id = int(input("Enter id of the student to be updated: "))
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid student_id (numeric).")

            name = input("Enter name: ")
            address = input("Enter address : ")

            while True:
                try:
                    age = int(input("Enter age: "))
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid age (numeric).")

            number = input("Enter number: ")

            # Initialize a cursor to interact with the database
            cursor = self.connection.cursor()

            # Construct the update query
            update_query = sql.SQL("""
                 UPDATE {table_name} 
                 SET name = %s, address = %s, age = %s, number = %s
                 WHERE id=%s 
                    """).format(table_name=sql.Identifier("students2_1"))

            # Execute the query with the parameters
            cursor.execute(update_query, (name, address, age, number, student_id))

            # Check if the student was updated
            if cursor.rowcount > 0:
                print(f"Student with ID: {student_id} updated successfully.")
            else:
                print(f"Student with ID: {student_id} not found.")

            # Commit the transaction to make sure the data is saved to the database
            self.connection.commit()

            print("Data updated successfully.")

        except Exception as e:
            print(f"Error updating data: {e}")

        finally:
            # Close the cursor
            cursor.close()
