# Negative Error handling 
from src.mobile_money import MobileMoneyAccount, InsufficientBalanceError
def main():
    print("=" * 45)
    print("   MOBILE MONEY / AIRTIME SYSTEM DEMO 2")
    print("   (Negative / Edge Case Tests)")
    print("=" * 45)

    account = MobileMoneyAccount("0700123456", "Bob")
    print(f"\nNew account created for {account.owner_name} ({account.phone_number})")
    #This test is for the checking of a negative topup amount such as -50,000
    print("\n--- Test 1: Top-Up with Negative Amount (Expected to Fail) ---")
    try:
        account.top_up(-5000)
        print("Top-up succeeded (unexpected)")
    except ValueError as e:
        print(f"Top-up refused: {e}")
    # This is the test for when the top up is zero
    print("\n--- Test 2: Top-Up with Zero Amount (Expected to Fail) ---")
    try:
        account.top_up(0)
        print("Top-up succeeded (unexpected)")
    except ValueError as e:
        print(f"Top-up refused: {e}")
    # This is the test when the call is on an Empty balance 
    print("\n--- Test 3: Call on Empty Balance (Expected to Fail) ---")
    try:
        account.charge_call(minutes=1, rate_per_minute=200)
        print("Call succeeded (unexpected)")
    except InsufficientBalanceError as e:
        print(f"Call refused: {e}")
    # This is the test for sending an SMS on an Empty Balance
    print("\n--- Test 4: SMS on Empty Balance (Expected to Fail) ---")
    try:
        account.charge_sms(count=1, cost_per_sms=100)
        print("SMS succeeded (unexpected)")
    except InsufficientBalanceError as e:
        print(f"SMS refused: {e}")
    # This is the test for top-up a small Amount for future tests with different amounts
    print("\n--- Setup: Top-Up a Small Amount for Further Tests ---")
    account.top_up(1000)
    print(f"Topped up UGX 1,000 -> Balance: UGX {account.balance:,.0f}")
    # This is the test for when the call exceeds the balance
    print("\n--- Test 5: Call That Exceeds Balance (Expected to Fail) ---")
    try:
        account.charge_call(minutes=10, rate_per_minute=200)  # would cost 2000
        print("Call succeeded (unexpected)")
    except InsufficientBalanceError as e:
        print(f"Call refused: {e}")
    # This is the test for the SMS count that exceeds the balance 
    print("\n--- Test 6: SMS Count That Exceeds Balance (Expected to Fail) ---")
    try:
        account.charge_sms(count=50, cost_per_sms=100)  # would cost 5000
        print("SMS succeeded (unexpected)")
    except InsufficientBalanceError as e:
        print(f"SMS refused: {e}")
    # Test for negative minutes
    print("\n--- Test 7: Negative Minutes (Edge Case - No Validation Exists) ---")
    balance_before = account.balance
    account.charge_call(minutes=-10, rate_per_minute=200)
    print(f"Balance before: UGX {balance_before:,.0f} -> Balance after: UGX {account.balance:,.0f}")
    if account.balance > balance_before:
        print("WARNING: Negative minutes increased the balance instead of being rejected!")

    print("\n" + "=" * 45)
    print("   FINAL ACCOUNT STATE")
    print("=" * 45)
    print(account.summary())


if __name__ == "__main__":
    main()
