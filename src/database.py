
import sqlite3
from typing import Optional

class Database:
    """
    Class for connecting to the student management system database.

    Attributes:
        host (str): The hostname or IP address of the server hosting the database.
        port (int): The port number used by the database server.
        username (str): The username for authentication with the database.
        password (str): The password for authentication with the database.
        db_name (str): The name of the database to connect to.
        connection (sqlite3.Connection): A handle to the open database connection.
    """

    def __init__(self, host: str, port: int, username: str, password: str, db_name: str) -> None:
        """
        Initialize the Database class and establish a connection to the database.

        Args:
            host (str): The hostname or IP address of the server hosting the database.
            port (int): The port number used by the database server.
            username (str): The username for authentication with the database.
            password (str): The password for authentication with the database.
            db_name (str): The name of the database to connect to.
        """
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.db_name = db_name
        self.connection = sqlite3.connect(f"{self.host}:{self.port}/{self.db_name}")

    def execute(self, query: str, parameters: Optional[tuple] = None) -> list:
        """
        Execute a SQL query on the database and return the results.

        Args:
            query (str): The SQL query to be executed.
            parameters (tuple): A tuple of parameter values for the query.

        Returns:
            list: The results of the query as a list of dictionaries.
        """
        with self.connection:
            cursor = self.connection.cursor()
            if parameters is not None:
                cursor.execute(query, parameters)
            else:
                cursor.execute(query)
            results = cursor.fetchall()
            return [dict(zip([column[0] for column in cursor.description], row)) for row in results]

    def close(self) -> None:
        """
        Close the database connection.
        """
        self.connection.close()