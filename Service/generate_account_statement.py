import json


class GenerateStatements:
    def __init__(self, account_repository):
        """
        Initialize a GenerateStatements object.

        The GenerateStatements class is responsible for generating account statements based on transaction records.

        :param account_repository: The repository for interacting with accounts and transactions in the database.
        :return: None
        """
        self.account_repository = account_repository

    def generate_account_statement(self, account_id: int) -> json.dumps:
        """
        Generate an account statement in JSON format based on transaction records.

        :param account_id: The ID of the account for which the statement is generated.
        :return: A JSON-formatted string representing the account statement.
        """
        statement_list = []
        connection = self.account_repository.db_connection.create_db_connection()
        data_rows, _ = self.account_repository.db_connection.execute_query(
            'SELECT * FROM transactions WHERE account_id=?;',
            (account_id,), connection)
        if data_rows:
            for row in data_rows:
                statement_list.append({
                    'account_id': row[1],
                    'amount': row[2],
                    'type': row[3],
                    'time': row[4],
                })
            return json.dumps(statement_list, indent=2)
        return json.dumps([], indent=2)
