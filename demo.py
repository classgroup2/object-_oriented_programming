# Group Members:
# Mulisa Docile -----S25B38/033
# Daniel Obar -----M25B38/014 
# Abi Mirembe -----M25B38/022
# Flavia Sherinah -----S25B38/031
# Victoria Marvis -----S25B38/014
# Mordecai Corey Kwezi -----M25B38/024

from src.mobile_money import (
    Customer,
    Account,
    TransactionHistory,
    Agent,
    InsufficientBalanceError,
)


def main():
    print("=" * 45)
    print("   MOBILE MONEY / AIRTIME SYSTEM DEMO")
    print("=" * 45)

    customer = Customer("Mulisa Docile", "0700123456", "mulisa@email.com")
    print(f"\nCustomer created: {customer.get_details()}")

    account = Account("ACC001", customer)
    history = TransactionHistory(account)
    print(f"Account created: {account.account_id}")

    agent = Agent("Daniel Obar", "AGT001", "Kampala Branch")
    print(f"Agent: {agent.name} ({agent.agent_id}) - {agent.branch}")

    print("\n--- Agent Top-Up ---")
    agent.top_up_account(account, 50000)

    print("\n--- Voice Call ---")
    cost = account.charge_call(minutes=30, rate_per_minute=200)
    print(f"30 min call @ UGX 200/min = UGX {cost:,.0f}")
    print(f"Balance: UGX {account.balance:,.0f}")

    print("\n--- Send SMS ---")
    cost = account.charge_sms(count=5, cost_per_sms=100)
    print(f"5 SMS @ UGX 100 each = UGX {cost:,.0f}")
    print(f"Balance: UGX {account.balance:,.0f}")

    print("\n--- Agent Withdrawal ---")
    agent.withdraw_from_account(account, 5000)

    print("\n--- Insufficient Balance (Expected to Fail) ---")
    try:
        account.charge_call(minutes=300, rate_per_minute=200)
        print("Call succeeded (unexpected)")
    except InsufficientBalanceError as e:
        print(f"Call refused: {e}")

    print("\n" + "=" * 45)
    print("   TRANSACTION HISTORY")
    print("=" * 45)
    history.print_history()

    print("\n" + "=" * 45)
    print("   ALL REGISTERED CUSTOMERS")
    print("=" * 45)
    Customer.print_all_customers()

    print("\n" + "=" * 45)
    print("   FINAL ACCOUNT STATE")
    print("=" * 45)
    agent.check_account(account)


if __name__ == "__main__":
    main()
