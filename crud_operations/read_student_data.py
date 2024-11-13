import psycopg2


class StudentDataReader:

    def __init__(self, db_connection):
        self.connection = db_connection

    def read_data(self):
        """Retrieve all records from the table in the database"""
        try:
            # Initialize a cursor to interact with the database
            cursor = self.connection.cursor()

            # Execute the SQL query to retrieve all rows in the table
            cursor.execute("SELECT * FROM students2_0;")

            # Fetch all results from the query
            students = cursor.fetchall()
            for student in students:
                # Print each student's data in a formatted output
                print(f'Student with ID: {student[0]}, Name: {student[1]},'
                      f' Address: {student[2]}, Age: {student[3]}, Number: {student[4]}')

            print("Connected to the database!")

        except psycopg2.DatabaseError as error:
            print("Error: Could not connect to the database", error)

        finally:
            # Close the cursor
            cursor.close()
