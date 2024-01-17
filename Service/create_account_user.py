from datetime import datetime
from Domain.account import Account
from Domain.customer import Customer


class AccountOpening:
    def __init__(self, account_repository):
        """
        Initialize an AccountOpening object.

        The AccountOpening is responsible for creating new accounts for customers.

        :param account_repository: The repository for interacting with accounts in the database.
        :return: None
        """
        self.account_repository = account_repository

    def create_account(self, customer_id: int, name: str, email: str, phone_number: str) -> Account:
        """
        Create a new account for a customer and save it to the database.

        :param customer_id: The ID of the customer for whom the account is created.
        :param name: The name of the customer.
        :param email: The email of the customer.
        :param phone_number: The phone number of the customer.
        :return: The newly created account.
        """
        try:
            customer = Customer(customer_id, name, email, phone_number)
            account_number = self.__generate_account_number()
            account = Account(None, customer_id, account_number)
            account = self.account_repository.save_account(account, customer)
            return account
        except RuntimeError as e:
            raise RuntimeError(f"Account creation got failed. Error details : {e}")

    @staticmethod
    def __generate_account_number() -> int:
        """
        Generate a unique account number based on the current timestamp.

        :return: The generated account number.
        """
        account_id = str(datetime.timestamp(datetime.now())).replace(".", "")
        return int(account_id)
