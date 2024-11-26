import tkinter as tk
from tkinter import messagebox, ttk, Frame

from crud_operations.read_student_data import StudentDataReader


class ReadStudentWindow:
    """
    This class creates a GUI window to display student records fetched from the database.
    """

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

        # Frame to contain the Treeview and its scrollbars
        tree_frame = Frame(self.top)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Vertical scrollbar for the Treeview
        self.tree_scroll_y = ttk.Scrollbar(tree_frame, orient='vertical')
        self.tree_scroll_y.pack(side='right', fill='y')

        # Horizontal scrollbar for the Treeview
        self.tree_scroll_x = ttk.Scrollbar(tree_frame, orient='horizontal')
        self.tree_scroll_x.pack(side='bottom', fill='x')

        self.db_connection = db_connection

        # Create a Treeview widget to display data in a table format
        self.tree = ttk.Treeview(tree_frame,
                                 columns=('id', 'name', 'address', 'age', 'number'),
                                 show='headings',
                                 yscrollcommand=self.tree_scroll_y.set,
                                 xscrollcommand=self.tree_scroll_x.set)
        # Configure Treeview column headings
        self.tree.heading('id', text='ID')
        self.tree.heading('name', text='Name')
        self.tree.heading('address', text='Address')
        self.tree.heading('age', text='Age')
        self.tree.heading('number', text='Number')

        # Adjust column width
        self.tree.column('id', width=50, anchor='center')
        self.tree.column('name', width=150, anchor='w')
        self.tree.column('address', width=200, anchor='w')
        self.tree.column('age', width=100, anchor='center')
        self.tree.column('number', width=150, anchor='center')

        self.tree.pack(fill='both', expand=True)  # Pack the Treeview widget into the window, expanding it

        # Connect scrollbars to Treeview
        self.tree_scroll_y.config(command=self.tree.yview)
        self.tree_scroll_x.config(command=self.tree.xview)

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
