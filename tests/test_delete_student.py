import unittest
from unittest.mock import MagicMock, patch

from psycopg2 import sql

from crud_operations.delete_student import DeleteStudent


class TestDeleteStudent(unittest.TestCase):
    def setUp(self):
        # Mock the database connection and cursor
        self.mock_connection = MagicMock()
        self.mock_cursor = MagicMock()
        self.mock_connection.cursor.return_value.__enter__.return_value = self.mock_cursor

        # Initialize the DeleteStudent instance
        self.table_name = 'test_table'
        self.delete_student = DeleteStudent(self.mock_connection, self.table_name)

    def tearDown(self):
        # Clean up mocks
        self.mock_cursor.reset_mock()
        self.mock_connection.reset_mock()

    @patch('tkinter.messagebox.showerror')
    def test_delete_student_exception(self, mock_showerror):
        # Simulate an exception during cursor execution
        self.mock_cursor.execute.side_effect = Exception("Simulated database error")

        result = self.delete_student.delete_student(student_id=1)

        self.assertFalse(result, "Expected delete_student to return False on exception")
        self.mock_cursor.execute.assert_called_once()  # Ensure execute was attempted
        self.mock_connection.rollback.assert_called_once()  # Ensure rollback was called
        mock_showerror.assert_called_once_with('Database Error', 'Error deleting student: Simulated database error')

    @patch('tkinter.messagebox.showerror')
    def test_delete_student_not_found(self, mock_showerror):
        # Simulate no student found in the database
        self.mock_cursor.fetchone.return_value = None  # Student was found

        result = self.delete_student.delete_student(student_id=1)

        self.assertFalse(result, "Expected delete_student return False if student is not found")
        self.mock_cursor.execute.assert_called_once()  # Ensure the SELECT query was executed
        mock_showerror.assert_not_called()  # Ensure no error message is displayed
        self.mock_connection.commit.assert_not_called()  # Ensure no commit occurred

    @patch('tkinter.messagebox.showinfo')
    def test_delete_student_success(self, mock_showinfo):
        # Simulate finding the student and successful deletion
        self.mock_cursor.fetchone.return_value = (1,)  # Student exists

        result = self.delete_student.delete_student(student_id=1)

        self.assertTrue(result, "Expected delete_student to return True on successful deletion")

        expected_select_query = sql.SQL("""
                             SELECT id FROM {table_name}
                             WHERE id = %s
                                """).format(
            table_name=sql.Identifier(self.table_name)
        )

        expected_delete_query = sql.SQL("""
                     DELETE FROM {table_name} 
                     WHERE id = %s
                        """).format(
            table_name=sql.Identifier(self.table_name)
        )

        # Ensure the SELECT query was executed
        self.mock_cursor.execute.assert_any_call(expected_select_query, (1,))

        # Ensure the DELETE query was executed
        self.mock_cursor.execute.assert_any_call(expected_delete_query, (1,))

        # Ensure commit occurred
        self.mock_connection.commit.assert_called_once()

        # Ensure no error message is displayed
        mock_showinfo.assert_not_called()
