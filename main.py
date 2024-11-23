from tkinter import Tk, Button, messagebox

from crud_operations.db import create_connection_with_retry, close_connection
from gui.create_student_window import CreateStudentWindow
from gui.delete_student_window import DeleteStudentWindow
from gui.read_student_window import ReadStudentWindow
from gui.update_student_window import UpdateStudentWindow


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

        # Create and display the buttons for different operations
        self.create_button = Button(self.master, text="Create New Student",
                                    command=self.open_create_window)
        self.delete_button = Button(self.master, text="Delete Student",
                                    command=self.open_delete_window)
        self.display_button = Button(self.master, text="Display Student",
                                     command=self.open_fetch_window)
        self.update_button = Button(self.master, text="Update Student",
                                    command=self.open_update_window)

        # Pack buttons to make them visible in the GUI
        self.create_button.pack(pady=10)
        self.delete_button.pack(pady=10)
        self.display_button.pack(pady=10)
        self.update_button.pack(pady=10)

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


def start_gui() -> None:
    """
    Initializes and starts the Tkinter GUI application.
    This function creates the root Tkinter window, establishes the database connection,
    and initializes the MainWindow class for CRUD operations.
    """
    root = Tk()  # Create a new Tkinter window (root window)
    root.title('Student Database Management System')
    root.geometry('400x200')  # Define the size of the window
    root.config(padx=10, pady=10)  # Add padding around the window edges

    # Establish the database connection with retry logic
    try:
        conn = create_connection_with_retry(retries=3, delay=5)
    except Exception as e:
        messagebox.showerror('Database Error', f'Could not connect to the database: {e}')
        root.destroy()  # Close the window if the connection fails
        return

    if conn:
        # Create and open the main window for CRUD operations
        MainWindow(root, conn)
        root.protocol('WM_DELETE_WINDOW',
                      lambda: (close_connection(conn), root.destroy()))
        root.mainloop()  # Start the Tkinter main event loop
    else:
        messagebox.showerror('Database Connection Error',
                             'Could not connect to the database.')


start_gui()
