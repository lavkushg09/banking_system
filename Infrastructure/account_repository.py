from db.db_client import DatabaseConnection
from Domain import Account, Customer
from typing import Optional, Union
from sqlite3 import connect


class AccountRepository:
    def __init__(self, db_connection=DatabaseConnection()) -> None:
        """
        Initialize an AccountRepository object.

        The AccountRepository interacts with the database to perform operations on accounts and customers.

        :return: None
        """
        self.db_connection = db_connection

    def save_account(self, account: Account, customer: Optional[Customer] = None) -> Account:
        """
        Save an account and its associated customer to the database.

        If the account already exists, update its details. If a customer is provided, save the customer details.

        :param account: The account to be saved or updated.
        :param customer: The associated customer, if any.
        :return: The saved or updated account.
        :raises RuntimeError: If an error occurs during the database operation.
        """
        connection = self.db_connection.create_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        try:
            already_account = self.find_accounts_by_customer_id(account.customer_id)
            if already_account:
                account.account_id = already_account.account_id
                account.account_number = already_account.account_number
                if customer is not None:
                    account.balance = already_account.balance

            self._save_customer(customer, connection)
            _, account_id = self._save_account(account, connection)
            account.set_account_id(account_id)
            connection.commit()
            return account
        except RuntimeError as e:
            connection.rollback()
        finally:
            connection.close()

    def _save_customer(self, customer: Customer, connection: connect):
        """
        Save a customer to the database if provided.

        :param customer: The customer to be saved.
        :param connection: The database connection.
        :return: None
        """
        if customer:
            return self.db_connection.execute_query(
                "INSERT OR IGNORE INTO Customers (customer_id, name, phone_number, email) VALUES(?,?,?,?)",
                (customer.customer_id, customer.name, customer.phone_number, customer.email), connection)
        return None, None

    def _save_account(self, account: Account, connection: connect):
        """
        Save or update an account in the database.

        :param account: The account to be saved or updated.
        :param connection: The database connection.
        :return: A tuple containing the result rows and the last inserted row ID.
        """

        if account.account_id:
            return self.db_connection.execute_query(
                "INSERT OR REPLACE INTO Accounts (account_id, customer_id, account_number, balance)"
                " VALUES (?,?,?,?)",
                (account.account_id, account.customer_id, account.account_number, account.balance),
                connection)
        else:
            return self.db_connection.execute_query(
                "INSERT INTO Accounts (customer_id, account_number, balance) VALUES (?,?,?)",
                (account.customer_id, account.account_number, account.balance),
                connection)

    def find_account_by_id(self, account_id: int) -> Account:
        """
        Find an account by its ID in the database.

        :param account_id: The ID of the account to search for.
        :return: The found account.
        :raises ValueError: If the account is not found for the given ID.
        """
        connection = self.db_connection.create_db_connection()
        data_list, _ = self.db_connection.execute_query("SELECT * FROM Accounts WHERE account_id =?",
                                                        (account_id,),
                                                        connection)
        if data_list:
            data = data_list[0]
            return Account(data[0], data[1], int(data[2]), data[3])
        raise ValueError("Account not found for given account id.")

    def find_accounts_by_customer_id(self, customer_id: int) -> Union[None, Account]:
        """
        Find accounts associated with a customer ID in the database.

        :param customer_id: The ID of the customer.
        :return: The found account or None if not found.
        """
        connection = self.db_connection.create_db_connection()
        data_list, _ = self.db_connection.execute_query("SELECT * FROM Accounts WHERE customer_id =?",
                                                        (customer_id,),
                                                        connection)
        if data_list:
            data = data_list[0]
            return Account(data[0], data[1], int(data[2]), data[3])
        return None
