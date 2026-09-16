# Group Members:
# Mulisa Docile
# Daniel Obar
# Abi Mirembe
# Flavia Sherinah
# Victoria Marvis
# Mordecai Corey Kwezi

from src.mobile_money2 import (
    Customer, Account, TransactionHistory,
    Agent, InsufficientBalanceError
)


def main():
    print("=" * 45)
    print("   MOBILE MONEY / AIRTIME SYSTEM DEMO")
    print("=" * 45)
    print()

    # Step 1: Create the customer
    customer = Customer("Mulisa Docile", "0700123456", "mulisa@email.com")
    print(f"Customer: {customer.get_details()}")

    # Step 2: Create the account (balance starts at UGX 0)
    account = Account("ACC001", customer)

    # Step 3: Attach a transaction history to the account
    history = TransactionHistory(account)

    # Step 4: Agent tops up the account
    agent = Agent("Daniel Obar", "AGT001", "Kampala Branch")
    print(f"Agent: {agent.name} ({agent.agent_id}) - {agent.branch}")
    print()
    print("--- Top-Up ---")
    agent.top_up_account(account, 50_000)
    print()

    # Step 5: Successful voice call
    print("--- Voice Call ---")
    try:
        cost = account.charge_call(minutes=30, rate_per_minute=200)
        print(f"30 min call @ UGX 200/min = UGX {cost:,.0f}")
        print(f"Balance: UGX {account.check_balance():,.0f}")
    except InsufficientBalanceError as e:
        print(f"Call refused: {e}")
    print()

    # Step 6: Successful SMS
    print("--- Send SMS ---")
    try:
        cost = account.charge_sms(count=5, cost_per_sms=100)
        print(f"5 SMS @ UGX 100 each = UGX {cost:,.0f}")
        print(f"Balance: UGX {account.check_balance():,.0f}")
    except InsufficientBalanceError as e:
        print(f"SMS refused: {e}")
    print()

    # Step 7: Operation that must be refused (insufficient balance)
    print("--- Insufficient Balance (Expected to Fail) ---")
    try:
        cost = account.charge_call(minutes=300, rate_per_minute=200)
        print(f"Call succeeded, cost UGX {cost:,.0f}")
    except InsufficientBalanceError as e:
        print(f"Call refused: {e}")
    print()

    # Step 8: Check the balance
    print(f"Current balance: UGX {account.check_balance():,.0f}")
    print(f"Last transaction: {history.get_last().get_details()}")
    print()

    # Step 9: Transaction history (the refused call is not recorded)
    print("--- Transaction History ---")
    history.print_history()
    print(f"Total transactions recorded: {len(history.get_all())}")
    print()

    # Step 10: Final account summary, printed by the agent
    print("--- Final Account Summary ---")
    agent.check_account(account)


if __name__ == "__main__":
    main()
