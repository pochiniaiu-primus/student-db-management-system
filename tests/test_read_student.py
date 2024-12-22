import unittest
from unittest.mock import MagicMock, patch

import psycopg2

from crud_operations.read_student_data import StudentDataReader


class TestStudentDataReader(unittest.TestCase):
    """Unit test case for the StudentDataReader class."""

    @patch('psycopg2.connect')
    def setUp(self, mock_connect):
        """
        Set up the test environment before each test method.
        Creating a mock database connection and cursor.
        """
        # Create a mock database connection
        self.mock_connection = MagicMock()

        # Crate a mock cursor for the database connection
        self.mock_cursor = MagicMock()

        # Configure the mock connection to return the mock cursor
        self.mock_connection.cursor.return_value = self.mock_cursor

        # Configure the mock psycopg2 connect method to return the mock connection
        mock_connect.return_value = self.mock_connection

        # Create an instance of StudentDataReader with the mock connection and test table name
        self.reader = StudentDataReader(self.mock_connection, 'test_table')

    def test_fetch_records_success(self):
        # Define mock data to be returned by the cursor
        mock_data = [(1, 'Na Stia', 'Hannover', 21, '1234567890')]
        self.mock_cursor.fetchall.return_value = mock_data

        records = self.reader.fetch_records()

        # Verify that the execute method was called on the cursor with the correct SQL query
        self.mock_cursor.execute.assert_called_once_with("SELECT * FROM test_table;")

        # Verify that the fetchall method was called on the cursor
        self.mock_cursor.fetchall.assert_called_once()

        self.assertEqual(records, mock_data)

    @patch('tkinter.messagebox.showerror')
    def test_fetch_records_database_error(self, mock_showerror):
        # Simulate a database error by raising a DatabaseError exception
        self.mock_cursor.execute.side_effect = psycopg2.DatabaseError('Mocked database error')

        records = self.reader.fetch_records()

        # Verify that the showerror method was called with the correct error message
        mock_showerror.assert_called_once_with('Database Error', 'Failed to fetch records: Mocked database error')

        # Verify that no records are returned
        self.assertEqual(records, [])

    def tearDown(self):
        """
        Clean up the test environment after each test method.
        This includes verifying that the cursor was closed.
        """
        # Verify that the cursor's close method was called
        self.mock_cursor.close.assert_called_once()
