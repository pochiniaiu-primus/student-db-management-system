from crud_operations.create_student import CreateStudent
from crud_operations.add_student import AddStudent
from crud_operations.read_student_data import StudentDataReader
from crud_operations.update_student import UpdateStudent
from crud_operations.db import create_connection_with_retry, close_connection

RETRIES = 3
DELAY = 5  # Delay in seconds for retrying connection

# Initialize the database connection as None
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
        print('3. Read Data')
        print('4. Update all Data')
        print('5. Exit')

        try:
            choice = int(input('Enter your choice (1-5): '))
        except ValueError:
            print("Invalid input. Please enter a number (1-5).")
            continue

        if choice == 1:
            # Create an instance of CreateStudent with the existing connection
            create_student_instance = CreateStudent(conn)
            # Create table if it does not exist
            create_student_instance.create_student_table()
        elif choice == 2:
            # Insert new student data
            insert_student_instance = AddStudent(conn)
            insert_student_instance.add_student()
        elif choice == 3:
            # Read and display student data
            read_student_instance = StudentDataReader(conn)
            read_student_instance.read_data()
        elif choice == 4:
            # Update all student data
            update_all_data_student_instance = UpdateStudent(conn)
            update_all_data_student_instance.update_all_student_fields()
        elif choice == 5:
            # Exit the loop and application
            print("Exiting the application.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

except Exception as e:
    print(f"Error connecting to the database: {e}")

finally:
    # Close the database connection if it was successfully created
    close_connection(conn)
