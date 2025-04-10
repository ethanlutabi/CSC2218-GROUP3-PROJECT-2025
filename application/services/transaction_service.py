from uuid import uuid4
from datetime import datetime

from domain.entities.transaction import Transaction, TransactionType
from domain.entities.account import Account
from domain.exceptions import (
    InsufficientFundsError, 
    AccountNotFoundError,
    InvalidTransactionError
)
from application.service.dtos import TransactionDTO

class TransactionService:
    """Application service for handling transactions"""
    
    def _init_(self, account_repository, transaction_repository):
        """Dependency Injection of repositories"""
        self.account_repository = account_repository
        self.transaction_repository = transaction_repository
    
    def deposit(self, account_id: str, amount: float) -> Transaction:
        """
        Process a deposit transaction
        Args:
            account_id: ID of the account to deposit to
            amount: Amount to deposit (must be positive)
        Returns:
            The created transaction
        Raises:
            AccountNotFoundError: If account doesn't exist
            InvalidTransactionError: If amount is invalid
        """
        if amount <= 0:
            raise InvalidTransactionError("Deposit amount must be positive")
        
        account = self._get_account(account_id)
        
        # Update account balance
        account.update_balance(amount)
        self.account_repository.update(account)
        
        # Create and save transaction
        transaction = Transaction(
            transaction_id=str(uuid4()),
            transaction_type=TransactionType.DEPOSIT,
            amount=amount,
            account_id=account_id,
            timestamp=datetime.now()
        )
        self.transaction_repository.add(transaction)
        
        return transaction
    
    def withdraw(self, account_id: str, amount: float) -> Transaction:
        """
        Process a withdrawal transaction
        Args:
            account_id: ID of the account to withdraw from
            amount: Amount to withdraw (must be positive)
        Returns:
            The created transaction
        Raises:
            AccountNotFoundError: If account doesn't exist
            InvalidTransactionError: If amount is invalid
            InsufficientFundsError: If account has insufficient funds
        """
        if amount <= 0:
            raise InvalidTransactionError("Withdrawal amount must be positive")
        
        account = self._get_account(account_id)
        
        # Check if withdrawal is possible
        if account.available_balance < amount:
            raise InsufficientFundsError(
                f"Available balance {account.available_balance} is less than withdrawal amount {amount}"
            )
        
        # Update account balance (negative amount for withdrawal)
        account.update_balance(-amount)
        self.account_repository.update(account)
        
        # Create and save transaction
        transaction = Transaction(
            transaction_id=str(uuid4()),
            transaction_type=TransactionType.WITHDRAWAL,
            amount=amount,
            account_id=account_id,
            timestamp=datetime.now()
        )
        self.transaction_repository.add(transaction)
        
        return transaction
    
    def _get_account(self, account_id: str) -> Account:
        """Helper method to get account or raise exception"""
        account = self.account_repository.get_by_id(account_id)
        if not account:
            raise AccountNotFoundError(f"Account with ID {account_id} not found")
        return account