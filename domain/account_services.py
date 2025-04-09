from typing import Optional
from uuid import UUID

from models.accounts import Account, AccountType
from models.transactions import Transaction, TransactionType


class AccountRulesServices:
    """Service for enforcing business rules on accounts"""

    @staticmethod
    def validate_deposit(account:Account, amount:float)-> bool:
        """Validate if a deposit is allowed"""
        return amount > 0

    @staticmethod
    def validate_withdraw(account:Account, amount:float)->bool:
        """Validate if a withdrawal is allowed"""
        if amount <= 0:
            return False
        if amount> account.balance:
            return False
        if account.account_type.CHECKING:
            return True
        elif account.account_type.SAVINGS:

            remaining_balance= account.balance - amount
            return remaining_balance >= 0
        return True

    @staticmethod
    def create_transaction(account_id:UUID, transaction_type:TransactionType, amount:float)-> Transaction:
        """Create a new transaction record"""
        return Transaction(
            account_id = account_id,
            transaction_type = transaction_type,
            amount= amount
        )
class CheckingAccount(Account):
    def __init__(self, **data):
        super().__init__(account_type= AccountType.CHECKING, **data)

        # Could override withdraw method if need be
        # def withdraw(self,amount:float)->bool:
        #    return super().withdraw(amount)


class SavingsAccount(Account):
    def __iniy__(self, mininum_balance:float=0.0,**data):
        super().__init__(account_type= AccountType.SAVINGS,**data)
        self.minimum_balance = mininum_balance

    def withdraw(self, amount:float)->bool:
        """Override withdraw to enforce mimimum balance"""
        if self.balance - amount < self.minimum_balance:
            return False
        return super().withdraw(amount)
