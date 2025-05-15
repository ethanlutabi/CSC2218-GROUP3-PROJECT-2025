from abc import ABC, abstractmethod
from datetime import date


class Account(ABC):
    def __init__(self, account_id: str, owner: str, balance: float = 0.0,
                 interest_strategy =  None, last_interest_date: date = None):
        self.account_id = account_id
        self.owner = owner
        self.balance = balance
        self.interest_strategy = interest_strategy
        self.last_interest_date = last_interest_date or date.today()

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



    



