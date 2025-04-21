# this file defines the account domain model
from dataclasses import dataclass
from enum import Enum, auto
from datetime import datetime
from typing import Optional

class AccountType(Enum):
    CHECKING = auto()
    SAVINGS = auto()

class AccountStatus(Enum):
    ACTIVE = auto()
    CLOSED = auto()
    

@dataclass
class Account:
    account_id: str
    account_type: AccountType
    balance: float
    status: AccountStatus
    creation_date: datetime
    owner_id: Optional[str] = None 
    
    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.balance += amount
    
    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if self.balance < amount:
            raise ValueError("Insufficient funds")
        self.balance -= amount
        
    def can_transfer(self, amount: float) -> bool:
        return self.status == AccountStatus.ACTIVE and self.balance >= amount

