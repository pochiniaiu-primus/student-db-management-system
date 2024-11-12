from psycopg2 import sql


class AddStudent:

    def __init__(self, db_connection):
        self.connection = db_connection

    def add_student(self):
        """Accepts user input and inserts a new student record into the database."""
        try:
            # Code to accept data from the user with validation
            name = input("Enter name: ")
            address = input("Enter address : ")

            # Input validation for age
            while True:
                try:
                    age = int(input('Enter age: '))
                    break
                except ValueError:
                    print("Invalid age. Please enter a number.")

            number = input("Enter number: ")

            # Prepare and execute the SQL insert statement
            cursor = self.connection.cursor()
            insert_data = sql.SQL("""
                 INSERT INTO {table_name} (name, address, age, number)
                 VALUES (%s, %s, %s, %s)
                    """).format(table_name=sql.Identifier("students2_1"))

            # Execute the query with the parameters
            cursor.execute(insert_data, (name, address, age, number))

            # Commit the transaction to make sure the data is saved to the database
            self.connection.commit()

            print(f"Data added successfully.")

        except Exception as e:
            print(f"Error inserting data: {e}")
            self.connection.rollback()  # # Rollback on error to maintain consistency

        finally:
            # Close the cursor
            cursor.close()
