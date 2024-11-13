from crud_operations.create_student import CreateStudent
from crud_operations.add_student import AddStudent
from crud_operations.read_student_data import StudentDataReader
from crud_operations.update_student import UpdateStudent
from crud_operations.update_student_attribute import UpdateStudentAttribute
from crud_operations.delete_student import DeleteStudent
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
        print("\n--- Welcome to the Student Database Management System ---")
        print("Please choose an option:")
        print('1. Create Student Table')
        print('2. Insert New Student')
        print('3. View All Students')
        print('4. Update Student Details')
        print('5. Update Single Field')
        print('6. Delete Student Record')
        print('7. Exit Application')

        try:
            choice = int(input('Enter your choice (1-7): '))
        except ValueError:
            print("Invalid input. Please enter a number (1-7).")
            continue

        # Mapping choices to corresponding operations
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
            update_student_instance = UpdateStudent(conn)
            update_student_instance.update_all_student_fields()
        elif choice == 5:
            # Update one student field
            update_one_attribute_student_instance = UpdateStudentAttribute(conn)
            update_one_attribute_student_instance.update_student_field()
        elif choice == 6:
            # Delete student
            delete_student_instance = DeleteStudent(conn)
            delete_student_instance.delete_student()
        elif choice == 7:
            # Exit the loop and application
            print("Exiting the application.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")

except Exception as e:
    print(f"Error connecting to the database: {e}")

finally:
    # Close the database connection if it was successfully created
    close_connection(conn)
