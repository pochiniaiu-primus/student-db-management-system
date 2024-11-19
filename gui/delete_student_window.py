import tkinter as tk
from tkinter import messagebox

from crud_operations.delete_student import DeleteStudent


class DeleteStudentWindow:
    """
    A GUI window for deleting a student from the database.
    """

    def __init__(self, master, db_connection):
        """
        Initialize a new window for deleting a student.
        Args:
            master (tk.Tk): The parent Tkinter window.
            db_connection: A live database connection.
        """
        # Create a new top-level window (child window of the main root window)
        self.top = tk.Toplevel(master)
        self.top.title('Delete Student')

        # Store the database connection
        self.db_connection = db_connection

        # Form fields for entering student datails
        self.initialize_form_fields()

    def initialize_form_fields(self):
        """
        Create and display input fields and buttons for deleting a student.
        """

        # Student ID input
        tk.Label(self.top, text="Enter Student ID: ").pack(pady=5)
        self.id_entry = tk.Entry(self.top)
        self.id_entry.pack(pady=5)

        # Submit button
        tk.Button(self.top, text='Delete', command=self.delete_student).pack(pady=10)

    def delete_student(self):
        """
        Handle the deletion of a student from the database.
        """
        # Trim whitespace for robustness
        student_id = self.id_entry.get().strip()

        # Validate ID input
        if not student_id.isdigit():
            messagebox.showerror('Invalid Input', 'Student ID must be a positive number.')
            return

        # Attempt to delete the student using the DeleteStudent class
        try:
            delete_student_instance = DeleteStudent(self.db_connection)
            success = delete_student_instance.delete_student(int(student_id))
            if success:
                messagebox.showinfo('Success',
                                    f'Student with ID: {student_id} has been deleted.')
            else:
                messagebox.showerror('Error', f'Student with ID: {student_id} does not exist.')
        except Exception as e:
            messagebox.showerror('Error', f'An error occurred: {e}')

        finally:
            self.top.destroy()
