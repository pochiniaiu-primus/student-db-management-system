import unittest
from unittest.mock import MagicMock, patch
from psycopg2 import sql
from crud_operations.add_student import AddStudent


class TestAddStudent(unittest.TestCase):

    def setUp(self):
        self.mock_db_connection = MagicMock()
        self.add_student_instance = AddStudent(self.mock_db_connection)

    def test_add_student_success(self):
        mock_cursor = MagicMock()
        self.mock_db_connection.cursor.return_value = mock_cursor

        name = "Se Honc"
        address = "Hamburg"
        age = 21
        number = "1234567890"

        with patch('crud_operations.add_student.messagebox.showinfo'), \
                patch('crud_operations.add_student.messagebox.showerror'):
            self.add_student_instance.add_student(name, address, age, number)

        expected_sql = sql.SQL("""
                 INSERT INTO {table_name} (name, address, age, number)
                 VALUES (%s, %s, %s, %s)
                    """).format(table_name=sql.Identifier('students2_1'))

        mock_cursor.execute.assert_called_once_with(expected_sql, (name, address, age, number))
        self.mock_db_connection.commit.assert_called_once()

    def test_add_student_invalid_phone_number(self):
        name = "Na Stia"
        address = "Hamburg"
        age = 21
        number = "12345"

        with patch('crud_operations.add_student.messagebox.showinfo'), \
                patch('crud_operations.add_student.messagebox.showerror') as mock_showerror:
            self.add_student_instance.add_student(name, address, age, number)

        mock_showerror.assert_called_once_with('Invalid Phone Number',
                                               'Please enter a valid phone number.')

    def test_add_student_missing_fields(self):
        name = ""
        address = "Hamburg"
        age = 21
        number = "1234567890"

        with patch('crud_operations.add_student.messagebox.showinfo'), \
                patch('crud_operations.add_student.messagebox.showerror') as mock_showerror:
            self.add_student_instance.add_student(name, address, age, number)

        mock_showerror.assert_called_once_with('Missing Fields', 'Please fill out all fields.')

    def test_add_student_database_error(self):
        mock_cursor = MagicMock()
        self.mock_db_connection.cursor.return_value = mock_cursor

        mock_cursor.execute.side_effect = Exception('Database Error')

        name = "Se Honc"
        address = "Hamburg"
        age = 21
        number = "1234567890"

        with patch('crud_operations.add_student.messagebox.showinfo'), \
                patch('crud_operations.add_student.messagebox.showerror') as mock_showerror:
            self.add_student_instance.add_student(name, address, age, number)

        mock_showerror.assert_called_once_with('Database Error', 'Error inserting data: Database Error')
        self.mock_db_connection.rollback.assert_called_once()
