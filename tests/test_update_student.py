import unittest
from unittest.mock import MagicMock, patch

import psycopg2
from psycopg2 import sql

from crud_operations.update_student import UpdateStudent


class TestUpdateStudent(unittest.TestCase):
    """
    Unit test case for the UpdateStudent class.
    """

    @patch('psycopg2.connect')
    def setUp(self, mock_connect):
        """
        Set up the test environment before each test method.
        This includes creating a mock database connection and cursor.
        """
        # Create a mock database connection
        self.mock_connection = MagicMock()

        # Create a mock cursor for the database connection
        self.mock_cursor = MagicMock()

        # Configure the mock connection to return the mock cursor
        self.mock_connection.cursor.return_value = self.mock_cursor

        # Configure the mock psycopg2 connect method to return the mock connection
        mock_connect.return_value = self.mock_connection

        # Create an instance of UpdateStudent with the mock connection and a test table name
        self.updater = UpdateStudent(self.mock_connection, 'test_table')

    @patch('tkinter.messagebox.showinfo')
    def test_update_student_success(self, mock_showinfo):
        """
        Test case for successfully updating a student record in the database.
        """
        # Mock the update success by setting rowcount to 1
        self.mock_cursor.rowcount = 1

        # Call the method to update the student
        self.updater.update_all_student_fields(1, 'Na Stia', 'Hannover', 21, '1234567890')

        # Verify that the SQL update query was executed correctly
        self.mock_cursor.execute.assert_called_with(
            sql.SQL("""
                 UPDATE {table_name} 
                 SET name = %s, address = %s, age = %s, number = %s
                 WHERE id = %s 
                    """).format(table_name=sql.Identifier('test_table')),
            ('Na Stia', 'Hannover', 21, '1234567890', 1)
        )
        self.mock_connection.commit.assert_called_once()

        # Verify that the info message was displayed
        mock_showinfo.assert_called_once_with('Success', 'Student with ID 1 updated successfully.')

    @patch('tkinter.messagebox.showwarning')
    def test_update_student_not_found(self, mock_showwarning):
        """
        Test case for handling the case when a student record is not found in the database.
        """
        # Mock the student not found by setting rowcount to 0
        self.mock_cursor.rowcount = 0

        # Call the method to update the student
        self.updater.update_all_student_fields(1, 'Na Stia', 'Hannover', 21, '1234567890')

        # Verify that the SQL update query was executed correctly
        self.mock_cursor.execute.assert_called_with(
            sql.SQL("""
                 UPDATE {table_name} 
                 SET name = %s, address = %s, age = %s, number = %s
                 WHERE id = %s 
                    """).format(table_name=sql.Identifier('test_table')),
            ('Na Stia', 'Hannover', 21, '1234567890', 1)
        )
        self.mock_connection.commit.assert_called_once()

        # Verify that the warning message was displayed
        mock_showwarning.assert_called_once_with('Not Found', 'Student with ID 1 not found.')

    @patch('tkinter.messagebox.showerror')
    def test_update_student_exception(self, mock_showerror):
        """
        Test case for handling exceptions during the update process.
        """

        # Simulate an exception during SQL execution
        self.mock_cursor.execute.side_effect = psycopg2.Error('Mocked exception')

        # Call the method to update the student
        self.updater.update_all_student_fields(1, 'Na Stia', 'Hannover', 21, '1234567890')

        # Verify that the rollback was called
        self.mock_connection.rollback.assert_called_once()

        # Verify that the error message was displayed
        mock_showerror.assert_called_once_with('Database Error', 'Could not update student: Mocked exception')

    def tearDown(self):
        """
        Clean up the test environment after each test method.
        """
        # Verify that the cursor was closed
        self.mock_cursor.close.assert_called_once()
