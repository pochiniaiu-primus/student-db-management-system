from crud_operations.create_student import CreateStudent
from crud_operations.add_student import AddStudent
from crud_operations.db import create_connection_with_retry, close_connection

RETRIES = 3
DELAY = 5  # seconds

# Initialize the connection as None
conn = None

try:
    # Establish the database connection
    conn = create_connection_with_retry(retries=RETRIES, delay=DELAY)

    if conn is None:
        raise Exception("Database connection failed.")

    while True:
        print("\nWelcome to the student database management system!")
        print('1. Create Table')
        print('2. Insert Data')
        print('3. Exit')

        try:
            choice = int(input('Enter your choice (1-7): '))
        except ValueError:
            print("Invalid input. Please enter a number (1-3).")
            continue

        if choice == 1:
            # Create an instance of CreateStudent with the existing connection
            create_student_instance = CreateStudent(conn)
            # Create the table
            create_student_instance.create_student_table()
        elif choice == 2:
            insert_student_instance = AddStudent(conn)
            insert_student_instance.add_student()
        elif choice == 3:
            print("Exiting the application.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 3.")

except Exception as e:
    print(f"Error connecting to the database: {e}")

finally:
    # Close the database connection if it was successfully created
    close_connection(conn)
