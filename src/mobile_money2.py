class Customer:
    all_accounts = []

    def __init__(self, name, contact, balance):
            self.name = name
            self.contact = contact
            self.balance = balance
            

    def __str__(self):
            return f"Account\nName: {self.name}\nContact: {self.contact}\nBalance: {self.balance}"    

    @classmethod
    def add_customer(cls):
        while True:
            name = input("Enter Customer Name: ")
            contact = input("Enter Contact Number: ")
        
            while True:
                balance_input = input("Enter starting balance or press enter for 0")
                if balance_input == "":
                    balance = 0
                    break
                try:
                    balance = float(balance_input)
                    break
                except ValueError:
                    print("Please enter a valid number")

            new_customer = cls(name, contact, balance)
            cls.all_accounts.append(new_customer)
            print(f"Customer {name} added successfully!")

            while True:
                try:
                    another_input = int(input("Add another customer?\n1. Yes\n2. No: "))
                    if another_input == 1:
                        break         # breaks the validation loop, goes back to outer while True
                    elif another_input == 2:
                        return        # exits add_customer entirely, back to main menu
                    else:
                        print("Please enter 1 or 2")
                except ValueError:
                    print("Please enter a valid number (1 or 2)")

    @classmethod
    def view_customers(cls):
        print("\n---Customer Accounts---")
        if not cls.all_accounts:
            print("No customers yet.")
        else:
            for c in cls.all_accounts:
                print(c)
                print()

def main_menu():
    while True:
        print("--------Telecom Service--------")
        print("1. Add customer")
        print("2. View customer list")
        print("3. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            Customer.add_customer()
        elif choice == "2":
            Customer.view_customers()
        elif choice == "3":
            print("Thank you!")
            break
        else:
            print("Invalid option, please choose 1, 2, or 3.\n")


main_menu()

            
"""Customer.add_customer()
for c in Customer.all_accounts:
     print(c)"""

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

#Mordecai: git This class stores and manages all transactions for an account
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