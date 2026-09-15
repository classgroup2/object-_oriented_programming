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

class Transactions:
    pass

class TransactionHistory:
    pass

class Agent:
    pass