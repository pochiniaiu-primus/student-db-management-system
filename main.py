from tkinter import Tk, Button, messagebox
from crud_operations.db import create_connection_with_retry, close_connection
from gui.create_student_window import CreateStudentWindow
from gui.delete_student_window import DeleteStudentWindow


class MainWindow:
    """
    Main GUI window for the Student Database Management System.
    """

    def __init__(self, master, db_connection):
        """
        Initialize the main application window with options for CRUD operations.
        Args:
            master (Tk): The root Tkinter window.
            db_connection: Database connection object.
        """
        self.master = master
        self.db_connection = db_connection
        master.title('Student Database Management System')

        # Create and display buttons
        self.create_button = Button(self.master, text="Create New Student",
                                    command=self.open_create_window)
        self.delete_button = Button(self.master, text="Delete Student",
                                    command=self.open_delete_window)

        # Make the buttons visible
        self.create_button.pack(pady=10)
        self.delete_button.pack(pady=10)

    def open_create_window(self):
        """
        Opens the CreateStudentWindow when the user clicks the button.
        """
        CreateStudentWindow(self.master, self.db_connection)

    def open_delete_window(self):
        """
        Opens the DeleteStudentWindow when the user clicks the button.
        """
        DeleteStudentWindow(self.master, self.db_connection)


def start_gui():
    """
    Initialize and start the Tkinter application.
    """
    root = Tk()  # Create a new Tkinter window
    root.title('Student Database Management System')
    root.geometry('400x200')  # Centralize the window
    root.config(padx=10, pady=10)  # Add padding around the window edges

    # Establish database connection
    try:
        conn = create_connection_with_retry(retries=3, delay=5)
    except Exception as e:
        messagebox.showerror('Database Error', f'Could not connect to the database: {e}')
        root.destroy()
        return

    if conn:
        # Create main window
        MainWindow(root, conn)
        root.protocol('WM_DELETE_WINDOW',
                      lambda: (close_connection(conn), root.destroy()))
        root.mainloop()
    else:
        messagebox.showerror('Database Connection Error',
                             'Could not connect to the database.')


start_gui()
