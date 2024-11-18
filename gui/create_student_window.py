import tkinter as tk
from tkinter import messagebox

from crud_operations.add_student import AddStudent


class CreateStudentWindow:

    def __init__(self, master, db_connection):
        """
        Initialize a new window for creating a student.
        Args:
            master (Tkinter.Tk): The parent Tkinter window (root in this case).
            db_connection: A live connection to the PostgreSQL database.
        """
        # Create a new top-level window (child window of the main root window)
        self.top = tk.Toplevel(master)
        self.top.title('Create New Student')

        # Store the database connection
        self.db_connection = db_connection

        # Form fields for entering student datails
        self.create_form_fields()

    def create_form_fields(self):
        """
        Create, pack and display form fields for user input to collect student information.

        This method sets up the graphical interface components (labels and input fields)
        for entering student details such as name, age, address, and contact number.
        It also adds a Submit button to trigger the submission of the data.

        Fields:
            - Student Name (Text Entry)
            - Student Age (Numeric Entry)
            - Student Address (Text Entry)
            - Student Contact Number (Text Entry)
        """

        # Create and pack a label and text entry field for the student's name
        tk.Label(self.top, text="Enter Student Name: ").pack(pady=5)
        self.name_entry = tk.Entry(self.top)
        self.name_entry.pack(pady=5)

        # Create and pack a label and text entry field for the student's age
        tk.Label(self.top, text="Enter Student Age: ").pack(pady=5)
        self.age_entry = tk.Entry(self.top)
        self.age_entry.pack(pady=5)

        # Create and pack a label and text entry field for the student's address
        tk.Label(self.top, text="Enter Student Address: ").pack(pady=5)
        self.address_entry = tk.Entry(self.top)
        self.address_entry.pack(pady=5)

        # Create and pack a label and text entry field for the student's contact number
        tk.Label(self.top, text="Enter Student Number: ").pack(pady=5)
        self.number_entry = tk.Entry(self.top)
        self.number_entry.pack(pady=5)

        # Submit button for form submission
        tk.Button(self.top, text='Submit', command=self.submit_student).pack(pady=10)

    def submit_student(self):
        """
        Collects the entered data and adds the student to the database using AddStudent class.
        """

        # Get the entered name, age, address and number from the input fields

        name = self.name_entry.get()
        try:
            age = int(self.age_entry.get())
        except ValueError:
            messagebox.showerror('Invalid Age', 'Please enter a valid number')
            return

        address = self.address_entry.get()

        number = self.number_entry.get()

        # Validate name, address, and number fields
        if not name or not address or not number:
            messagebox.showerror('Missing Fields',
                                 'Please fill out all fields except age.')
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
