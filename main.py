from tkinter import *
from tkinter import messagebox
from crud_operations.db import create_connection_with_retry, close_connection
from gui.create_student_window import CreateStudentWindow


class MainWindow:

    def __init__(self, master, db_connection):
        """
        Main window for the application with options for CRUD operations.
        Args:
            master (Tkinter.Tk): The main Tkinter window.
            db_connection (psycopg2 connection object): A live connection to the PostgreSQL database.
        """
        self.master = master
        self.db_connection = db_connection
        master.title('Student Database Management System')

        # Button to open the student creation window
        self.create_button = Button(self.master, text="Create New Student",
                                    command=self.open_create_window)
        # Make the button visible
        self.create_button.pack(pady=10)

    def open_create_window(self):
        """
        Opens the CreateStudentWindow when the user clicks the button.
        """
        CreateStudentWindow(self.master, self.db_connection)


def start_gui():
    """
    Initialize and start the Tkinter application with the database connection.
    """
    root = Tk()  # Create a new Tkinter window
    root.minsize(width=400, height=200)  # Set the window size
    root.config(padx=10, pady=10)  # Add padding around the window edges

    # Establish database connection
    conn = create_connection_with_retry(retries=3, delay=5)

    if conn:
        # Create main window
        main_window = MainWindow(root, conn)
        root.protocol('WM_DELETE_WINDOW',
                      lambda: (close_connection(conn), root.destroy()))
    else:
        messagebox.showerror('Database Connection Error',
                             'Failed to connect to the database. Exiting.')
        root.quit()

    # Start the Tkinter event loop
    root.mainloop()


start_gui()
