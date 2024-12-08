import tkinter as tk
from tkinter import messagebox

from crud_operations.add_student import AddStudent


class CreateStudentWindow:
    """This class creates a GUI window to allow the user to add a new student to the database."""

    def __init__(self, master, db_connection):
        """
        Initialize a new window for creating a student.
        Args:
            master (Tkinter.Tk): The parent Tkinter window (usually the root window).
            db_connection: A live connection to the PostgreSQL database used to add the student.
        """
        # Create a new top-level window (a child window of the main root window)
        self.top = tk.Toplevel(master)
        self.top.title('Create New Student')

        # Store the database connection for use in submitting student data
        self.db_connection = db_connection

        # Call the method to create and display form fields
        self.create_form_fields()

    def create_form_fields(self):
        """
         Create, pack, and display form fields for user input to collect student information.

         This method sets up the graphical interface components (labels and entry fields)
         for entering student details such as:
             - Name (text input)
             - Age (numeric input)
             - Address (text input)
             - Contact Number (text input)

         It also adds a 'Submit' button to trigger the submission of the form data.
         """

        # Label and input field for the student's name
        tk.Label(self.top, text="Enter Student Name: ").pack(pady=5)
        self.name_entry = tk.Entry(self.top)
        self.name_entry.pack(pady=5)

        # Label and input field for the student's age
        tk.Label(self.top, text="Enter Student Age: ").pack(pady=5)
        self.age_entry = tk.Entry(self.top)
        self.age_entry.pack(pady=5)

        # Label and input field for the student's address
        tk.Label(self.top, text="Enter Student Address: ").pack(pady=5)
        self.address_entry = tk.Entry(self.top)
        self.address_entry.pack(pady=5)

        # Label and input field for the student's contact number
        tk.Label(self.top, text="Enter Student Number: ").pack(pady=5)
        self.number_entry = tk.Entry(self.top)
        self.number_entry.pack(pady=5)

        # Submit button to trigger the student creation process
        tk.Button(self.top, text='Submit', command=self.submit_student).pack(pady=10)

    def submit_student(self):
        """
        Collects the entered data from the form fields and adds the student to the database using AddStudent class.
        """

        # Get the entered name, age, address and number from the input fields
        name = self.name_entry.get()
        address = self.address_entry.get()
        number = self.number_entry.get()
        age = self.age_entry.get()

        # Validate name, address, and number fields
        if not name or not address or not age:
            messagebox.showerror('Missing Fields',
                                 'Please fill out all fields.')
            return

        # Validate phone number
        if not number.isdigit():
            messagebox.showerror('Invalid Phone Number',
                                 'Please enter a valid phone number.')
            return

        # Create AddStudent instance and add student data to the database
        create_student_instance = AddStudent(self.db_connection)
        create_student_instance.add_student(name, address, age, number)

        # Close the student creation window after submission
        self.top.destroy()
