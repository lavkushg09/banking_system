import os
import unittest
import json
from unittest.mock import Mock, patch
from datetime import datetime
from db.db_client import DatabaseConnection
from Domain.account import Account
from Domain.customer import Customer
from Infrastructure.account_repository import AccountRepository
from Service import AmountTransaction, AccountOpening, GenerateStatements

class TestAccountRepository(unittest.TestCase):
    def setUp(self):
        self.db_filename = 'test.db'
        # Create necessary tables
        
        self.db_connection = DatabaseConnection(self.db_filename)
        self.create_tables()

        self.account_repository = AccountRepository(self.db_connection)
        self.account_client = AccountOpening(self.account_repository)
        self.account_ins = self.account_client.create_account(35, 'test_cl_id', 'lazy@gmail.com', '123456789')
        self.amount_transaction = AmountTransaction(self.account_repository)
        self.generate_statements = GenerateStatements(self.account_repository)


    def tearDown(self):
        # Delete the test database after the test run
        if os.path.exists(self.db_filename):
            os.remove(self.db_filename)

    def create_tables(self):
        connection = self.db_connection.create_db_connection()
        cursor = connection.cursor()

        cursor.executescript('''
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
        ''')
        connection.commit()
        connection.close()

    def test_save_account(self):
        customer = Customer(1, "John Doe", "john@example.com", "123-456-7890")
        account = Account(None, 1, 12345678)
        saved_account = self.account_repository.save_account(account, customer)

        self.assertIsNotNone(saved_account.account_id)
        self.assertEqual(saved_account.customer_id, 1)
        self.assertEqual(saved_account.account_number, 12345678)

    def test_find_account_by_id(self):
        customer = Customer(1, "Jane Doe", "jane@example.com", "987-654-3210")
        account = Account(None, 1, 12345678)
        saved_account = self.account_repository.save_account(account, customer)

        found_account = self.account_repository.find_account_by_id(saved_account.account_id)

        self.assertIsNotNone(found_account)
        self.assertEqual(found_account.account_id, saved_account.account_id)
        self.assertEqual(found_account.account_number, saved_account.account_number)

    def test_find_accounts_by_customer_id(self):
        customer = Customer(1, "Bob Smith", "bob@example.com", "111-222-3333")
        account1 = Account(None, 1, 12345678)
        account2 = Account(None, 2, 123456780)
        self.account_repository.save_account(account1, customer)
        self.account_repository.save_account(account2, customer)

        found_accounts = self.account_repository.find_accounts_by_customer_id(1)

        self.assertIsNotNone(found_accounts)

    def test_make_transaction_deposit(self):
        initial_balance = self.account_ins.get_balance()
        amount = 50.0
        transaction_type = "deposit"
        result_account = self.amount_transaction.make_transaction(self.account_ins.account_id, 
                                                                  amount, transaction_type)
        self.assertEqual(result_account.account_id, self.account_ins.account_id)
        self.assertEqual(result_account.account_number, self.account_ins.account_number)
        self.assertEqual(result_account.balance, initial_balance + amount)

    def test_make_transaction_withdrawal(self):
        initial_balance = self.account_ins.get_balance()
        deposit_amount = 50.0
        transaction_type = "deposit"
        
        result_account = self.amount_transaction.make_transaction(self.account_ins.account_id, 
                                                                  deposit_amount, transaction_type)
        transaction_type = "withdraw"
        withdrawal_acount = 25
        result_account = self.amount_transaction.make_transaction(self.account_ins.account_id, 
                                                                  withdrawal_acount, transaction_type)
        self.assertEqual(result_account.account_id, self.account_ins.account_id)
        self.assertEqual(result_account.account_number, self.account_ins.account_number)
        self.assertEqual(result_account.balance, initial_balance + deposit_amount-withdrawal_acount)

    def test_make_transaction_invalid_type(self):
        deposit_amount = 50.0
        transaction_type = "depositamount"
        with self.assertRaises(ValueError):
            self.amount_transaction.make_transaction(self.account_ins.account_id, deposit_amount, transaction_type)

    def test_make_transaction_invalid_amount_withdrawal(self):
        deposit_amount = 150.0
        transaction_type = "withdraw"
        with self.assertRaises(ValueError):
            self.amount_transaction.make_transaction(self.account_ins.account_id, deposit_amount, transaction_type)

    def test_generate_account_statement(self):
        statement = self.generate_statements.generate_account_statement(self.account_ins.account_id)
        
        self.assertEqual(json.loads(statement),[])
        deposit_amount = 1100.0
        withdrawal_acount = 200
        deposit_transaction_type = "deposit"
        withdrawal_transaction_type = "withdraw"
        self.amount_transaction.make_transaction(self.account_ins.account_id, deposit_amount, deposit_transaction_type)
        self.amount_transaction.make_transaction(self.account_ins.account_id, withdrawal_acount, withdrawal_transaction_type)
        statements = self.generate_statements.generate_account_statement(self.account_ins.account_id)
        data_list = json.loads(statements)
        for data in data_list:
            if data['type'] == deposit_transaction_type:
                self.assertEqual(data['amount'], deposit_amount)
            elif data['type'] == withdrawal_transaction_type:
                self.assertEqual(data['amount'], withdrawal_acount)
        self.assertEqual(len(data_list), 2)

if __name__ == '__main__':
    unittest.main()
