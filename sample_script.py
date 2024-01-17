from Infrastructure.account_repository import AccountRepository
from db.local_db_initialization import DatabaseInitializer
from Service import AccountOpening, GenerateStatements, AmountTransaction, TransactionFailedException



def entry_point():
    """
    Entry point of the banking system application.

    This function demonstrates the workflow of creating an account,
    performing transactions, and generating account statements.

    :return: None
    """
    # Initialize AccountRepository
    account_repository = AccountRepository()

    # Create an account using AccountOpening service
    account_client = AccountOpening(account_repository)
    customer_id = 9
    customer_name = "Customer_01"
    customer_email = "customer@example.com"
    customer_phone_number = "123-456-7890"
    try:
        account_ins = account_client.create_account(customer_id, customer_name, customer_email, customer_phone_number)

        # Perform transactions using AmountTransaction service
        account_transaction = AmountTransaction(account_repository)

        try:
            account_ins = account_transaction.make_transaction(account_ins.account_id, 1000, 'deposit')
            account_ins = account_transaction.make_transaction(account_ins.account_id, -2700, 'deposit')
        except TransactionFailedException as e:
            print(f"{str(e)}")
        
        try:
            account_ins = account_transaction.make_transaction(account_ins.account_id, 500, 'withdraw')
            account_ins = account_transaction.make_transaction(account_ins.account_id, -200, 'withdraw')
        except TransactionFailedException as e:
            print(f"{str(e)}")

        # Print the updated account balance
        print(f"Updated account balance {account_ins.get_balance()}")


        # Generate and print account statements using GenerateStatements service
        generate_statement = GenerateStatements(account_repository)
        statement_list = generate_statement.generate_account_statement(account_ins.account_id)
        print(statement_list)
    except RuntimeError as e:
        print(f"Getting exception. Exception details : {str(e)}")

if __name__ == "__main__":
    # Initialize the database
    database_initializer = DatabaseInitializer()
    database_initializer.initialize_db()

    # Execute the entry point of the application
    entry_point()