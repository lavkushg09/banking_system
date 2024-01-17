class TransactionFailedException(Exception):
    def __init__(self, message="Transaction failed"):
        self.message = message
        super().__init__(self.message)
