from uuid import uuid4
from datetime import datetime
from typing import Optional

from domain.entities.account import Account, AccountType, AccountStatus
from domain.exceptions import InvalidAccountTypeError
from application.service.dtos import CreateAccountDTO

class AccountCreationService:
    """Application service for account creation (Factory Pattern)"""
    
    def _init_(self, account_repository):
        """Dependency Injection of account repository"""
        self.account_repository = account_repository
    
    def create_account(self, account_dto: CreateAccountDTO) -> str:
        """
        Creates a new account based on the provided DTO
        Args:
            account_dto: Data Transfer Object with account creation details
        Returns:
            The ID of the newly created account
        Raises:
            InvalidAccountTypeError: If account type is not supported
        """
        try:
            account_type = AccountType(account_dto.account_type.upper())
        except ValueError:
            raise InvalidAccountTypeError(f"Invalid account type: {account_dto.account_type}")
        
        # Generate unique ID for the account
        account_id = str(uuid4())
        
        # Create new account entity
        new_account = Account(
            account_id=account_id,
            account_type=account_type,
            balance=account_dto.initial_deposit,
            status=AccountStatus.ACTIVE,
            creation_date=datetime.now()
        )
        
        # Save account through repository
        self.account_repository.add(new_account)
        
        return account_id