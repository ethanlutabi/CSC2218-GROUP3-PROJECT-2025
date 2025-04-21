# this file defines the Transaction class and its properties
from uuid import uuid4
from datetime import datetime
from domain.transaction import Transaction, TransactionType

class TransactionService:
    def __init__(self, account_repository, transaction_repository):
        self.account_repository = account_repository
        self.transaction_repository = transaction_repository
    
    def deposit(self, account_id: str, amount: float) -> Transaction:
        account = self.account_repository.get_account_by_id(account_id)
        if not account:
            raise ValueError("Account not found")
        
        account.deposit(amount)
        self.account_repository.update_account(account)
        
        transaction = Transaction(
            transaction_id=str(uuid4()),
            transaction_type=TransactionType.DEPOSIT,
            amount=amount,
            timestamp=datetime.now(),
            account_id=account_id
            
        )
        
        self.transaction_repository.save_transaction(transaction)
        return transaction
    
    def withdraw(self, account_id: str, amount: float) -> Transaction:
        account = self.account_repository.get_account_by_id(account_id)
        if not account:
            raise ValueError("Account not found")
        
        account.withdraw(amount)
        self.account_repository.update_account(account)
        
        transaction = Transaction(
            transaction_id=str(uuid4()),
            transaction_type=TransactionType.WITHDRAW,
            amount=amount,
            timestamp=datetime.now(),
            account_id=account_id,
            
        )
        
        self.transaction_repository.save_transaction(transaction)
        return transaction