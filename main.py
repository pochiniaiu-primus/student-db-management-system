import logging
from tkinter import Tk, Button, messagebox

from crud_operations.db import create_connection_with_retry, close_connection
from gui.create_student_window import CreateStudentWindow
from gui.delete_student_window import DeleteStudentWindow
from gui.read_student_window import ReadStudentWindow
from gui.update_student_window import UpdateStudentWindow
from gui.update_student_attribute_window import UpdateStudentAttributeWindow
from crud_operations.create_student_table import CreateStudent


class MainWindow:
    """
    Main GUI window for the Student Database Management System.
    Provides CRUD operations through buttons.
    """

    def __init__(self, master, db_connection):
        """
        Initialize the main application window with buttons to perform CRUD operations.

        Args:
            master (Tk): The root Tkinter window.
            db_connection: Active database connection object.
        """
        self.master = master  # The main Tkinter window
        self.db_connection = db_connection  # Database connection object
        master.title('Student Database Management System')

        self.create_buttons()

    def create_buttons(self):
        """
        Creates and displays buttons for CRUD operations.
        """

        buttons = [
            ("Create New Student", self.open_create_window),
            ("Delete Student", self.open_delete_window),
            ("Display Student", self.open_fetch_window),
            ("Update Student", self.open_update_window),
            ("Update Attribute", self.open_update_attribute_window),
        ]

        # Pack buttons to make them visible in the GUI
        for text, command in buttons:
            button = Button(self.master, text=text, command=command)
            button.pack(pady=10)

    def open_create_window(self) -> None:
        """
        Opens the CreateStudentWindow when the user clicks the 'Create New Student' button.
        """
        CreateStudentWindow(self.master, self.db_connection)

    def open_delete_window(self) -> None:
        """
        Opens the DeleteStudentWindow when the user clicks the 'Delete Student' button.
        """
        DeleteStudentWindow(self.master, self.db_connection)

    def open_fetch_window(self) -> None:
        """
        Opens the ReadStudentWindow when the user clicks the 'Display Student' button.
        Ensures only one window instance exists at a time.
        """
        ReadStudentWindow(self.master, self.db_connection)

    def open_update_window(self) -> None:
        """
        Opens the UpdateStudentWindow when the user clicks the 'Update Student' button.
        """
        UpdateStudentWindow(self.master, self.db_connection)

    def open_update_attribute_window(self) -> None:
        """
        Opens the UpdateStudentAttributeWindow when the user clicks the 'Update Attribute' button.
        """
        UpdateStudentAttributeWindow(self.master, self.db_connection)


def start_gui() -> None:
    """
    Initializes and starts the Tkinter GUI application.
    This function sets up the root Tkinter window, establishes the database connection,
    ensures the student table exists, and opens the main window for CRUD operations.
    """
    root = Tk()  # Create the main Tkinter window (root window)
    root.title('Student Database Management System')
    root.geometry('400x300')  # Define the initial size of the window
    root.config(padx=10, pady=10)  # Add padding around the window edges

    try:
        # Establish the database connection with retry logic
        conn = create_connection_with_retry(retries=3, delay=5)
        if not conn:
            # If the connection is not successful, show an error and exit
            messagebox.showerror('Database Error', 'Could not connect to the database.')
            return

        # Ensure the student table exists by calling CreateStudent
        table_creator = CreateStudent(conn)
        table_creator.create_student_table()  # Create the table if it doesn't exist.

        # After successful table creation, open the main window for CRUD operations
        MainWindow(root, conn)
        root.protocol('WM_DELETE_WINDOW',
                      lambda: (close_connection(conn), root.destroy()))
        root.mainloop()  # Start the Tkinter main event loop

    except Exception as e:
        # Handle any errors during the connection or table creation process
        messagebox.showerror('Database Error', f'Could not initialize the database: {e}')
        logging.error(f'Initialization error: {e}', exc_info=True)
        root.destroy()  # Close the window if the connection or initialization fails


if __name__ == '__main__':
    start_gui()
