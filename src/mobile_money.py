# Group Members:
# Mulisa Docile -----S25B38/033
# Daniel Obar -----M25B38/014 
# Abi Mirembe -----M25B38/022
# Flavia Sherinah -----S25B38/031
# Victoria Marvis -----S25B38/014
# Mordecai Corey Kwezi -----M25B38/024
#the github link is https://github.com/classgroup2/object-_oriented_programming
from datetime import datetime
import uuid

# Raised when balance is too low for a charge.
class InsufficientBalanceError(Exception):
    pass

# Represents the person who owns a mobile money account.
class Customer:
    all_customers: list["Customer"] = []

    def __init__(self, name: str, phone_number: str, email: str):
        self.name = name
        self.phone_number = phone_number
        self.email = email
        Customer.all_customers.append(self)

    def get_details(self) -> str:
        return f"Name: {self.name}, Phone: {self.phone_number}, Email: {self.email}"

    @classmethod
    def print_all_customers(cls) -> None:
        if not cls.all_customers:
            print("No customers registered yet.")
            return
        for i, customer in enumerate(cls.all_customers, 1):
            print(f"{i}. {customer.get_details()}")


# Manages the customer's airtime balance and all financial operations.
class Account:
    def __init__(self, account_id: str, owner: Customer):
        self.account_id = account_id
        self.owner = owner
        self._balance = 0.0
        self.history = None   # set by TransactionHistory(account)

    def _record(self, transaction_type: str, amount: float) -> None:
        if self.history is not None:
            self.history.add_transaction(Transaction(transaction_type, amount))

    def top_up(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Top-up amount must be positive")
        self._balance += amount
        self._record("TOP_UP", amount)

    def withdraw(self, amount: float) -> float:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self._balance:
            raise InsufficientBalanceError(
                f"Insufficient balance. Need UGX {amount:,.0f}, have UGX {self._balance:,.0f}."
            )
        self._balance -= amount
        self._record("WITHDRAWAL", amount)
        return amount

    def charge_call(self, minutes: int, rate_per_minute: float) -> float:
        if minutes <= 0 or rate_per_minute <= 0:
            raise ValueError("Minutes and rate per minute must be positive")
        cost = minutes * rate_per_minute
        if cost > self._balance:
            raise InsufficientBalanceError(
                f"Insufficient balance. Need UGX {cost:,.0f}, have UGX {self._balance:,.0f}."
            )
        self._balance -= cost
        self._record("CALL", cost)
        return cost

    def charge_sms(self, count: int, cost_per_sms: float) -> float:
        if count <= 0 or cost_per_sms <= 0:
            raise ValueError("SMS count and cost per SMS must be positive")
        cost = count * cost_per_sms
        if cost > self._balance:
            raise InsufficientBalanceError(
                f"Insufficient balance. Need UGX {cost:,.0f}, have UGX {self._balance:,.0f}."
            )
        self._balance -= cost
        self._record("SMS", cost)
        return cost

    @property
    def balance(self) -> float:
        return self._balance

    def check_balance(self) -> float:
        return self._balance

    def summary(self) -> str:
        return (
            f"  Account ID  : {self.account_id}\n"
            f"  Phone Number: {self.owner.phone_number}\n"
            f"  Owner       : {self.owner.name}\n"
            f"  Balance     : UGX {self._balance:,.0f}"
        )


# Records a single financial event on an account.
class Transaction:
    def __init__(self, transaction_type: str, amount: float):
        self.transaction_id = str(uuid.uuid4())[:8]
        self.transaction_type = transaction_type
        self.amount = amount
        self.date_time = datetime.now().strftime("%Y-%m-%d %H:%M")

    def get_details(self) -> str:
        return f"{self.transaction_type:10} | UGX {self.amount:>7,.0f} | {self.date_time}"


# Stores and manages all transactions for an account.
class TransactionHistory:
    def __init__(self, account: Account):
        self.account = account
        self.transactions: list[Transaction] = []
        account.history = self

    def add_transaction(self, transaction: Transaction) -> None:
        self.transactions.append(transaction)

    def get_all(self) -> list[Transaction]:
        return self.transactions

    def get_last(self) -> Transaction | None:
        return self.transactions[-1] if self.transactions else None

    def print_history(self) -> None:
        if not self.transactions:
            print("No transactions yet.")
            return
        for i, t in enumerate(self.transactions, 1):
            print(f"{i}. {t.get_details()}")


# Represents a service agent who can perform operations on customer accounts.
class Agent:
    def __init__(self, name: str, agent_id: str, branch: str):
        self.name = name
        self.agent_id = agent_id
        self.branch = branch

    def top_up_account(self, account: Account, amount: float) -> None:
        account.top_up(amount)
        print(f"Agent {self.name} topped up UGX {amount:,.0f}")
        print(f"Balance: UGX {account.check_balance():,.0f}")

    def withdraw_from_account(self, account: Account, amount: float) -> None:
        account.withdraw(amount)
        print(f"Agent {self.name} processed a withdrawal of UGX {amount:,.0f}")
        print(f"Balance: UGX {account.check_balance():,.0f}")

    def check_account(self, account: Account) -> None:
        print(account.summary())
