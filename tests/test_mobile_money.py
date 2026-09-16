# Group Members:
# Mulisa Docile -----S25B38/033
# Daniel Obar -----M25B38/014 
# Abi Mirembe -----M25B38/022
# Flavia Sherinah -----S25B38/031
# Victoria Marvis -----S25B38/014
# Mordecai Corey Kwezi -----M25B38/024

import unittest
from src.mobile_money import (
    Customer,
    Account,
    Transaction,
    TransactionHistory,
    Agent,
    InsufficientBalanceError,
)


class TestCustomer(unittest.TestCase):
    def setUp(self):
        Customer.all_customers.clear()
        self.customer = Customer("Mulisa Docile", "0700123456", "mulisa@email.com")

    def test_creation(self):
        self.assertEqual(self.customer.name, "Mulisa Docile")
        self.assertEqual(self.customer.phone_number, "0700123456")
        self.assertEqual(self.customer.email, "mulisa@email.com")

    def test_get_details(self):
        details = self.customer.get_details()
        self.assertIn("Mulisa Docile", details)
        self.assertIn("0700123456", details)
        self.assertIn("mulisa@email.com", details)

    def test_all_customers_tracking(self):
        self.assertIn(self.customer, Customer.all_customers)
        self.assertEqual(len(Customer.all_customers), 1)

    def test_multiple_customers(self):
        c2 = Customer("Daniel Obar", "0700987654", "daniel@email.com")
        self.assertEqual(len(Customer.all_customers), 2)


class TestAccount(unittest.TestCase):
    def setUp(self):
        self.customer = Customer("Alice", "0700111222", "alice@email.com")
        self.account = Account("ACC001", self.customer)

    def test_initial_balance(self):
        self.assertEqual(self.account.balance, 0)

    def test_top_up(self):
        self.account.top_up(50000)
        self.assertEqual(self.account.balance, 50000)

    def test_top_up_negative_raises(self):
        with self.assertRaises(ValueError):
            self.account.top_up(-1000)

    def test_top_up_zero_raises(self):
        with self.assertRaises(ValueError):
            self.account.top_up(0)

    def test_charge_call(self):
        self.account.top_up(10000)
        cost = self.account.charge_call(minutes=10, rate_per_minute=200)
        self.assertEqual(cost, 2000)
        self.assertEqual(self.account.balance, 8000)

    def test_charge_call_insufficient_balance(self):
        self.account.top_up(500)
        with self.assertRaises(InsufficientBalanceError):
            self.account.charge_call(minutes=10, rate_per_minute=200)
        self.assertEqual(self.account.balance, 500)

    def test_charge_call_invalid_inputs(self):
        self.account.top_up(10000)
        with self.assertRaises(ValueError):
            self.account.charge_call(minutes=-1, rate_per_minute=200)

    def test_charge_sms(self):
        self.account.top_up(5000)
        cost = self.account.charge_sms(count=10, cost_per_sms=100)
        self.assertEqual(cost, 1000)
        self.assertEqual(self.account.balance, 4000)

    def test_charge_sms_insufficient_balance(self):
        self.account.top_up(500)
        with self.assertRaises(InsufficientBalanceError):
            self.account.charge_sms(count=10, cost_per_sms=100)
        self.assertEqual(self.account.balance, 500)

    def test_withdraw(self):
        self.account.top_up(10000)
        amount = self.account.withdraw(3000)
        self.assertEqual(amount, 3000)
        self.assertEqual(self.account.balance, 7000)

    def test_withdraw_insufficient_balance(self):
        self.account.top_up(500)
        with self.assertRaises(InsufficientBalanceError):
            self.account.withdraw(1000)
        self.assertEqual(self.account.balance, 500)

    def test_withdraw_negative_raises(self):
        self.account.top_up(10000)
        with self.assertRaises(ValueError):
            self.account.withdraw(-500)

    def test_summary(self):
        result = self.account.summary()
        self.assertIn("ACC001", result)
        self.assertIn("0700111222", result)
        self.assertIn("Alice", result)


class TestTransaction(unittest.TestCase):
    def test_creation(self):
        t = Transaction("TOP_UP", 5000)
        self.assertEqual(t.transaction_type, "TOP_UP")
        self.assertEqual(t.amount, 5000)
        self.assertIsNotNone(t.transaction_id)
        self.assertIsNotNone(t.date_time)

    def test_get_details(self):
        t = Transaction("CALL", 2000)
        details = t.get_details()
        self.assertIn("CALL", details)
        self.assertIn("2,000", details)


class TestTransactionHistory(unittest.TestCase):
    def setUp(self):
        Customer.all_customers.clear()
        self.customer = Customer("Bob", "0700333444", "bob@email.com")
        self.account = Account("ACC002", self.customer)
        self.history = TransactionHistory(self.account)

    def test_initially_empty(self):
        self.assertEqual(len(self.history.get_all()), 0)

    def test_add_transaction(self):
        t = Transaction("TOP_UP", 5000)
        self.history.add_transaction(t)
        self.assertEqual(len(self.history.get_all()), 1)

    def test_get_last(self):
        t1 = Transaction("TOP_UP", 5000)
        t2 = Transaction("CALL", 1000)
        self.history.add_transaction(t1)
        self.history.add_transaction(t2)
        self.assertEqual(self.history.get_last().transaction_type, "CALL")

    def test_get_last_empty(self):
        self.assertIsNone(self.history.get_last())

    def test_auto_record_on_top_up(self):
        self.account.top_up(10000)
        self.assertEqual(len(self.history.get_all()), 1)
        self.assertEqual(self.history.get_all()[0].transaction_type, "TOP_UP")

    def test_auto_record_on_call(self):
        self.account.top_up(10000)
        self.account.charge_call(minutes=5, rate_per_minute=200)
        self.assertEqual(len(self.history.get_all()), 2)
        self.assertEqual(self.history.get_all()[1].transaction_type, "CALL")

    def test_auto_record_on_sms(self):
        self.account.top_up(10000)
        self.account.charge_sms(count=3, cost_per_sms=100)
        self.assertEqual(len(self.history.get_all()), 2)
        self.assertEqual(self.history.get_all()[1].transaction_type, "SMS")

    def test_no_record_on_failed_operation(self):
        self.account.top_up(500)
        with self.assertRaises(InsufficientBalanceError):
            self.account.charge_call(minutes=10, rate_per_minute=200)
        self.assertEqual(len(self.history.get_all()), 1)


class TestAgent(unittest.TestCase):
    def setUp(self):
        Customer.all_customers.clear()
        self.customer = Customer("Charlie", "0700555666", "charlie@email.com")
        self.account = Account("ACC003", self.customer)
        self.history = TransactionHistory(self.account)
        self.agent = Agent("Daniel Obar", "AGT001", "Kampala Branch")

    def test_creation(self):
        self.assertEqual(self.agent.name, "Daniel Obar")
        self.assertEqual(self.agent.agent_id, "AGT001")
        self.assertEqual(self.agent.branch, "Kampala Branch")

    def test_top_up_account(self):
        self.agent.top_up_account(self.account, 50000)
        self.assertEqual(self.account.balance, 50000)

    def test_check_account(self):
        self.account.top_up(10000)
        self.agent.check_account(self.account)

    def test_withdraw_from_account(self):
        self.account.top_up(10000)
        self.agent.withdraw_from_account(self.account, 3000)
        self.assertEqual(self.account.balance, 7000)


if __name__ == "__main__":
    unittest.main()
