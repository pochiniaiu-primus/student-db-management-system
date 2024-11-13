from psycopg2 import sql


class UpdateStudentAttribute:

    def __init__(self, db_connection):
        self.connection = db_connection

    def update_student_field(self):
        """Update a specific field of a student record."""
        try:
            # Code to accept data from the user
            while True:
                try:
                    student_id = int(input("Enter id of the student to be updated: "))
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid student_id (numeric).")

            # Initialize a cursor to interact with the database
            cursor = self.connection.cursor()

            # Available fields and their prompts
            fields = {
                '1': ('name', 'Enter the new name: '),
                '2': ('address', 'Enter the new address: '),
                '3': ('age', 'Enter the new age: '),
                '4': ('number', 'Enter the new number: '),
            }
            print('Which field would you like to update? ')

            # Print out the available fields to update
            for key in fields:
                print(f'{key}:{fields[key][0]}')

            # Get user's choice for field to update
            while True:
                try:
                    field_choice = input('Enter the number of the field you want to update: ')
                    if field_choice not in fields:
                        print("Invalid choice. Please choose a valid field.")
                        continue
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid number of the field (numeric).")

            if field_choice in fields:
                field_name, prompt = fields[field_choice]
                new_value = input(prompt)

                if field_name == 'age':
                    try:
                        new_value = int(new_value)
                    except ValueError:
                        print("Invalid input. Age must be a number.")
                        return  # Exit the function if input is invalid

                data = sql.SQL("""
                     UPDATE {table_name}
                     SET {field}=%s
                     WHERE id=%s
                        """).format(
                    table_name=sql.Identifier("students2_1"),
                    field=sql.Identifier(field_name)
                )

                # Execute the query with the parameters
                cursor.execute(data, (new_value, student_id))

                # Commit the transaction to make sure the data is saved to the database
                self.connection.commit()

                # Provide feedback to the user
                if cursor.rowcount > 0:
                    print(f"{field_name.capitalize()} updated successfully.")
                else:
                    print(f"Student with ID: {student_id} not found.")

            else:
                print("Invalid choice. Please choose a valid field.")

        except Exception as e:
            print(f"Error updating data: {e}")

        finally:
            # Close the cursor
            cursor.close()
