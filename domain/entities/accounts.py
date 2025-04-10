from datetime import datetime
from enum import Enum
from typing import Optional, List
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

class AccountType(str,Enum):
    CHECKING = "checking"
    SAVINGS = "savings"

class AccountStatus(str, Enum):
    ACTIVE = "active"
    CLOSED = "closed"

class Account(BaseModel):
    account_id: UUID = Field(default_factory=uuid4)
    acount_type: AccountType
    balance: float = 0.0
    status: AccountStatus = AccountStatus.ACTIVE
    date_created:datetime = Field(default_factory= datetime.now)

    def deposit(self, amount: float) ->bool:
        # Add money to the accunt
        if amount <= 0:
            return False
        self.balance +=amount
        return True

    def withdraw(self, amount:float)-> bool:
        # Remove money from the account
        return amount>0 and amount <= self.balance

    def close(self)->bool:
        """CLose the account if balance is zero"""
        if self.balance == 0:
            self.status =AccountStatus.CLOSED
            return True
        return False

    class Config:
        from_attributes = True
