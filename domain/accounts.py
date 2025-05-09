from abc import ABC, abstractmethod

class Account(ABC):
    def __init__(self, account_id: str, owner: str, balance: float = 0.0):
        self.account_id = account_id
        self.owner = owner
        self.balance = balance

    def deposit(self, amount: float):
        if amount <= 0:
            raise ValueError("Deposit must be positive")
        self.balance += amount

    def withdraw(self, amount: float):
        if amount <= 0:
            raise ValueError("Withdrawal must be positive")
        if self.balance < amount:
            raise ValueError("Insufficient balance")
        self.balance -= amount

    @abstractmethod
    def account_type(self) -> str:
        pass

class SavingsAccount(Account):
    def account_type(self) -> str:
        return "savings"

class CheckingAccount(Account):
    def account_type(self) -> str:
        return "checking"


class AccountFactory:
    @staticmethod
    def create_account(account_type: str, account_id: str, owner: str, balance: float = 0.0) -> Account:
        if account_type == "savings":
            return SavingsAccount(account_id, owner, balance)
        elif account_type == "checking":
            return CheckingAccount(account_id, owner, balance)
        else:
            raise ValueError(f"Unknown account type: {account_type}")
