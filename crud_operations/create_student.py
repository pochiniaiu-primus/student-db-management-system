from psycopg2 import sql

class CreateStudent:

    def __init__(self, db_connection):
        self.connection = db_connection

    def create_student_table(self):
        """Create the student table in the PostgreSQL database."""
        try:
            # Initialize cursor to execute SQL queries
            cursor = self.connection.cursor()

            # Construct the SQL query using sql.SQL and sql.Identifier to create the table if it doesn't exist.
            create_table_query = sql.SQL("""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    id SERIAL PRIMARY KEY,
                    name TEXT,
                    address TEXT,
                    age INT,
                    number TEXT
                );
            """).format(table_name=sql.Identifier("students2_1"))

            # Execute a SQL query
            cursor.execute(create_table_query)

            # Commit the transaction after executing the query to make the changes persistent.
            self.connection.commit()

            print("Table created successfully.")

        except Exception as e:
            print(f"Error creating table: {e}")
            self.connection.rollback()  # Rollback in case of error

        finally:
            # Close the cursor and connection
            cursor.close()
