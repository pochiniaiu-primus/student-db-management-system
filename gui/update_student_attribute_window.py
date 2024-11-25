import tkinter as tk
from tkinter import messagebox
from typing import Optional

from crud_operations.update_student_attribute import UpdateStudentAttribute


class UpdateStudentAttributeWindow:
    """
    A GUI window for updating a student's information in the database.
    Allows the user to select and modify specific student attributes.
    """

    def __init__(self, master, db_connection):
        """
        Initialize the window for updating a student's attributes.
        Args:
            master (tk.Tk): Parent Tkinter window (usually the root window).
            db_connection: Database connection object.
        """
        self.master = master  # Store the reference to the parent window.

        self.db_connection = db_connection  # Store the database connection

        # Create a new top-level window (a child window of the main root window)
        self.top = tk.Toplevel(self.master)
        self.top.title("Update Student's Attribute")
        self.top.resizable(True, True)

        self.update_student_instance = UpdateStudentAttribute(self.db_connection)

        self._update_form: Optional[tk.Frame] = None  # Placeholder for the update form frame.

        self.create_find_student_section()

    def create_find_student_section(self) -> None:
        """Create the section for entering a student ID to find."""
        tk.Label(self.top, text="Enter Student ID to Update: ").pack(pady=5)

        self.id_entry = tk.Entry(self.top)  # Input field for student ID.
        self.id_entry.pack(pady=5)

        tk.Button(self.top, text='Find Student', command=self.check_student_id).pack(pady=10)

    def check_student_id(self) -> None:
        """Check the validity of the entered Student ID and fetch the student's details."""

        student_id = self.id_entry.get().strip()

        if not student_id.isdigit():  # Validate that the input is numeric.
            messagebox.showerror('Invalid ID', 'Please enter a valid numeric ID.')
            return  # Exit if validation fails.

        student_id_int = int(student_id)

        # Check if the student exists in the database
        if self.update_student_instance.find_student_by_id(student_id_int):
            # If the update form is already open, bring it to focus.
            if self._update_form and self._update_form.winfo_exists():
                messagebox.showinfo('Form Already Open',
                                    "The update student's attribute form is already open.")
                self._update_form.focus_set()  # Focus on the existing form
            else:
                self.show_attributes_menu(student_id_int)  # Show the update options.

        else:
            # If no student is found, display an error message.
            messagebox.showerror('Student Not Found', f'No student found with ID: {student_id}')

    def show_attributes_menu(self, student_id: int) -> None:
        """Display attribute options to update for a student."""
        self.clear_update_form()  # Clear any existing update forms.

        self._update_form = tk.Frame(self.top)  # Create a new frame for the update form.
        self._update_form.pack(pady=10)

        tk.Label(self._update_form,
                 text="Choose an attribute to update:").pack(pady=10)

        # Mapping of attribute names to their respective commands.
        attributes = {
            'Name': lambda: self.create_update_field(student_id, 'name'),
            'Address': lambda: self.create_update_field(student_id, 'address'),
            'Age': lambda: self.create_update_field(student_id, 'age'),
            'Number': lambda: self.create_update_field(student_id, 'number'),

        }

        # Create a button for each attribute
        for attr, command in attributes.items():
            tk.Button(self._update_form, text=attr, command=command).pack(pady=5)

    def create_update_field(self, student_id: int, field: str) -> None:
        """Create input and update button for a specific attribute."""
        self.clear_update_form()  # Clear any existing forms

        self._update_form = tk.Frame(self.top)  # Create a new frame for this update form.
        self._update_form.pack(pady=10)

        # Display the attribute being updated.
        field_display = field.capitalize()

        tk.Label(self._update_form,
                 text=f'Updating {field_display} for Student ID: {student_id}').pack(pady=10)
        tk.Label(self._update_form,
                 text=f'Enter New {field_display}:').pack(pady=5)

        input_entry = tk.Entry(self._update_form)  # Create an input field for the new value.
        input_entry.pack(pady=5)

        # Command for submitting the update.
        update_command = lambda: self.submit_update(student_id, field, input_entry)
        tk.Button(self._update_form, text='Update', command=update_command).pack(pady=10)

    def submit_update(self, student_id: int, field: str, input_entry: tk.Entry) -> None:
        """Handle the update submission for a specific field."""
        value = input_entry.get().strip()

        # Validate input based on the field type.
        if field == 'age':
            try:
                value = int(value)
            except ValueError:
                messagebox.showerror('Invalid Age', 'Please enter aa valid numeric age.')
                return  # Exit if validation fails

        if field == 'number' and not value.isdigit():
            messagebox.showerror('Invalid Phone Number', 'Please enter a valid numeric phone number.')
            return

        try:
            # Attempt to update the student record in the database.
            self.update_student_instance.update_student_field(student_id, field, value)
            self.top.destroy()  # Close the window after successful update.
        except Exception as e:
            # Show an error message if the update fails.
            messagebox.showerror('Error', f'An error occurred: {e}')

    def clear_update_form(self) -> None:
        """Clear any existing form elements from the update form."""
        if self._update_form and self._update_form.winfo_exists():  # Check if the form exists
            self._update_form.destroy()  # Destroy the form to reset it.
