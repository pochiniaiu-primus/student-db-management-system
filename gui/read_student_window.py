import tkinter as tk
from tkinter import messagebox, ttk

from crud_operations.read_student_data import StudentDataReader


class ReadStudentWindow:
    """This class creates a GUI window to display student records fetched from the database."""

    def __init__(self, master, db_connection):
        """
        Initialize a new GUI window for reading student data.
        Args:
            master (tk.Tk): The parent Tkinter window that serves as the root of the application.
            db_connection: A live database connection used to fetch student data.
        """
        # Create a new top-level window (a child window of the main root window)
        self.top = tk.Toplevel(master)
        self.top.title('Student Records')
        self.top.geometry('1000x400')

        self.db_connection = db_connection

        # Create a Treeview widget to display data in a table format
        self.tree = ttk.Treeview(self.top,
                                 columns=('id', 'name', 'address', 'age', 'number'), show='headings')
        self.tree.heading('id', text='ID')
        self.tree.heading('name', text='Name')
        self.tree.heading('address', text='Address')
        self.tree.heading('age', text='Age')
        self.tree.heading('number', text='Number')
        self.tree.pack(fill='both', expand=True)  # Pack the Treeview widget into the window, expanding it

        # Add a button to refresh the data displayed in the Treeview
        tk.Button(self.top, text='Refresh Data', command=self.load_data).pack(pady=10)

        # Initially load the data when the window is created
        self.load_data()

    def load_data(self):
        """Fetch and display student data in the Treeview."""
        # Clear any existing data in the Treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Try to fetch records from the database using the StudentDataReader class
        try:
            read_student_instance = StudentDataReader(self.db_connection)
            records = read_student_instance.fetch_records()

            # Check if no records were fetched and show a message
            if not records:
                messagebox.showinfo('No Data', 'No records found')

            # Insert each record into the Treeview
            for record in records:
                self.tree.insert("", "end", values=record)

        except Exception as e:
            # Show an error message if an exception occurs while fetching or displaying the records
            messagebox.showerror('Error', f'An error occurred: {e}')
