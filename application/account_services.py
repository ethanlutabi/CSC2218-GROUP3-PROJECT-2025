# this file defines the acount creation service, which is responsible for creating new accounts.
from typing import Optional
from uuid import uuid4
from datetime import datetime
from domain.account import Account, AccountType, AccountStatus

class AccountCreationService:
    def __init__(self, account_repository):
        self.account_repository = account_repository
    
    def create_account(self, account_type: AccountType, initial_deposit: float = 0.0, owner_id: Optional[str] = None) -> str:
        if initial_deposit < 0:
            raise ValueError("Initial deposit cannot be negative")
        
        # For savings accounts, require minimum deposit
        if account_type == AccountType.SAVINGS and initial_deposit < 100:
            raise ValueError("Savings accounts require minimum $100 deposit")
            
        account_id = str(uuid4())
        new_account = Account(
            account_id=account_id,
            account_type=account_type,
            balance=initial_deposit,
            status=AccountStatus.ACTIVE,
            creation_date=datetime.now(),
            owner_id=owner_id
        )
        
        self.account_repository.create_account(new_account)
        return account_id