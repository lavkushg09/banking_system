class Customer:
    def __init__(self, customer_id: int, name: str, phone_number: str, email: str):
        """
        Initialize a Customer object.

        :param customer_id: Unique identifier for the customer.
        :param name: Name of the customer.
        :param phone_number: Phone number of the customer.
        :param email: Email address of the customer.
        """
        self.customer_id = customer_id
        self.name = name
        self.phone_number = phone_number
        self.email = email
