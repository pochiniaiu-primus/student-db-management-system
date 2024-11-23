import tkinter as tk
from tkinter import messagebox
from typing import Optional
from crud_operations.update_student import UpdateStudent


class UpdateStudentWindow:
    """A GUI window for updating a student's information in the database."""

    def __init__(self, master, db_connection):
        """
        Initialize a new window for updating a student.
        Args:
            master (Tkinter.Tk): The parent Tkinter window (usually the root window).
            db_connection: Active database connection to the PostgreSQL database used to update the student.
        """
        # Create a new top-level window (a child window of the main root window)
        self.top = tk.Toplevel(master)
        self.top.title('Update Student')

        # Store the database connection for use in submitting student data
        self.db_connection = db_connection
        self.update_student_instance = UpdateStudent(self.db_connection)

        self._update_form: Optional[tk.Frame] = None  # Track update form state

        self.create_find_student_section()

    def create_find_student_section(self) -> None:
        """Create UI elements to find a student by their ID."""
        tk.Label(self.top, text="Enter Student ID to Update: ").pack(pady=5)
        self.id_entry = tk.Entry(self.top)
        self.id_entry.pack(pady=5)

        tk.Button(self.top, text='Find Student', command=self.check_student_id).pack(pady=10)

    def check_student_id(self) -> None:
        """
        Validates the entered Student ID and fetches the student's details from the database.
        Ensures a valid numeric ID is provided and opens the update form if the student exists.
        """
        student_id = self.id_entry.get().strip()

        if not student_id.isdigit():
            messagebox.showerror('Invalid ID', 'Please enter a valid numeric ID.')
            return

        # Check if the student exists in the database
        if self.update_student_instance.find_student_by_id(student_id):
            # Ensure only one form exists
            if self._update_form and self._update_form.winfo_exists():
                messagebox.showinfo('Form Already Open', 'The update form is already open.')
                self._update_form.focus_set()  # Focus on the existing form
            else:
                self.create_form_fields(student_id)
        else:
            messagebox.showerror('Student Not Found', f'No student found with ID: {student_id}')

    def create_form_fields(self, student_id: str) -> None:
        """
        Create form fields to update a student's details.

        Args:
            student_id (str): The ID of the student to update.
        """
        self._update_form = tk.Frame(self.top)
        self._update_form.pack(pady=10)

        tk.Label(self._update_form, text=f'Updating Student with ID: {student_id}').pack(pady=10)

        # Name input
        tk.Label(self._update_form, text="Enter Student Name: ").pack(pady=5)
        self.name_entry = tk.Entry(self._update_form)
        self.name_entry.pack(pady=5)

        # Age input
        tk.Label(self._update_form, text="Enter Student Age: ").pack(pady=5)
        self.age_entry = tk.Entry(self._update_form)
        self.age_entry.pack(pady=5)

        # Address input
        tk.Label(self._update_form, text="Enter Student Address: ").pack(pady=5)
        self.address_entry = tk.Entry(self._update_form)
        self.address_entry.pack(pady=5)

        # Phone number input
        tk.Label(self._update_form, text="Enter Student Number: ").pack(pady=5)
        self.number_entry = tk.Entry(self._update_form)
        self.number_entry.pack(pady=5)

        # Submit button
        tk.Button(self._update_form, text='Update', command=lambda: self.update_student(student_id)).pack(pady=10)

    def update_student(self, student_id: str) -> None:
        """
         Update the student's information in the database.

         Args:
             student_id (str): The ID of the student to update.
         """

        name = self.name_entry.get().strip()
        address = self.address_entry.get().strip()
        number = self.number_entry.get().strip()
        try:
            age = int(self.age_entry.get().strip())
        except ValueError:
            messagebox.showerror('Invalid Age', 'Please enter a valid numeric age.')
            return

        if not name or not address or not number:
            messagebox.showerror('Missing Fields',
                                 'Please fill out all fields except age.')
            return

        if not number.isdigit():
            messagebox.showerror('Invalid Phone Number',
                                 'Please enter a valid numeric phone number.')
            return

        try:
            self.update_student_instance.update_all_student_fields(student_id,
                                                                   name,
                                                                   address,
                                                                   age,
                                                                   number)
            self.top.destroy()  # Close the window after a successful update
        except Exception as e:
            messagebox.showerror('Error', f'An error occured: {e}')
