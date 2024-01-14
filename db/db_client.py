import sqlite3
from sqlite3 import connect
from typing import Tuple, Optional


class DatabaseConnection:
    def __init__(self, connection_string='db/local_sqldb.db'):
        """
        Initialize a DatabaseConnection object.

        :param connection_string: The SQLite database connection string.
        """
        self.connection_string = connection_string

    def create_db_connection(self) -> connect:
        """
        Create and return a connection to the SQLite database.

        :return: SQLite database connection object.
        """
        conn = sqlite3.connect(self.connection_string)
        return conn

    @staticmethod
    def execute_query(query: str, query_data: tuple, connection: connect) -> Tuple[Optional[list], int]:
        """
        Execute an SQL query with provided data on the given connection.

        :param query: SQL query string.
        :param query_data: Data to be used in the query.
        :param connection: SQLite database connection object.
        :return: A tuple containing the result rows and the last inserted row ID.
                 Returns (None, last_row_id) if no result rows.
        :raises RuntimeError: If an error occurs during query execution.
        """
        try:
            cursor = connection.cursor()
            cursor.execute(query, query_data)
            last_row_id = cursor.lastrowid
            rows = cursor.fetchall()
            if rows:
                return rows, last_row_id
            return None, last_row_id
        except sqlite3.Error as e:
            print(e)
            raise RuntimeError("Could not execute query")
        except sqlite3.IntegrityError as e:
            raise RuntimeError("Could not execute query due to IntegrityError")
