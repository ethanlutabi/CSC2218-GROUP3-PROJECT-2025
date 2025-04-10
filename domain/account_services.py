from typing import Optional
from uuid import UUID
from models.accounts import Account, AccountType
from models.transactions import Transaction, TransactionType


class AccountValidationService:
    """Service for validating account operations"""

    @staticmethod
    def validate_deposit(amount: float) -> bool:
        """Validate if a deposit amount is valid"""
        return amount > 0

    @staticmethod
    def validate_withdrawal(account: Account, amount: float) -> bool:
        """Validate if a withdrawal is allowed based on general rules"""
        # Basic validation: amount must be positive and not exceed balance
        if amount <= 0 or amount > account.balance:
            return False
        
        # Account-specific validation is handled by the account classes
        return True


class TransactionService:
    """Service for creating and managing transactions"""
    
    @staticmethod
    def create_transaction(account_id: UUID, transaction_type: TransactionType, amount: float) -> Transaction:
        """Create a new transaction record"""
        return Transaction(
            account_id=account_id,
            transaction_type=transaction_type,
            amount=amount
        )


class CheckingAccount(Account):
    def __init__(self, **data):
        super().__init__(account_type=AccountType.CHECKING, **data)
    
    def can_withdraw(self, amount: float) -> bool:
        """Check if withdrawal is allowed for this account type"""
        # Use the validation service for basic validation
        if not AccountValidationService.validate_withdrawal(self, amount):
            return False
        
        # Checking accounts have no additional restrictions
        return True


class SavingsAccount(Account):
    def __init__(self, minimum_balance: float = 0.0, **data):
        super().__init__(account_type=AccountType.SAVINGS, **data)
        self.minimum_balance = minimum_balance
    
    def can_withdraw(self, amount: float) -> bool:
        """Check if withdrawal is allowed for this account type"""
        # Use the validation service for basic validation
        if not AccountValidationService.validate_withdrawal(self, amount):
            return False
        
        # Savings accounts require maintaining minimum balance
        return (self.balance - amount) >= self.minimum_balance
    
    def withdraw(self, amount: float) -> bool:
        """Override withdraw to enforce minimum balance"""
        if not self.can_withdraw(amount):
            return False
        return super().withdraw(amount)