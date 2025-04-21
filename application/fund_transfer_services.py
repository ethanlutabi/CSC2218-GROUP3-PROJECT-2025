# from uuid import uuid4
# from datetime import datetime
# from domain.transaction import Transaction, TransactionType

# class FundTransferService:
#     def __init__(self, account_repo, transaction_repo):
#         self.account_repo = account_repo
#         self.transaction_repo = transaction_repo
    
#     def transfer_funds(self, source_id: str, dest_id: str, amount: float) -> Transaction:
#         if source_id == dest_id:
#             raise ValueError("Cannot transfer to same account")
        
#         source = self.account_repo.find_by_id(source_id)
#         dest = self.account_repo.find_by_id(dest_id)
        
#         if not source or not dest:
#             raise ValueError("One or both accounts not found")
        
#         if not source.can_transfer(amount):
#             raise ValueError("Source account cannot complete transfer")
        
#         # Atomic transfer operation
#         source.withdraw(amount)
#         dest.deposit(amount)
        
#         self.account_repo.save(source)
#         self.account_repo.save(dest)
        
#         transfer = Transaction(
#             transaction_id=str(uuid4()),
#             transaction_type=TransactionType.TRANSFER,
#             amount=amount,
#             timestamp=datetime.now(),
#             account_id=source_id,
#             destination_account_id=dest_id
#         )
        
#         self.transaction_repo.save(transfer)
#         return transfer

from uuid import uuid4
from datetime import datetime
from domain.transaction import Transaction, TransactionType
from domain.account import AccountStatus

class FundTransferService:
    def __init__(self, account_repo, transaction_repo):
        self.account_repo = account_repo
        self.transaction_repo = transaction_repo
    
    def transfer_funds(self, source_id: str, dest_id: str, amount: float) -> Transaction:
        # Validate accounts are different
        if source_id == dest_id:
            raise ValueError("Cannot transfer to same account")
        
        # Retrieve accounts
        source = self.account_repo.find_by_id(source_id)
        dest = self.account_repo.find_by_id(dest_id)
        
        # Check accounts exist
        if not source or not dest:
            raise ValueError("One or both accounts not found")
        
        # Validate source account can transfer
        if not source.can_transfer(amount):
            raise ValueError("Source account cannot complete transfer")
            
        # Validate destination account can receive
        if dest.status != AccountStatus.ACTIVE:
            raise ValueError("Destination account is not active")
        
        # Perform atomic transfer
        source.withdraw(amount)
        dest.deposit(amount)
        
        # Persist changes
        self.account_repo.save(source)
        self.account_repo.save(dest)
        
        # Create transaction record
        transfer = Transaction(
            transaction_id=str(uuid4()),
            transaction_type=TransactionType.TRANSFER,
            amount=amount,
            timestamp=datetime.now(),
            account_id=source_id,
            destination_account_id=dest_id
        )
        
        self.transaction_repo.save(transfer)
        return transfer