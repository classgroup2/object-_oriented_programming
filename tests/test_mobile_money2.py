# Group Members:
# Mulisa Docile
# Daniel Obar
# Abi Mirembe
# Flavia Sherinah
# Victoria Marvis
# Mordecai Corey Kwezi

import unittest

from src.mobile_money2 import (
    Customer, Account, Transaction, TransactionHistory,
    Agent, InsufficientBalanceError
)


class TestCustomer(unittest.TestCase):
    def setUp(self):
        self.customer = Customer("Alice Nakato", "0700123456", "alice@email.com")

    def test_attributes(self):
        self.assertEqual(self.customer.name, "Alice Nakato")
        self.assertEqual(self.customer.phone_number, "0700123456")
        self.assertEqual(self.customer.email, "alice@email.com")

    def test_get_details(self):
        details = self.customer.get_details()
        self.assertIn("Alice Nakato", details)
        self.assertIn("0700123456", details)
        self.assertIn("alice@email.com", details)

    def test_new_customer_is_added_to_all_customers(self):
        self.assertIn(self.customer, Customer.all_customers)

    def test_multiple_customers_are_all_tracked(self):
        before = len(Customer.all_customers)
        second = Customer("Bob Okello", "0700333444", "bob@email.com")
        third = Customer("Carol Namutebi", "0700555666", "carol@email.com")
        self.assertEqual(len(Customer.all_customers), before + 2)
        self.assertIn(second, Customer.all_customers)
        self.assertIn(third, Customer.all_customers)


