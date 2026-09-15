# Group Members:
# Mulisa Docile
# Daniel Obar: M25B38/014
# Abi Mirembe
# Flavia Sherinah
# Victoria Marvis
# Mordecai Corey Kwezi


class MobileMoneyAccount:
    def __init__(self, phone_number, owner_name):
        self._phone_number = phone_number
        self._owner_name = owner_name
        self._balance = 0

    @property
    def phone_number(self):
        return self._phone_number

    @property
    def owner_name(self):
        return self._owner_name

    @property
    def balance(self):
        return self._balance

    def top_up(self, amount):
        if amount <= 0:
            raise ValueError("Top-up amount must be positive.")
        self._balance += amount

    def charge_call(self, minutes, rate_per_minute):
        cost = minutes * rate_per_minute
        if cost > self._balance:
            raise InsufficientBalanceError(
                f"Insufficient balance for call. Need UGX {cost:,.0f}, have UGX {self._balance:,.0f}."
            )
        self._balance -= cost

    def charge_sms(self, count, cost_per_sms):
        cost = count * cost_per_sms
        if cost > self._balance:
            raise InsufficientBalanceError(
                f"Insufficient balance for SMS. Need UGX {cost:,.0f}, have UGX {self._balance:,.0f}."
            )
        self._balance -= cost

    def check_balance(self):
        return self._balance

    def summary(self):
        return (
            f"Account Summary\n"
            f"  Phone Number : {self._phone_number}\n"
            f"  Owner        : {self._owner_name}\n"
            f"  Balance      : UGX {self._balance:,.0f}"
        )


class InsufficientBalanceError(Exception):
    pass

class agent:
    pass