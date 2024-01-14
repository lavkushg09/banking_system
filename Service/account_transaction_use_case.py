from Infrastructure import AccountRepository
from Domain import Account


class AmountTransaction:
    def __init__(self, account_repository: AccountRepository):
        """
        Initialize an AmountTransaction object.

        The AmountTransaction is responsible for performing transactions and updating the associated accounts.

        :param account_repository: The repository for interacting with accounts in the database.
        :return: None
        """
        self.account_repository = account_repository

    def make_transaction(self, account_id: int, amount: float, transaction_type: str) -> Account:
        """
        Perform a transaction on the specified account and update it in the database.

        :param account_id: The ID of the account on which the transaction is performed.
        :param amount: The amount of the transaction.
        :param transaction_type: The type of the transaction ("deposit" or "withdraw").
        :return: The updated account instance.
        :raises ValueError: If an invalid transaction type is provided.
        """
        account = self.account_repository.find_account_by_id(account_id)
        print("Transaction", f"{account.__dict__}")
        if transaction_type == "deposit":
            account.deposit(amount)
            print(account.balance, "balance")
        elif transaction_type == "withdraw":
            account.withdraw(amount)
        else:
            raise ValueError("Invalid transaction type")
        account_ins = self.account_repository.save_account(account)
        self.create_transaction(account_id, amount, transaction_type)
        return account_ins

    def create_transaction(self, account_id: int, amount: float, transaction_type: str):
        """
        Create a transaction record in the database.

        :param account_id: The ID of the account associated with the transaction.
        :param amount: The amount of the transaction.
        :param transaction_type: The type of the transaction ("deposit" or "withdraw").
        :return: None
        """
        connection = self.account_repository.db_connection.create_db_connection()
        self.account_repository.db_connection.execute_query(
            "INSERT INTO Transactions (account_id, amount, transaction_type) VALUES (?,?,?)",
            (account_id, amount, transaction_type),
            connection)
        connection.commit()
        connection.close()
