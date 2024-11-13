from psycopg2 import sql


class DeleteStudent:

    def __init__(self, db_connection):
        self.connection = db_connection

    def delete_student(self):
        """Delete a student record from the database identified by the student's ID."""
        try:
            # Code to accept data from the user
            cursor = self.connection.cursor()

            # Accept student ID and validate it as an integer
            while True:
                try:
                    student_id = int(input("Enter id of the student you want to delete: "))
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid student_id (numeric).")

            # Check if the student exists in the database
            find_student_by_id = sql.SQL("""
                         SELECT * FROM {table_name}
                         WHERE id=%s
                            """).format(
                table_name=sql.Identifier("students2_1")
            )

            cursor.execute(find_student_by_id, (student_id,))
            student = cursor.fetchone()

            if student:
                # Display the student information and prompt for confirmation
                print(f'Student to be deleted: ID: {student[0]}, Name: {student[1]},'
                      f' Address: {student[2]}, Age: {student[3]}, Number: {student[4]}')
                choice = input('Are you sure you want to delete the student?: (yes/no) ').strip().lower()

                if choice == 'yes':
                    # Delete the student record if confirmed
                    delete = sql.SQL("""
                         DELETE FROM {table_name} 
                         WHERE id=%s
                            """).format(
                        table_name=sql.Identifier("students2_1")
                    )
                    cursor.execute(delete, (student[0],))

                    # Commit the deletion to the database
                    self.connection.commit()
                    print(f"Student with ID {student[0]} has been deleted successfully.")
                else:
                    print('Deletion cancelled.')
            else:
                print("Student with the specified ID was not found.")

        except Exception as e:
            # Error handling and rollback in case of an error
            print(f"Error deleting data: {e}")
            self.connection.rollback()

        finally:
            # Close the cursor
            cursor.close()
