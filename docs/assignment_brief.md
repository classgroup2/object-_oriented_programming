# Mobile Money / Airtime System

> A telecom-style service holds airtime credit against a customer's phone number.

---

## Overview & Requirements
Each account is identified by a phone number and an owner's name, and holds a balance in Uganda shillings. Customers can top up the account to add credit. Top-ups must be positive amounts; zero or negative top-ups are invalid.

The account can be charged for voice calls (a number of minutes at a given rate per minute) and for SMS messages (a number of messages at a cost per message). If the balance is too low to cover the charge, the operation must be refused.

Customers and agents must be able to check the remaining balance and to see a clear summary of the account (number, owner, and balance).

A demonstration should top up an account, make successful calls and send SMS, attempt at least one operation that fails through insufficient balance, and print the final state of the account.

---

## Evaluation Criteria
* **Object-Oriented Design:** The scenario is modelled with classes and objects, not only loose functions and global variables.
* **Encapsulation & Validation:** State and behaviour sit with sensible objects; invalid actions are refused rather than ignored.
* **Demonstration:** The demo runs easily and shows both successful use and at least one rejected case.
* **Extensibility:** Names and structure leave room to grow the same system in later topics.
