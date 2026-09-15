class Customer:
    pass

class Account:
    pass

class Transaction:
    pass

#This class stores andmanages all transactions for an account
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
#obar
class Agent:
    def __init__(self, name, agent_id, branch):
        self._name = name
        self._agent_id = agent_id
        self._branch = branch
        self._transaction_log = []

    @property
    def name(self):
        return self._name

    @property
    def agent_id(self):
        return self._agent_id

    @property
    def branch(self):
        return self._branch

    @property
    def transaction_log(self):
        return self._transaction_log

    def top_up_account(self, account, amount):
        if amount <= 0:
            raise ValueError("Top-up amount must be positive.")

        account.top_up(amount)
        entry = (
            f"Agent {self._name} ({self._agent_id}) topped up "
            f"{account.owner_name}'s account with UGX {amount:,.0f}."
        )
        self._transaction_log.append(entry)
        print(f"[{self._branch}] {entry} New Balance: UGX {account.balance:,.0f}")

    def check_account(self, account):
        print(account.summary())