class TestAccount(unittest.TestCase):
    def setUp(self):
        self.customer = Customer("Alice Nakato", "0700123456", "alice@email.com")
        self.account = Account("ACC001", self.customer)

    def test_initial_balance_is_zero(self):
        self.assertEqual(self.account.check_balance(), 0)

    def test_top_up(self):
        self.account.top_up(10000)
        self.assertEqual(self.account.check_balance(), 10000)

    def test_multiple_top_ups(self):
        self.account.top_up(5000)
        self.account.top_up(3000)
        self.assertEqual(self.account.check_balance(), 8000)

    def test_top_up_zero_raises(self):
        with self.assertRaises(ValueError):
            self.account.top_up(0)

    def test_top_up_negative_raises(self):
        with self.assertRaises(ValueError):
            self.account.top_up(-500)

    def test_charge_call(self):
        self.account.top_up(10000)
        cost = self.account.charge_call(minutes=10, rate_per_minute=200)
        self.assertEqual(cost, 2000)
        self.assertEqual(self.account.check_balance(), 8000)

    def test_charge_sms(self):
        self.account.top_up(5000)
        cost = self.account.charge_sms(count=10, cost_per_sms=100)
        self.assertEqual(cost, 1000)
        self.assertEqual(self.account.check_balance(), 4000)

    def test_charge_call_insufficient_balance(self):
        self.account.top_up(500)
        with self.assertRaises(InsufficientBalanceError):
            self.account.charge_call(minutes=10, rate_per_minute=200)
        self.assertEqual(self.account.check_balance(), 500)

    def test_charge_sms_insufficient_balance(self):
        self.account.top_up(500)
        with self.assertRaises(InsufficientBalanceError):
            self.account.charge_sms(count=10, cost_per_sms=100)
        self.assertEqual(self.account.check_balance(), 500)

    def test_charge_call_rejects_invalid_minutes(self):
        self.account.top_up(10000)
        with self.assertRaises(ValueError):
            self.account.charge_call(minutes=0, rate_per_minute=200)

    def test_charge_sms_rejects_invalid_count(self):
        self.account.top_up(10000)
        with self.assertRaises(ValueError):
            self.account.charge_sms(count=-1, cost_per_sms=100)

    def test_withdraw(self):
        self.account.top_up(10000)
        withdrawn = self.account.withdraw(4000)
        self.assertEqual(withdrawn, 4000)
        self.assertEqual(self.account.check_balance(), 6000)

    def test_withdraw_zero_raises(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(0)

    def test_withdraw_negative_raises(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(-500)

    def test_withdraw_insufficient_balance(self):
        self.account.top_up(500)
        with self.assertRaises(InsufficientBalanceError):
            self.account.withdraw(1000)
        self.assertEqual(self.account.check_balance(), 500)

    def test_balance_is_private(self):
        self.assertFalse(hasattr(self.account, "balance"))
        self.assertTrue(hasattr(self.account, "_balance"))

    def test_summary(self):
        self.account.top_up(43500)
        result = self.account.summary()
        self.assertIn("ACC001", result)
        self.assertIn("0700123456", result)
        self.assertIn("Alice Nakato", result)
        self.assertIn("43,500", result)


class TestTransaction(unittest.TestCase):
    def setUp(self):
        self.transaction = Transaction("TOP_UP", 50000)

    def test_generates_own_id_and_timestamp(self):
        self.assertTrue(self.transaction.transaction_id)
        self.assertTrue(self.transaction.date_time)

    def test_ids_are_unique(self):
        other = Transaction("CALL", 6000)
        self.assertNotEqual(self.transaction.transaction_id, other.transaction_id)

    def test_get_details(self):
        details = self.transaction.get_details()
        self.assertIn("TOP_UP", details)
        self.assertIn("50,000", details)
        self.assertIn(self.transaction.date_time, details)


class TestTransactionHistory(unittest.TestCase):
    def setUp(self):
        self.customer = Customer("Alice Nakato", "0700123456", "alice@email.com")
        self.account = Account("ACC001", self.customer)
        self.history = TransactionHistory(self.account)

    def test_starts_empty(self):
        self.assertEqual(self.history.get_all(), [])
        self.assertIsNone(self.history.get_last())

    def test_attaches_itself_to_the_account(self):
        self.assertIs(self.account.history, self.history)

    def test_add_transaction(self):
        self.history.add_transaction(Transaction("CALL", 6000))
        self.assertEqual(len(self.history.get_all()), 1)

    def test_get_last(self):
        self.history.add_transaction(Transaction("CALL", 6000))
        self.history.add_transaction(Transaction("SMS", 500))
        self.assertEqual(self.history.get_last().transaction_type, "SMS")

    def test_account_operations_are_logged(self):
        self.account.top_up(50000)
        self.account.charge_call(minutes=30, rate_per_minute=200)
        self.account.charge_sms(count=5, cost_per_sms=100)
        self.account.withdraw(1000)
        types = [t.transaction_type for t in self.history.get_all()]
        self.assertEqual(types, ["TOP_UP", "CALL", "SMS", "WITHDRAWAL"])

    def test_refused_operation_is_not_logged(self):
        self.account.top_up(1000)
        with self.assertRaises(InsufficientBalanceError):
            self.account.charge_call(minutes=300, rate_per_minute=200)
        self.assertEqual(len(self.history.get_all()), 1)


class TestAgent(unittest.TestCase):
    def setUp(self):
        self.customer = Customer("Alice Nakato", "0700123456", "alice@email.com")
        self.account = Account("ACC001", self.customer)
        self.history = TransactionHistory(self.account)
        self.agent = Agent("Daniel Obar", "AGT001", "Kampala Branch")

    def test_attributes(self):
        self.assertEqual(self.agent.name, "Daniel Obar")
        self.assertEqual(self.agent.agent_id, "AGT001")
        self.assertEqual(self.agent.branch, "Kampala Branch")

    def test_top_up_account_credits_and_logs(self):
        self.agent.top_up_account(self.account, 50000)
        self.assertEqual(self.account.check_balance(), 50000)
        self.assertEqual(self.history.get_last().transaction_type, "TOP_UP")
        self.assertEqual(self.history.get_last().amount, 50000)

    def test_top_up_account_rejects_invalid_amount(self):
        with self.assertRaises(ValueError):
            self.agent.top_up_account(self.account, 0)
        self.assertEqual(self.account.check_balance(), 0)
        self.assertEqual(self.history.get_all(), [])

    def test_withdraw_from_account_debits_and_logs(self):
        self.agent.top_up_account(self.account, 50000)
        self.agent.withdraw_from_account(self.account, 15000)
        self.assertEqual(self.account.check_balance(), 35000)
        self.assertEqual(self.history.get_last().transaction_type, "WITHDRAWAL")
        self.assertEqual(self.history.get_last().amount, 15000)

    def test_withdraw_from_account_rejects_insufficient_balance(self):
        self.agent.top_up_account(self.account, 1000)
        with self.assertRaises(InsufficientBalanceError):
            self.agent.withdraw_from_account(self.account, 5000)
        self.assertEqual(self.account.check_balance(), 1000)


if __name__ == "__main__":
    unittest.main()
