from db.db_client import DatabaseConnection


class DatabaseInitializer:
    def __init__(self) -> None:
        """
        Initialize a DatabaseInitializer object.
        The DatabaseInitializer is responsible for initializing the database schema.
        :return: None
        """
        self.db_connection = DatabaseConnection()

    def initialize_db(self) -> None:
        """
        Initialize the database schema.
        This method creates tables in the database if they do not already exist.
        :return: None
        """
        connection = self.db_connection.create_db_connection()

        # Create a cursor object to execute SQL queries
        cursor = connection.cursor()

        # Define the table schema
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS Customers (
            customer_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone_number TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS Accounts (
            account_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            account_number TEXT NOT NULL,
            balance REAL DEFAULT 0,
            FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
        );

        CREATE TABLE IF NOT EXISTS Transactions (
            transaction_id INTEGER PRIMARY KEY,
            account_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            transaction_type TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (account_id) REFERENCES Accounts(account_id)
        );
        '''

        # Execute the query to create tables
        cursor.executescript(create_table_query)
        # Commit the changes and close the connection
        connection.commit()
        connection.close()
