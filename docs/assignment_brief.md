# Mobile Money / Airtime System

> A telecom-style service holds airtime credit against a customer's phone number.

---

## Overview & Requirements
Each account is identified by a phone number and an owner's name, and holds a balance in Uganda shillings. Customers can top up the account to add credit. Top-ups must be positive amounts; zero or negative top-ups are invalid.

The account can be charged for voice calls (a number of minutes at a given rate per minute) and for SMS messages (a number of messages at a cost per message). If the balance is too low to cover the charge, the operation must be refused.

Customers and agents must be able to check the remaining balance and to see a clear summary of the account (number, owner, and balance).

A demonstration should top up an account, make successful calls and send SMS, attempt at least one operation that fails through insufficient balance, and print the final state of the account.

---

## System Classes

### 1. Customer
Represents the person who owns a mobile money account.

| Attribute | Type | Description |
|-----------|------|-------------|
| `name` | str | Full name of the customer |
| `phone_number` | str | Registered phone number (unique ID) |
| `email` | str | Customer's email address |

| Method | Description |
|--------|-------------|
| `get_details()` | Returns formatted string with name, phone, and email |

---

### 2. Account
Manages the customer's airtime balance and all financial operations.

| Attribute | Type | Description |
|-----------|------|-------------|
| `account_id` | str | Unique account identifier |
| `owner` | Customer | The customer who owns this account |
| `_balance` | float | Current balance in UGX (private, starts at 0) |

| Method | Description |
|--------|-------------|
| `top_up(amount)` | Adds credit; rejects if amount <= 0 |
| `charge_call(minutes, rate_per_minute)` | Deducts cost of a call; rejects if insufficient balance |
| `charge_sms(count, cost_per_sms)` | Deducts cost of SMS; rejects if insufficient balance |
| `check_balance()` | Returns current balance |
| `summary()` | Returns formatted account summary |

---

### 3. Transaction
Records a single financial event on an account.

| Attribute | Type | Description |
|-----------|------|-------------|
| `transaction_id` | str | Unique transaction identifier |
| `transaction_type` | str | One of: "TOP_UP", "CALL", "SMS" |
| `amount` | float | Amount debited or credited in UGX |
| `date_time` | str | Timestamp of the transaction |

| Method | Description |
|--------|-------------|
| `get_details()` | Returns formatted string with type, amount, and date |

---

### 4. TransactionHistory
Stores and manages all transactions for an account.

| Attribute | Type | Description |
|-----------|------|-------------|
| `account` | Account | The account this history belongs to |
| `transactions` | list | List of all Transaction objects |

| Method | Description |
|--------|-------------|
| `add_transaction(transaction)` | Appends a transaction to the list |
| `get_all()` | Returns all transactions |
| `get_last()` | Returns the most recent transaction |
| `print_history()` | Prints a formatted list of all transactions |

---

### 5. Agent
Represents a service agent who can perform operations on customer accounts.

| Attribute | Type | Description |
|-----------|------|-------------|
| `name` | str | Agent's full name |
| `agent_id` | str | Unique agent identifier |
| `branch` | str | Branch where the agent works |

| Method | Description |
|--------|-------------|
| `top_up_account(account, amount)` | Tops up a customer's account and logs the transaction |
| `check_account(account)` | Prints the account summary |

---

## Step-by-Step System Flow

### Step 1: Create a Customer
```
customer = Customer("Mulisa Docile", "0700123456", "mulisa@email.com")
```
A new customer is registered with name, phone number, and email.

### Step 2: Create an Account for the Customer
```
account = Account("ACC001", customer)
```
An account is created and linked to the customer. Balance starts at UGX 0.

### Step 3: Create a Transaction History for the Account
```
history = TransactionHistory(account)
```
An empty transaction history is attached to the account.

### Step 4: Agent Tops Up the Account
```
agent = Agent("Daniel Obar", "AGT001", "Kampala Branch")
agent.top_up_account(account, 50, 000)
```
- Account balance increases by UGX 50,000
- A TOP_UP transaction is recorded with amount and timestamp

### Step 5: Customer Makes a Voice Call
```
account.charge_call(minutes=30, rate_per_minute=200)
```
- Cost = 30 x 200 = UGX 6,000
- Balance decreases by UGX 6,000
- A CALL transaction is recorded

### Step 6: Customer Sends SMS
```
account.charge_sms(count=5, cost_per_sms=100)
```
- Cost = 5 x 100 = UGX 500
- Balance decreases by UGX 500
- An SMS transaction is recorded

### Step 7: Attempt an Operation with Insufficient Balance
```
account.charge_call(minutes=300, rate_per_minute=200)
```
- Cost = 300 x 200 = UGX 60,000
- Balance is only UGX 43,500
- Operation is REFUSED, InsufficientBalanceError is raised
- No transaction is recorded

### Step 8: Check Balance
```
account.check_balance()
```
Returns the current balance: UGX 43,500

### Step 9: View Transaction History
```
history.print_history()
```
Shows all successful transactions: top-up, call, SMS (the failed call is not recorded).

### Step 10: View Final Account Summary
```
account.summary()
```
Displays phone number, owner name, and final balance.

---

## Sample Demo Output

```
=============================================
   MOBILE MONEY / AIRTIME SYSTEM DEMO
=============================================

Customer: Mulisa Docile (0700123456)
Agent: Daniel Obar (AGT001) - Kampala Branch

--- Top-Up ---
Agent Daniel Obar topped up UGX 50,000
Balance: UGX 50,000

--- Voice Call ---
30 min call @ UGX 200/min = UGX 6,000
Balance: UGX 44,000

--- Send SMS ---
5 SMS @ UGX 100 each = UGX 500
Balance: UGX 43,500

--- Insufficient Balance (Expected to Fail) ---
Call refused: Insufficient balance. Need UGX 60,000, have UGX 43,500.

--- Transaction History ---
1. TOP_UP   | UGX 50,000 | 2026-09-14 10:00
2. CALL     | UGX  6,000 | 2026-09-14 10:05
3. SMS      | UGX    500 | 2026-09-14 10:10

--- Final Account Summary ---
  Account ID  : ACC001
  Phone Number: 0700123456
  Owner       : Mulisa Docile
  Balance     : UGX 43,500
```

---

## Evaluation Criteria
* **Object-Oriented Design:** The scenario is modelled with classes and objects, not only loose functions and global variables.
* **Encapsulation & Validation:** State and behaviour sit with sensible objects; invalid actions are refused rather than ignored.
* **Demonstration:** The demo runs easily and shows both successful use and at least one rejected case.
* **Extensibility:** Names and structure leave room to grow the same system in later topics.
