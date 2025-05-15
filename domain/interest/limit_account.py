# domain/interest/limit_account.py
from domain.accounts.create_accounts import Account
from domain.interest.limits_constraint import LimitConstraint 
from datetime import date

class LimitedAccount(Account):
    """
    Decorator around an Account to enforce daily/monthly limits.
    """
    def __init__(self, base_account: Account, constraint: LimitConstraint):
        super().__init__(
            base_account.account_id,
            base_account.owner,
            base_account.balance,
            interest_strategy=base_account.interest_strategy,
            last_interest_date=base_account.last_interest_date
        )
        self._base = base_account
        self._constraint = constraint

    def deposit(self, amount: float):
        today = date.today()
        self._constraint.check(amount, today)
        self._base.deposit(amount)
        self._constraint.record(amount, today)
        self.balance = self._base.balance

    def withdraw(self, amount: float):
        today = date.today()
        self._constraint.check(amount, today)
        self._base.withdraw(amount)
        self._constraint.record(amount, today)
        self.balance = self._base.balance

    def account_type(self) -> str:
        return self._base.account_type()