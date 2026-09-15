class Customer:
    pass

class Account:
    pass
class Transaction:
    def __init__(self, transaction_id, transaction_type, amount, date_time):
        self.transaction_id = transaction_id
        self.transaction_type = transaction_type
        self.amount = amount
        self.date_time = date_time

    def get_details(self):
        return f"Transaction ID: {self.transaction_id}, " \
               f"Type: {self.transaction_type}, " \
               f"Amount: UGX {self.amount}, " \
               f"Date: {self.date_time}"

class TransactionHistory:
    pass

class Agent:
    pass