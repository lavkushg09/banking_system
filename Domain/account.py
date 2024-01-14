from typing import Optional


class Account:
    def __init__(self, account_id: int, customer_id: int, account_number: int, balance: Optional[int] = 0):
        """
        Initialize an Account object.

        :param account_id: Unique identifier for the account.
        :param customer_id: Unique identifier for the customer associated with the account.
        :param account_number: Account number.
        :param balance: Initial balance of the account (default is 0).
        """
        self.balance = balance
        self.account_id = account_id
        self.customer_id = customer_id
        self.account_number = account_number

    def set_account_id(self, account_id: int) -> None:
        """
        Set the account_id for the account.

        :param account_id: New account_id to set.
        :return: None
        """
        self.account_id = account_id

    def deposit(self, amount: float) -> float:
        """
        Deposit funds into the account.

        :param amount: Amount to deposit.
        :return: Updated balance after the deposit.
        """
        self.balance += amount
        return self.balance

    def withdraw(self, amount: float) -> float:
        """
        Withdraw funds from the account.

        :param amount: Amount to withdraw.
        :return: Updated balance after the withdrawal.
        :raises ValueError: If there are insufficient funds for the withdrawal.
        """
        if self.balance >= amount:
            self.balance -= amount
            return self.balance
        else:
            raise ValueError("Insufficient funds")

    def get_balance(self) -> float:
        """
        Get the current balance of the account.

        :return: Current balance of the account.
        """
        return self.balance
