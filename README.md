# Object-Oriented Programming: Group Project (Topic 5)

## Group 9: Mobile Money / Airtime System

A telecom-style service that holds airtime credit against a customer's phone
number. An account is topped up by an agent, charged for voice calls and SMS,
and refuses any operation it cannot cover. Every successful operation is
recorded in a transaction history.

### Group Members
- Mulisa Docile
- Daniel Obar
- Abi Mirembe
- Flavia Sherinah
- Victoria Marvis
- Mordecai Corey Kwezi

---

## Repository Structure

```text
.
├── demo2.py                      # Runnable demonstration (the 10-step flow)
├── src/
│   ├── __init__.py
│   └── mobile_money2.py          # All five classes and the custom exception
├── tests/
│   ├── __init__.py
│   └── test_mobile_money2.py     # Unit tests for all five classes
├── docs/
│   └── assignment_brief.md       # Assignment brief and class specification
├── .gitignore
└── README.md
```

---

## How to Run

Run both commands from the project root folder (the folder holding `demo2.py`).

Demonstration:

```bash
python demo2.py
```

Unit tests:

```bash
python -m unittest discover -s tests -t .
```

Requires Python 3.9 or newer. There are no external dependencies.

---

## Classes

| Class | Responsibility |
|-------|----------------|
| `Customer` | Holds the owner's name, phone number and email; every customer created is tracked in `Customer.all_customers` |
| `Account` | Holds the balance and performs top-ups, withdrawals, call charges and SMS charges |
| `Transaction` | One financial event, with its own generated ID and timestamp |
| `TransactionHistory` | Stores and prints all transactions for one account |
| `Agent` | Tops up or withdraws from a customer's account and prints the account summary |
| `InsufficientBalanceError` | Raised when the balance cannot cover a charge or a withdrawal |

### Design Notes
- The balance is private (`_balance`) and is only reachable through
  `top_up`, `withdraw`, `charge_call`, `charge_sms`, `check_balance` and `summary`.
- `TransactionHistory(account)` attaches itself to the account, so the account
  logs each successful operation itself. A refused operation raises before any
  logging, so it never reaches the history.
- Invalid actions are refused rather than ignored: a top-up or withdrawal of
  zero or less raises `ValueError`, and a withdrawal or charge larger than the
  balance raises `InsufficientBalanceError`.
- `Customer.all_customers` is a class-level list that every new `Customer`
  appends itself to on construction, so the group can grow the customer base
  without a separate registry class. `Customer.print_all_customers()` prints
  it in the same style as `TransactionHistory.print_history()`.

---

## OOP Principles Demonstrated
- **Classes and Objects:** five classes model the customer, account, transaction, history and agent.
- **Encapsulation:** the balance is private and changed only through account methods that validate first.
- **Abstraction:** callers use `charge_call` and `charge_sms` without knowing how the cost or the logging is handled.
- **Composition:** an `Account` holds a `Customer` and a `TransactionHistory`, which holds `Transaction` objects.
