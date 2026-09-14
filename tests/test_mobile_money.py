# Group Members:
# Mulisa Docile
# Daniel Obar
# Abi Mirembe
# Flavia Sherinah
# Victoria Marvis
# Mordecai

import unittest
from src.mobile_money import MobileMoneyAccount, InsufficientBalanceError


class TestMobileMoneyAccount(unittest.TestCase):
    def setUp(self):
        self.account = MobileMoneyAccount("0700123456", "Alice")

    def test_initial_balance_is_zero(self):
        self.assertEqual(self.account.balance, 0)

    def test_top_up(self):
        self.account.top_up(10000)
        self.assertEqual(self.account.balance, 10000)

    def test_multiple_top_ups(self):
        self.account.top_up(5000)
        self.account.top_up(3000)
        self.assertEqual(self.account.balance, 8000)

    def test_top_up_zero_raises(self):
        with self.assertRaises(ValueError):
            self.account.top_up(0)

    def test_top_up_negative_raises(self):
        with self.assertRaises(ValueError):
            self.account.top_up(-500)

    def test_charge_call(self):
        self.account.top_up(10000)
        self.account.charge_call(minutes=10, rate_per_minute=200)
        self.assertEqual(self.account.balance, 8000)

    def test_charge_sms(self):
        self.account.top_up(5000)
        self.account.charge_sms(count=10, cost_per_sms=100)
        self.assertEqual(self.account.balance, 4000)

    def test_charge_call_insufficient_balance(self):
        self.account.top_up(500)
        with self.assertRaises(InsufficientBalanceError):
            self.account.charge_call(minutes=10, rate_per_minute=200)
        self.assertEqual(self.account.balance, 500)

    def test_charge_sms_insufficient_balance(self):
        self.account.top_up(500)
        with self.assertRaises(InsufficientBalanceError):
            self.account.charge_sms(count=10, cost_per_sms=100)
        self.assertEqual(self.account.balance, 500)

    def test_check_balance(self):
        self.account.top_up(7500)
        self.assertEqual(self.account.check_balance(), 7500)

    def test_summary(self):
        result = self.account.summary()
        self.assertIn("0700123456", result)
        self.assertIn("Alice", result)
        self.assertIn("UGX 0", result)

    def test_phone_number_property(self):
        self.assertEqual(self.account.phone_number, "0700123456")

    def test_owner_name_property(self):
        self.assertEqual(self.account.owner_name, "Alice")


if __name__ == "__main__":
    unittest.main()
