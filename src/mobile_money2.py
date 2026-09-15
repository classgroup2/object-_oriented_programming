class Customer:
    pass

class Account:
    pass

class Transaction:
    pass

#This class stores and manages all transactions for an account
class TransactionHistory:
    
    def __init__(self, account: Account):
        self.account = account
        self.transactions: list[Transaction] = []

    def add_transaction(self, transaction:Transaction):
        self.transactions.append(transaction)

    def get_all(self):  #This method just returns a Transaction list
        return self.transactions

    def get_last(self): # This method returns either a Transaction or nothing as per the conditions below 
        return self.transactions[-1] if self.transactions else None

    def print_history(self): #This method returns transaction History
        if not self.transactions:
            print("No transactions yet.")
            return
        for i, t in enumerate(self.transactions, 1):
            print(f"{i}. {t.get_details()}")

class Agent:
    pass