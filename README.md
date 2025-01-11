# Student Database Management System

## Project Overview

This project, **Student Database Management System**, is a Python-based application that leverages the **Tkinter**
library for its graphical user interface (GUI) and **PostgreSQL** for robust data management. The system supports full
CRUD (Create, Read, Update, Delete) operations, allowing users to efficiently manage student records. Key
functionalities
include adding new students, updating existing student information, deleting records, and viewing the existing data
through
an intuitive GUI.

## Key Features

1. **Create Student**: Add a new student to the database with information such as name, address, age, and phone number.
2. **Delete Student**: Remove a student from the database based on their unique ID.
3. **Read Student**: Display the list of all students in the database.
4. **Update Student**: Modify a student's information, such as their name, address, age or phone number.
5. **Update Attribute**: Update specific attributes (like address, age, etc.) of a student record.

## Tech Stack

- **Frontend**:
    - Python Tkinter (for GUI)
- **Backend**:
    - PostgreSQL (Database)
    - psycopg2 (Python library for PostgreSQL)
    - Python (Programing Language)
- **Testing**:
    - unittest (Unit testing framework)
- **Logging**:
    - logging (Python built-in module for error tracking)

## Requirements

To run the project, ensure you have the following installed and set up:

- Python 3.6 or later.
- PostgreSQL (Make sure the PostgreSQL server is installed and configured)
- psycopg2 (Python library for PostgreSQL)
- Tkinter (Python library for GUI, usually comes pre-installed configured)
- Environment variables for database connection parameters:
    - 'DBNAME', 'USER', 'PASSWORD', 'HOST', 'PORT'

## File Structure

### The project is organized into the following files:

Student-Database-Management-System/

#### crud_operations/

- **add_student.py** *Logic for adding a new student to the database*
- **delete_student.py** *Logic for deleting a student from the database*
- **read_student_data.py** *Logic for reading student records from the database*
- **update_student.py** *Logic for updating student records in the database*
- **update_student_attribute.py** *Logic for updating specific student attributes in the database*
- **create_student_table.py** *Creates the student table in the database if it doesn't exist*
- **db.py** *Handles database connection and retry logic*

#### gui/

- **create_student_window.py** *GUI window for adding a student*
- **delete_student_window.py** *GUI window for deleting a student*
- **read_student_window.py** *GUI window for displaying students*
- **update_student_attribute_window.py** *GUI window for updating specific student attributes*
- **update_student_window.py** *GUI window for updating student information*

#### tests/

- **test_create_student.py** *Unit tests for adding a student*
- **test_delete_student.py** *Unit tests for deleting a student*
- **test_read_student.py** *Unit tests for reading student data*
- **test_update_student.py** *Unit tests for updating student information*

#### main.py

- *Entry point for the application*

#### README.md

- *Project documentation*