# Group Members:
# Mulisa Docile
# Daniel Obar
# Abi Mirembe
# Flavia Sherinah
# Victoria Marvis
# Mordecai Corey Kwezi 

from src.mobile_money import MobileMoneyAccount, InsufficientBalanceError


def main():
    print("=" * 45)
    print("   MOBILE MONEY / AIRTIME SYSTEM DEMO")
    print("=" * 45)

    account = MobileMoneyAccount("0700123456", "Alice")
    print(f"\nNew account created for {account.owner_name} ({account.phone_number})")

    print("\n--- Top-Up ---")
    account.top_up(50000)
    print(f"Topped up UGX 50,000 -> Balance: UGX {account.balance:,.0f}")

    print("\n--- Voice Call ---")
    account.charge_call(minutes=30, rate_per_minute=200)
    print(f"30 min call @ UGX 200/min -> Balance: UGX {account.balance:,.0f}")

    print("\n--- Send SMS ---")
    account.charge_sms(count=5, cost_per_sms=100)
    print(f"5 SMS @ UGX 100 each -> Balance: UGX {account.balance:,.0f}")

    print("\n--- Insufficient Balance (Expected to Fail) ---")
    try:
        account.charge_call(minutes=300, rate_per_minute=200)
        print("Call succeeded (unexpected)")
    except InsufficientBalanceError as e:
        print(f"Call refused: {e}")

    print("\n" + "=" * 45)
    print("   FINAL ACCOUNT STATE")
    print("=" * 45)
    print(account.summary())


if __name__ == "__main__":
    main()
